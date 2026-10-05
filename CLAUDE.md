# Instructions for Claude

Entry point for Gabe's box setup; the real repo, `gabemahoney/box-admin-core`, is private.
Never print, echo or log a token; never read another process's environment.

1. This repo belongs at `~/projects/box-admin`. If you are anywhere else, `mkdir -p ~/projects`, move or clone it there, and continue from that copy (`git -C ~/projects/box-admin pull` if it was already there); re-read `~/projects/box-admin/CLAUDE.md`.
2. Run `~/projects/box-admin/clone-core`. It clones the private core repo using the box's GitHub token.
3. Only if it exits non-zero, ask the human to sign in: type
   `! gh auth login --hostname github.com --git-protocol https --web` as `gabemahoney`, then run step 2 again.
4. Find the box type: the Box types table in `~/projects/box_admin/box_admin_core/README.md` lists each type's check command; run them and use the one that matches. If none or several match, ask the human.
5. Run `python3 ~/projects/box_admin/box_admin_core/bootstrap <type>`, then follow `~/projects/box_admin/box_admin_core/.claude/skills/setup_box/SKILL.md`.
