# box-admin

The public entry point for Gabe's box setup. The real repo, `gabemahoney/box-admin-core`, is private.

Start plain `claude` (default permission mode, not auto) in any folder, say "clone
github.com/gabemahoney/box-admin into ~/projects/box-admin and follow it; layer `<layer repo URL>` with
`<VAR>=<login>`", and approve the setup scripts when Claude asks. Copy the layer part from the start line
in the README of your box type's layer repo; without it, Claude asks for it. Claude clones the private
core repo with the box's GitHub token (or walks you through a quick gh sign-in), bootstraps that layer and
carries on. If the bootstrap fails, Claude shows what it printed and stops. Tokens are never printed or
pasted into a chat. A checkout of this repo that already exists elsewhere is used where it is.

That start line is enough: if the layer has no `SKILL.md` or no `hosts/<host>/`, Claude opens a
read-only intake PR, polls it and the layer every few minutes, answers comments and reviews the owner's
setup PR. When that PR merges to the layer's `main`, Claude pulls and reruns setup_box from the top.
At human-only steps (tokens, AD migration, Slack credentials and Claude sign-in), it gives exact commands
with hidden `read -rs` prompts for secrets, waits, then carries on. It reports on the PR until setup runs clean.

The core and layer checkouts go in `~/projects/sysadmin-project/box_admin_dev`. To put them elsewhere,
export `BOX_ADMIN_ROOT=<absolute dir>` in the shell before starting `claude`.
