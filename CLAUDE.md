# Instructions for Claude

Entry point for Gabe's box setup. The real repo, `gabemahoney/box-admin-core`, is private.
Never print, echo or log any token, and never ask for one in chat. Check variables by name only.
Never read another process's environment or memory for a token.

1. If this repo is already cloned on the box, run `git -C <its folder> pull` first, then re-read this file.
2. If `GH_TOKEN_PERSONAL` is in your own environment (`compgen -e | grep -x GH_TOKEN_PERSONAL`), clone core with it:
   `GH_TOKEN="$GH_TOKEN_PERSONAL" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`
3. Otherwise, check whether gh is logged in as the personal account (prints logins only):
   `env -u GH_TOKEN -u GITHUB_TOKEN gh auth status --hostname github.com --json hosts --jq '.hosts["github.com"][]? | select(.state == "success") | .login'`
   If it lists `gabemahoney`, clone with gh's own credentials, without printing them:
   `GH_TOKEN="$(env -u GH_TOKEN -u GITHUB_TOKEN gh auth token --hostname github.com --user gabemahoney)" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`
4. Otherwise, one human step: ask the human to run, in a terminal on this box,
   `gh auth login --hostname github.com --git-protocol https --web`
   and sign in as the personal account (`gabemahoney`) with the device code. Then do step 3.
5. Follow the Bootstrap section of `~/box_admin/box_admin_core/README.md`.
