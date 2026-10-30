"""b.sct: clone-core prints core's path (the default root, or ~/projects/box_admin on an older box) and CLAUDE.md steps 2 and 4 use it."""

import pathlib, re, shutil, subprocess, sys, tempfile, unittest

sys.dont_write_bytecode = True
REPO = pathlib.Path(__file__).resolve().parent.parent
URL = "https://github.com/gabemahoney/box-admin-core.git"


class CloneCoreRootTest(unittest.TestCase):
    def run_clone_core(self, tmp, cores, root=None, git_exit=0):
        """Run clone-core with HOME=<tmp>/home, each core holding a .git dir, stub git exiting git_exit;
        returns (exit code, stdout, stderr, git arguments)."""
        home, bin_ = tmp / "home", tmp / "bin"
        home.mkdir()
        for core in cores:
            (core / ".git").mkdir(parents=True)
        bin_.mkdir()
        (bin_ / "git").write_text(f'#!/bin/sh\necho "$@" > "{tmp}/git.args"\nexit {git_exit}\n')
        (bin_ / "git").chmod(0o755)
        env = {"HOME": str(home), "PATH": f"{bin_}:/usr/bin:/bin", "GH_TOKEN_PERSONAL": "stub",
               "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}
        if root:
            env["BOX_ADMIN_ROOT"] = str(root)
        r = subprocess.run(["bash", str(REPO / "clone-core")], env=env, capture_output=True, text=True)
        args = tmp / "git.args"
        return r.returncode, r.stdout, r.stderr, args.read_text() if args.exists() else ""

    def test_core_path_follows_root_resolution(self):
        new, old = "home/projects/sysadmin-project/box_admin_dev/box_admin_core", "home/projects/box_admin/box_admin_core"
        cases = [  # (name, cores, BOX_ADMIN_ROOT, expected core, cloned); paths under tmp
            ("BOX_ADMIN_ROOT wins", [new, old], "r", "r/box_admin_core", True),
            ("new default beats old", [new, old], None, new, False),
            ("older box", [old], None, old, False),
            ("no core: clones to default", [], None, new, True),
        ]
        for name, cores, root, expected, cloned in cases:
            with self.subTest(name), tempfile.TemporaryDirectory() as d:
                tmp = pathlib.Path(d).resolve()
                code, out, err, git = self.run_clone_core(tmp, [tmp / c for c in cores], root and tmp / root)
                self.assertEqual(code, 0)
                self.assertEqual(out, f"{tmp / expected}\n")
                if cloned:
                    self.assertTrue(git.endswith(f"clone -q {URL} {tmp / expected}\n"), git)
                else:
                    self.assertEqual(git, "")
                if expected == old:
                    self.assertTrue((tmp / old / ".git").is_dir())
                    self.assertFalse((tmp / new).parent.exists())
                self.assertEqual("migration pending" in err.lower(), expected == old)
                if expected == old:
                    self.assertRegex(err, r"(?i)setup_box.*approv")

    def test_old_location_is_documented_as_pending_setup_box_approval(self):  # b.6wi
        for name in ("clone-core", "README.md"):
            with self.subTest(name=name):
                text = (REPO / name).read_text()
                if name == "clone-core":  # a runtime warning cannot repair the header's promise
                    text = "\n".join(line for line in text.splitlines() if line.startswith("#"))
                text = next(p for p in text.split("\n\n") if "~/projects/box_admin" in p)
                self.assertTrue(re.search(r"(?is)(?:until|pending)[^.]*setup_box[^.]*(?:approv|\bOK\b)", text),
                                f"{name}: describe the old location as pending setup_box approval")

    def test_failed_clone_exits_non_zero_without_a_core_path(self):
        with tempfile.TemporaryDirectory() as d:
            code, out, err, git = self.run_clone_core(pathlib.Path(d).resolve(), [], git_exit=1)
            self.assertNotEqual(code, 0)
            self.assertNotIn("box_admin_core", out)
            self.assertTrue(git)


class ClaudeMdRootTest(unittest.TestCase):
    def step(self, n):
        text = (REPO / "CLAUDE.md").read_text()
        return re.search(rf"^{n}\. .*?(?=^\d+\. |\Z)", text, re.M | re.S).group()

    def test_steps_2_and_4_take_core_from_clone_core_not_a_fixed_root(self):
        for n in (2, 4):
            with self.subTest(step=n):
                self.assertNotRegex(self.step(n), r"(~|\$HOME)/projects/")
        for phrase in ("core's absolute path is the last line it prints on stdout", 'set `C="<that path>"`'):
            self.assertIn(phrase, self.step(2))

    def test_step_4_hands_root_to_core_scripts(self):
        for cmd in ('`BOX_ADMIN_ROOT="${C%/*}" python3 "$C/new_layer" <type>',
                    '`BOX_ADMIN_ROOT="${C%/*}" python3 "$C/bootstrap" <layer repo URL> <VAR>=<login>`'):
            self.assertIn(cmd, self.step(4))

    def test_step_4_gates_existing_layouts_before_bootstrap(self):  # b.6wi
        # Static guidance guard; the command contracts above still cover new-layer setup.
        guard = self.step(4).split('`BOX_ADMIN_ROOT="${C%/*}" python3 "$C/bootstrap"', 1)[0]
        self.assertRegex(guard, r"(?is)existing.{0,300}setup_box.{0,160}before.{0,40}bootstrap",
                         "Route existing layouts through setup_box before bootstrap can clone destinations.")


if __name__ == "__main__":
    unittest.main()
