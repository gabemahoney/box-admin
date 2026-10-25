# box-admin

The public entry point for Gabe's box setup. The real repo, `gabemahoney/box-admin-core`, is private.

Start `claude --permission-mode acceptEdits --allowedTools Bash` (never auto or bypass) in any folder, say "clone
github.com/gabemahoney/box-admin into ~/projects/box-admin and follow it; layer `<layer repo URL>` with
`<VAR>=<login>`", and Claude first writes the permissions block to `~/.claude/settings.json` (approve that once), so nothing else prompts. Copy the layer part from the start line
in the README of your box type's layer repo; without it, Claude asks for it. Claude clones the private
core repo with the box's GitHub token (or walks you through a quick gh sign-in), bootstraps that layer and
carries on. If the bootstrap fails, Claude shows what it printed and stops. Tokens are never printed or
pasted into a chat. A checkout of this repo that already exists elsewhere is used where it is.

That start line is enough: if the layer has no `SKILL.md` or no `hosts/<host>/`, Claude opens a
read-only intake PR, polls it and the layer every few minutes, answers comments and reviews the owner's
setup PR. When that PR merges to the layer's `main`, Claude pulls and reruns setup_box from the top.
At human-only steps (tokens, AD migration, Slack credentials and Claude sign-in), it gives exact commands
with hidden `read -rs` prompts for secrets, waits, then carries on. It reports on the PR until setup runs clean.

On a box no layer fits, say instead "clone github.com/gabemahoney/box-admin into ~/projects/box-admin and
follow it; new layer `<type>` with `GH_TOKEN_WORK=<login>`" (`<type>`: lowercase letters and digits, your
name for the box type; the token pair is optional). Claude checks no layer already matches, asks you to
approve one command that creates the private layer repo `gabemahoney/box-admin-<type>`, then carries on as
above, finishing what it can while you answer the intake PR.

To bring a set-up box current, tell its sysadmin bot "pull box-admin and follow its update instructions".

**Tokens, any login shell (bash or tcsh).** Claude needs `GH_TOKEN_PERSONAL` (and `GH_TOKEN_WORK` if the
layer wants it) in its environment, and a tcsh login shell has no `read` or `export`. Type this one line in
the terminal; it prompts hidden, never echoes, and starts Claude, already permissive, with both set (drop the work half if you
have none):

```sh
bash -c 'set +x; IFS= read -rs -p "GH_TOKEN_PERSONAL: " GH_TOKEN_PERSONAL; echo; IFS= read -rs -p "GH_TOKEN_WORK: " GH_TOKEN_WORK; echo; export GH_TOKEN_PERSONAL GH_TOKEN_WORK; exec claude --permission-mode acceptEdits --allowedTools Bash'
```

The core and layer checkouts go in `~/projects/sysadmin-project/box_admin_dev` (core's standard layout; an older box whose core is only in `~/projects/box_admin` keeps using that). To put them elsewhere, export
`BOX_ADMIN_ROOT=<absolute dir>` in the shell before starting `claude`.
