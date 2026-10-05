# Instructions for Claude

This repo is only the entry point for Gabe's box setup. The real repo,
`gabemahoney/box-admin-core`, is private.

1. Clone it with the personal token, without printing it:
   `GH_TOKEN="$GH_TOKEN_PERSONAL" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`
2. If `GH_TOKEN_PERSONAL` is not in your environment (check by name: `compgen -e | grep -x GH_TOKEN_PERSONAL`),
   read it by name, without printing it, from the box's long-running agent-server process started at boot:
   `GH_TOKEN="$(tr '\0' '\n' < /proc/$(pgrep -of '[a]gent_server')/environ | sed -n 's/^GH_TOKEN_PERSONAL=//p')" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`
   (`[a]` stops pgrep matching the shell running this command.)
3. Only if that also fails, ask the human to run `read -rs GH_TOKEN_PERSONAL; export GH_TOKEN_PERSONAL`
   in a terminal and restart you from it. Never ask for the token in chat.
4. Follow the Bootstrap section of `~/box_admin/box_admin_core/README.md`.

Never print, echo or log any token.
