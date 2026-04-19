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
- `example/00-prd.md` is read-only. Extract patterns from it and promote them into the playbook; do not edit the example itself.

## Scope Discipline
- Design phase only. Do not reintroduce templates, scripts, CI, or folder scaffolds (`docs/adr/`, `src/`, `tests/`, etc.). Tooling is deferred until the playbook design stabilises.
- Active refactor: if `MODULARISATION_PLAN.md` has an open phase, follow it — read the plan before touching the playbook, respect the Phase 0 human gate, and append to the Progress log when a phase advances.
- End-of-phase alignment: when a phase closes, follow AI-AGENTS.md §Workflow step 6 — update `PROJECT_STATUS.md`, the plan's status header and checkboxes, and verify all tracking files agree on the current phase number before committing.

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
