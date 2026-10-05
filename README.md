# box-admin

The public entry point for Gabe's box setup. The real repo, `gabemahoney/box-admin-core`, is private.

Clone this repo (or `git pull` it), start Claude Code in it, and ask it to follow this repo. Claude
finds the personal GitHub token (its environment, the box's environment file, gh's sign-in) or, on a box that
has neither, walks you through a quick gh sign-in. It then clones the private repo and carries on.
Tokens are never printed or pasted into a chat.
