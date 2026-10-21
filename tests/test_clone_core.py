"""b.sct: clone-core and CLAUDE.md steps 2 and 4 resolve the box_admin root, not a fixed ~/projects/box_admin."""

import pathlib, re, shutil, subprocess, sys, tempfile, unittest

sys.dont_write_bytecode = True
REPO = pathlib.Path(__file__).resolve().parent.parent


class CloneCoreRootTest(unittest.TestCase):
    def run_clone_core(self, tmp, entry, cores, git_file=False, root=None, gh_exit=0, sticky=False):
        """Run a copy at <entry>/clone-core, HOME=<tmp>/home, each core holding .git (a file if git_file), stub gh
        exiting gh_exit, entry's parent sticky if sticky; returns (exit code, stdout, gh arguments)."""
        home, bin_ = tmp / "home", tmp / "bin"
        for core in cores:
            core.mkdir(parents=True)
            if git_file:
                (core / ".git").write_text("gitdir: elsewhere\n")
            else:
                (core / ".git").mkdir()
        entry.mkdir(parents=True)
        if sticky:
            entry.parent.chmod(0o1777)
        bin_.mkdir()
        shutil.copy(REPO / "clone-core", entry / "clone-core")
        (bin_ / "gh").write_text(f'#!/bin/sh\necho "$@" > "{tmp}/gh.args"\nexit {gh_exit}\n')
        (bin_ / "gh").chmod(0o755)
        env = {"HOME": str(home), "PATH": f"{bin_}:/usr/bin:/bin", "GH_TOKEN_PERSONAL": "stub"}
        if root:
            env["BOX_ADMIN_ROOT"] = str(root)
        r = subprocess.run(["bash", str(entry / "clone-core")], env=env, capture_output=True, text=True)
        args = tmp / "gh.args"
        return r.returncode, r.stdout, args.read_text() if args.exists() else ""

    def test_core_path_follows_root_resolution(self):
        new, old = "home/projects/sysadmin-project/box_admin_dev/box_admin_core", "home/projects/box_admin/box_admin_core"
        cases = [  # (name, entry, cores, .git is a file, BOX_ADMIN_ROOT, expected core, cloned); paths under tmp
            ("BOX_ADMIN_ROOT wins", "home/dev/box_admin", ["home/dev/box_admin_core"], False, "r",
             "r/box_admin_core", True),
            ("entry parent holds core", "home/dev/box_admin", ["home/dev/box_admin_core", new, old], False, None,
             "home/dev/box_admin_core", False),
            ("worktree core is found", "home/dev/box_admin", ["home/dev/box_admin_core"], True, None,
             "home/dev/box_admin_core", False),
            ("entry parent outside HOME", "home2/box_admin", ["home2/box_admin_core"], False, None, new, True),
            ("new default beats old", "elsewhere/box_admin", [new, old], False, None, new, False),
            ("older box", "elsewhere/box_admin", [old], False, None, old, False),
            ("no core: clones to default", "home/projects/box-admin", [], False, None, new, True),
        ]
        for name, entry, cores, git_file, root, expected, cloned in cases:
            with self.subTest(name), tempfile.TemporaryDirectory() as d:
                tmp = pathlib.Path(d).resolve()
                code, out, gh = self.run_clone_core(tmp, tmp / entry, [tmp / c for c in cores], git_file,
                                                    root and tmp / root)
                self.assertEqual(code, 0)
                self.assertEqual(out.splitlines()[-1], str(tmp / expected))
                self.assertEqual(gh, f"repo clone gabemahoney/box-admin-core {tmp / expected} -- -q\n" if cloned else "")

    def test_sticky_entry_parent_is_not_trusted(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = pathlib.Path(d).resolve()
            new = tmp / "home/projects/sysadmin-project/box_admin_dev/box_admin_core"
            code, out, gh = self.run_clone_core(tmp, tmp / "home/shared/box_admin", [tmp / "home/shared/box_admin_core"],
                                                sticky=True)
            self.assertEqual((code, out.splitlines()[-1]), (0, str(new)))
            self.assertEqual(gh, f"repo clone gabemahoney/box-admin-core {new} -- -q\n")

    def test_failed_clone_exits_non_zero_without_a_core_path(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = pathlib.Path(d).resolve()
            code, out, gh = self.run_clone_core(tmp, tmp / "elsewhere/box_admin", [], gh_exit=1)
            self.assertNotEqual(code, 0)
            self.assertNotIn("box_admin_core", out)
            self.assertTrue(gh)


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

    def test_step_4_hands_root_to_bootstrap(self):
        self.assertIn('`BOX_ADMIN_ROOT="${C%/*}" python3 "$C/bootstrap" <layer repo URL> <VAR>=<login>`', self.step(4))


if __name__ == "__main__":
    unittest.main()
