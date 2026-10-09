# box-admin

The public entry point for Gabe's box setup. The real repo, `gabemahoney/box-admin-core`, is private.

Start plain `claude` (default permission mode, not auto) in any folder, say "clone
github.com/gabemahoney/box-admin into ~/projects/box-admin and follow it", and approve the setup scripts
when Claude asks. Claude clones the private core repo with the box's GitHub token (or walks you through
a quick gh sign-in) and carries on. Tokens are never printed or pasted into a chat. A checkout of this
repo that already exists elsewhere is used where it is.

The core and layer checkouts go in `~/projects/box_admin`. To put them elsewhere, export
`BOX_ADMIN_ROOT=<absolute dir>` in the shell before starting `claude`.
