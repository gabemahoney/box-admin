"""Setup starts permissive: the start lines carry the flags, CLAUDE.md step 0 installs permissions.json."""

import json, pathlib, re, unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
FLAGS = "--permission-mode acceptEdits --allowedTools Bash"


class PermissionsFirstTest(unittest.TestCase):
    def test_start_lines_carry_flags(self):
        readme = (REPO / "README.md").read_text()
        self.assertIn(f"claude {FLAGS}` (never auto", readme)
        self.assertRegex(readme, r"exec claude " + re.escape(FLAGS) + "'")

    def test_step_zero_precedes_step_one_and_merges(self):
        text = (REPO / "CLAUDE.md").read_text()
        self.assertLess(text.index("\n0. Permissions first"), text.index("\n1. `<entry dir>`"))
        step = text.split("\n0. ")[1].split("\n1. ")[0]
        for needle in ("permissions.json", ".permissions=", "chmod 600", "umask 077", "never use auto mode"):
            self.assertIn(needle, step)
        self.assertNotIn("bypassPermissions\"", step)

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
