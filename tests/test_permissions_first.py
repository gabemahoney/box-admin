"""Setup starts permissive: the start lines carry the flags, CLAUDE.md step 0 merges permissions.json."""

import json, os, pathlib, re, shutil, subprocess, tempfile, unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
FLAGS = "--permission-mode acceptEdits --allowedTools Bash"


class PermissionsFirstTest(unittest.TestCase):
    def test_start_lines_carry_flags(self):
        readme = (REPO / "README.md").read_text()
        self.assertIn(f"claude {FLAGS}` (never auto", readme)
        self.assertRegex(readme, r"exec claude " + re.escape(FLAGS) + "'")

    def test_claude_md_names_accept_edits_as_setup_mode(self):
        text = (REPO / "CLAUDE.md").read_text()
        self.assertIn("acceptEdits", next(l for l in text.splitlines() if l.startswith("Setup ")))
        self.assertNotRegex(text, r"\bdefault (permission )?mode\b")

    def test_step_zero_precedes_step_one_and_writes_safely(self):
        text = (REPO / "CLAUDE.md").read_text()
        self.assertLess(text.index("\n0. Permissions first"), text.index("\n1. `<entry dir>`"))
        step = text.split("\n0. ")[1].split("\n1. ")[0]
        for needle in ("permissions.json", "chmod 600", "umask 077", "never use auto mode"):
            self.assertIn(needle, step)
        self.assertNotIn("bypassPermissions\"", step)

    @unittest.skipUnless(shutil.which("jq"), "jq missing")
    def test_step_zero_merges_exactly(self):  # b.fwk: file lists first, then live extras; live settings win
        cmd = re.search(r"`(mkdir -p ~/\.claude && .*?settings\.json)`\. It keeps", (REPO / "CLAUDE.md").read_text())[1]
        self.maxDiff = None
        live_perms = {"allow": ["Bash", "Bash(host-only *)"], "ask": ["Bash(host-ask *)"],
                      "deny": ["Read(~/host-only/**)"], "additionalDirectories": ["~/host-dir"], "defaultMode": "plan"}
        for live_file in (None, {"env": {"DUMMY": "x"}, "permissions": live_perms}):
            with self.subTest(live=bool(live_file)), tempfile.TemporaryDirectory() as home:
                live = pathlib.Path(home, ".claude", "settings.json")
                if live_file:
                    live.parent.mkdir()
                    live.write_text(json.dumps(live_file))
                run = lambda: subprocess.run(["bash", "-c", cmd], cwd=REPO, env={**os.environ, "HOME": home}, check=True)
                run()
                got, first = json.loads(live.read_text()), live.read_bytes()
                self.assertEqual(live.stat().st_mode & 0o777, 0o600)
                run()
                self.assertEqual(live.read_bytes(), first)  # a second run is a no-op
                want = json.loads((REPO / "permissions.json").read_text())
                for k, extra in (live_file or {}).get("permissions", {}).items():
                    want[k] = extra if isinstance(extra, str) else want[k] + [r for r in extra if r not in want[k]]
                want["additionalDirectories"] = [re.sub("^~/", home + "/", d) for d in want["additionalDirectories"]]
                self.assertEqual(got, {**(live_file or {}), "permissions": want})

    def test_permissions_json_matches_core(self):  # b.fwk: core's files/.claude/settings.json is the source
        root = os.environ.get("BOX_ADMIN_ROOT")
        core = pathlib.Path(root, "box_admin_core") if root else REPO.parent / "box_admin_core"
        if not (core / "files/.claude/settings.json").is_file():
            self.skipTest(f"no core at {core}")
        self.maxDiff = None
        want = json.loads((core / "files/.claude/settings.json").read_text())["permissions"]
        self.assertEqual(json.loads((REPO / "permissions.json").read_text()), want)

    def test_permissions_block(self):
        p = json.loads((REPO / "permissions.json").read_text())
        self.assertEqual(p["defaultMode"], "acceptEdits")
        self.assertIn("Bash", p["allow"])
        for d in ("Bash(claude)", "Bash(claude *)", "Bash(tmux kill-server*)", "Bash(pkill tmux*)"):
            self.assertIn(d, p["deny"])
        for a in ("Bash(git reset --hard*)", "Bash(git clean*)", "Bash(git stash*)"):
            self.assertIn(a, p["ask"])
        self.assertNotIn("bypassPermissions", json.dumps(p))
        self.assertNotIn("auto", p["defaultMode"])


if __name__ == "__main__":
    unittest.main()
