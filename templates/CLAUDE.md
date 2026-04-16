# CLAUDE.md — Claude Agent Rules

> Agent-specific configuration for Claude (Anthropic).
> **Shared rules are in `AI-AGENTS.md` — read that first. This file only adds Claude-specific behaviour.**

---

## Tool Use and Permissions

- Prefer dedicated tools (Read, Edit, Write, Glob, Grep) over Bash.
- Use Bash only for shell-only operations.
- Never skip pre-commit hooks (`--no-verify`) unless explicitly asked.
- Never force-push without explicit user confirmation.

## Autonomy Rules

- Local, reversible actions (file edits, test runs): proceed freely.
- Hard-to-reverse or externally visible actions (push, PR, deploy): confirm with user first.

## Response Style

- Concise. No trailing summaries of what was just done.
- Code: no comments unless the WHY is non-obvious.
- No emoji unless explicitly requested.
