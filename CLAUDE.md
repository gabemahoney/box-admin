# Instructions for Claude

This repo is only the entry point for Gabe's box setup. The real repo,
`gabemahoney/box-admin-core`, is private.

1. Clone it with the personal token, without printing it:
   `GH_TOKEN="$GH_TOKEN_PERSONAL" gh repo clone gabemahoney/box-admin-core ~/box_admin/box_admin_core`
2. If `GH_TOKEN_PERSONAL` is unset, this box type delivers it elsewhere. Check by name only
   (`compgen -e | grep -x GH_TOKEN_PERSONAL`), then ask the human. Never ask for the token in chat.
3. Follow the Bootstrap section of `~/box_admin/box_admin_core/README.md`.

Never print, echo or log any token.
