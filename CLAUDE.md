# CLAUDE.md — Claude Agent Rules

> Agent-specific configuration for Claude (Anthropic).
> **Shared rules are in `AI-AGENTS.md` — read that first. This file only adds Claude-specific behaviour.**

**Working Language:** All documentation, comments, and commits MUST be in **British English**.

---

## Naming Conventions (§3.2)
- **Files:** kebab-case (e.g. `new-section.md`).
- **Commits:** Conventional Commits (e.g. `feat(docs): add section on agentic loops`).
- **Branches:** `<type>/<id>-<description>` (e.g. `feat/US-DOC-001-setup`).

## Protected Paths
- Do not modify core playbook sections (§1, §8, §9) without prior human confirmation or an Issue/PR.
- Do not alter severity and autonomy parameters (§10, §12) unless explicitly requested to evolve the system.

## Editorial Rules
- Maximum line length: 120 characters.
- Always use first-level headings for each main document.
- Keep cross-references (§...) up to date.

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
