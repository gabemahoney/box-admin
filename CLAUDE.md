# Instructions for Claude

Entry point for Gabe's box setup. The real repo, `gabemahoney/box-admin-core`, is private, so the
first run on a new box goes like this. Never print, echo or log a token; check variables by name;
never read another process's environment.

1. If this repo was already cloned here, `git -C <its folder> pull` and re-read this file.
2. If `GH_TOKEN_PERSONAL` is in your environment (`compgen -e | grep -x GH_TOKEN_PERSONAL`), clone core:
   `GH_TOKEN="$GH_TOKEN_PERSONAL" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`
3. Otherwise it is usually in the box's environment file, which shells here don't always load. Check
   by name (`grep -c '^GH_TOKEN_PERSONAL=' /etc/environment`), then clone with it, read in memory:
   `GH_TOKEN="$(sed -n 's/^GH_TOKEN_PERSONAL=//p' /etc/environment | tr -d '"')" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`
4. If it isn't there either, the next step is the usual gh sign-in: ask the human to type
   `! gh auth login --hostname github.com --git-protocol https --web` and sign in as `gabemahoney`
   (a minute in the browser with a device code), then clone with gh's sign-in:
   `GH_TOKEN="$(env -u GH_TOKEN -u GITHUB_TOKEN gh auth token --hostname github.com --user gabemahoney)" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`
5. Follow the Bootstrap section of `~/box_admin/box_admin_core/README.md`.
