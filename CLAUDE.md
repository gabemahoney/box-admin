# Instructions for Claude

Entry point for Gabe's box setup. The real repo, `gabemahoney/box-admin-core`, is private.
Never print, echo or log any token, and never ask for one in chat. Check variables by name only.
Never read another process's environment or memory for a token.

1. If this repo is already cloned on the box, run `git -C <its folder> pull` first, then re-read this file.
2. If `GH_TOKEN_PERSONAL` is in your own environment (`compgen -e | grep -x GH_TOKEN_PERSONAL`), clone core with it:
   `GH_TOKEN="$GH_TOKEN_PERSONAL" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`
3. Otherwise, if gh is already logged in as the personal account (`gh auth status --hostname github.com`
   lists `gabemahoney`), use gh's own credentials: `gh auth switch --hostname github.com --user gabemahoney`
   if it is not the active account, then `env -u GH_TOKEN gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`.
4. Otherwise, one human step: ask the human to run, in a terminal on this box,
   `gh auth login --hostname github.com --git-protocol https --web`
   and sign in as the personal account (`gabemahoney`) with the device code. Then do step 3.
5. Follow the Bootstrap section of `~/box_admin/box_admin_core/README.md`.
