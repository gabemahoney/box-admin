# Instructions for Claude

Entry point for Gabe's box setup; the real repo, `gabemahoney/box-admin-core`, is private.
Never print, echo or log a token; never read another process's environment.
The human names the box's layer when starting: `<layer repo URL>` and `<VAR>=<login>`, both copied from that layer's README. If either is missing, ask the human for it before step 1; never list or guess layers.

1. `<entry dir>` is this CLAUDE.md's directory; leave it where it is if BOX_ADMIN_ROOT is set or it is a checkout of gabemahoney/box-admin, i.e. `git -C "<entry dir>" remote get-url origin | grep -qE 'github\.com[:/]gabemahoney/box-admin(\.git)?$'` exits 0 (it prints nothing; never print the URL). Otherwise this repo belongs at `~/projects/box-admin`: if you are anywhere else, `mkdir -p ~/projects`, move or clone it there, and continue from that copy (`git -C ~/projects/box-admin pull` if it was already there) as `<entry dir>`; re-read its CLAUDE.md.
2. Run `"<entry dir>/clone-core"`. It clones the private core repo using the box's GitHub token.
3. If it exits non-zero, tell the human plainly what it printed and stop. On a box with no secret store,
   the human may sign gh in (`! gh auth login --hostname github.com --git-protocol https --web` as `gabemahoney`); then rerun step 2.
4. Core is now at `C="${BOX_ADMIN_ROOT:-$HOME/projects/box_admin}/box_admin_core"` (BOX_ADMIN_ROOT, if set, is an absolute path; set C in each call that uses it). Run `python3 "$C/bootstrap" <layer repo URL> <VAR>=<login>`. If it exits non-zero, tell the human plainly what it printed and stop; never fix or guess the layer URL. Otherwise follow `$C/.claude/skills/setup_box/SKILL.md`.
