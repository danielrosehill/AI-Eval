# Private overlay

This plugin is generic. Anything specific to one person (GitHub owner, where evals live,
which indexes to update, how secrets reach a command) goes in a private overlay directory
that the plugin reads at run time. Nothing in the overlay is ever committed here.

## Resolving the directory

First match wins:

1. `$AI_EVAL_DATA`
2. `$CLAUDE_USER_DATA/ai-eval`
3. `~/.claude-user-data/ai-eval`

## Files

Lookup is overlay first, then built-in. An overlay file overrides this plugin where
they conflict. All files are optional.

| File | Holds |
|---|---|
| `conventions.md` | `<owner>`, `<evals-dir>`, how to run a command with API keys in its environment, where to look for existing plans, blog and collection hand-offs, and any spend rules stricter than the defaults |
| `register.md` | The indexes `register-eval` keeps up to date, and how to edit each |

Read `conventions.md` before any skill that creates a repo, spends money or publishes.
