# Codex Machinae

Universal software development framework for LLM-assisted projects.

**Working Language:** All documentation, commits, and agent outputs are in **British English**.

---

## Scope

This repository holds two artefacts:

1. `codex-machinae.md` — the playbook under active design.
2. `example/00-prd.md` — the reference project (Cortex PRD) used as the concrete source from which general patterns are extracted and promoted into the playbook.

Everything else in this repo is working configuration for the agents that collaborate on the design.

## Collaborators

Multiple LLMs work on this project across separate sessions. Each has a dedicated config file:

- `AI-AGENTS.md` — shared rules (source of truth).
- `CLAUDE.md` — Claude-specific rules.
- `GEMINI.md` — Gemini-specific rules.

New agents are added by creating an agent-specific file that aligns with `AI-AGENTS.md`.

## Working loop

1. Read `PROJECT_STATUS.md` to pick up context.
2. Evolve the playbook, informed by the example.
3. Update `PROJECT_STATUS.md` at the end of the session.
4. Commit with Conventional Commits.

Tooling (templates, bootstrap scripts, CI) will be produced **after** the playbook design stabilises, not before.
