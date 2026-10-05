# Instructions for Claude

Entry point for Gabe's box setup. The real repo, `gabemahoney/box-admin-core`, is private.
Never print, echo or log any token. Check variables by name only. Do each step without asking the human unless a step says to.

1. If this repo is already cloned on the box, run `git -C <its folder> pull` first, then re-read this file.
2. Clone core with the personal token:
   `GH_TOKEN="$GH_TOKEN_PERSONAL" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`
3. If `GH_TOKEN_PERSONAL` is not in your environment (`compgen -e | grep -x GH_TOKEN_PERSONAL` prints nothing),
   find it in memory, without printing it: first in the environment of your user's own processes, oldest
   first, then in `/etc/environment`. Run this as one command:
   ```
   t=$(for p in $(ps -u "$(id -u)" -o pid= --sort=start_time); do tr '\0' '\n' 2>/dev/null < /proc/$p/environ | sed -n 's/^GH_TOKEN_PERSONAL=//p'; done | grep -m1 .); [ -n "$t" ] || t=$(sed -n 's/^GH_TOKEN_PERSONAL="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' /etc/environment 2>/dev/null | head -1); [ -n "$t" ] && GH_TOKEN="$t" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core; unset t
   ```
4. Only if that also fails, ask the human to do one of these in a terminal on the box, then restart you from it:
   `gh auth login` (device flow, as the personal GitHub account), or `read -rs GH_TOKEN_PERSONAL; export GH_TOKEN_PERSONAL`.
   Never ask for the token in chat.
5. Follow the Bootstrap section of `~/box_admin/box_admin_core/README.md`.
