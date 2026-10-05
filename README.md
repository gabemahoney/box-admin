# box-admin

The public entry point for Gabe's box setup. The real repo,
`gabemahoney/box-admin-core`, is private.

To set up a box, clone it with the personal GitHub token and follow its README:

    GH_TOKEN="$GH_TOKEN_PERSONAL" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core

If `GH_TOKEN_PERSONAL` is unset, see CLAUDE.md for the fallback. Then follow the Bootstrap section of `~/box_admin/box_admin_core/README.md`.
Never print, echo or log any token.
