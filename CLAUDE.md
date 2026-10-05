# Instructions for Claude

Entry point for Gabe's box setup; the real repo, `gabemahoney/box-admin-core`, is private.
Never print, echo or log a token; never read another process's environment.

1. This repo belongs in `~/projects/box-admin`: clone it there, or `git -C ~/projects/box-admin pull` if present; re-read this file.
2. Find the personal token (own env, then `/etc/environment`, then gh as `gabemahoney`) and clone core. Run exactly:
   ```
   T="${GH_TOKEN_PERSONAL:-$(sed -n 's/^GH_TOKEN_PERSONAL=//p' /etc/environment 2>/dev/null | tr -d '"')}"; T="${T:-$(env -u GH_TOKEN -u GITHUB_TOKEN gh auth token --hostname github.com --user gabemahoney 2>/dev/null)}"; if [ -n "$T" ]; then GH_TOKEN="$T" gh repo clone gabemahoney/box-admin-core ~/projects/box_admin/box_admin_core; else echo "no token in env, /etc/environment or gh"; fi; unset T
   ```
3. Only if all three find nothing, ask the human to sign in: type
   `! gh auth login --hostname github.com --git-protocol https --web` as `gabemahoney`, then run step 2 again.
4. Find the box type: the core README's Box types table lists each type's check command; run them and use the one that matches. If none or several match, ask the human.
5. Run `python3 ~/projects/box_admin/box_admin_core/bootstrap <type>`, then follow `~/projects/box_admin/box_admin_core/.claude/skills/setup_box/SKILL.md`.
