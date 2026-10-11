"""b.7on: no file of this repo (tracked, or new and not ignored) holds a term of TERMS, in any case, in its
path or text; no exclusions. TERMS is stored ROT13-encoded, so this file holds none; decoded at run time."""

import codecs, os, pathlib, re, subprocess, sys, unittest

sys.dont_write_bytecode = True
REPO = pathlib.Path(__file__).resolve().parent.parent
TERMS = codecs.decode("aivqvn bzavirefr utk tznubarl-aiqn jbex-tvg-pbasvt ubeqr tyrna vasrerapr-ncv "
                      "vasrerapruho vasuho qtkp gryrcbeg bzavfgngvba vgff znantrfbsg ainc", "rot13").split()
PATTERN = "|".join(TERMS)  # letters and hyphens only: the same regex for Python and grep -E


class TermFreeTest(unittest.TestCase):
    def test_no_file_holds_a_term_in_its_path_or_text(self):  # b.7on HARD RULE extended
        listed = subprocess.run(["git", "-C", str(REPO), "ls-files", "-z", "--cached", "--others",
                                 "--exclude-standard"], capture_output=True, text=True, check=True).stdout.split("\0")
        files = [f for f in listed if f and (REPO / f).is_file()]  # a tracked file deleted here is gone
        self.assertTrue(files)
        term = re.compile(PATTERN.encode(), re.I)
        self.assertEqual([f"{f}: {m.group().decode().lower()}" for f in files
                          for m in [term.search(f.encode()) or term.search((REPO / f).read_bytes())] if m], [])
        grep = subprocess.run(["grep", "-liE", "-e", PATTERN, "--", *files], cwd=REPO, capture_output=True, text=True)
        self.assertEqual((grep.returncode, grep.stdout), (1, ""))  # the plain grep, too: no match


if __name__ == "__main__":
    unittest.main()
