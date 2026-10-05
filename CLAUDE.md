# Instructions for Claude

Entry point for Gabe's box setup. The real repo, `gabemahoney/box-admin-core`, is private.
Never print, echo or log a token; never read another process's environment.

1. If this repo was already cloned here, `git -C <its folder> pull` and re-read this file.
2. Find the personal token and clone core, in ONE command. It checks, in order, (a) your own
   environment, (b) the box's environment file `/etc/environment`, (c) gh's sign-in as `gabemahoney`,
   and clones with the first one found, never printing it. Run it exactly as written:
   ```
   T="${GH_TOKEN_PERSONAL:-$(sed -n 's/^GH_TOKEN_PERSONAL=//p' /etc/environment 2>/dev/null | tr -d '"')}"; T="${T:-$(env -u GH_TOKEN -u GITHUB_TOKEN gh auth token --hostname github.com --user gabemahoney 2>/dev/null)}"; if [ -n "$T" ]; then GH_TOKEN="$T" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core; else echo "no token in env, /etc/environment or gh"; fi; unset T
   ```
3. Only if all three find nothing, ask the human to sign in: type
   `! gh auth login --hostname github.com --git-protocol https --web` and sign in as `gabemahoney`
   (a minute in the browser with a device code). Then run step 2 again.
4. Follow the Bootstrap section of `~/box_admin/box_admin_core/README.md`.
