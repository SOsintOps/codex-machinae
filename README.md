# Codex Machinae

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│            ▄████▄   ▒█████  ▓█████▄ ▓█████ ▒██   ██▒         │
│           ▒██▀ ▀█  ▒██▒  ██▒▒██▀ ██▌▓█   ▀ ▒▒ █ █ ▒░         │
│           ▒▓█    ▄ ▒██░  ██▒░██   █▌▒███   ░░  █   ░         │
│           ▒▓▓▄ ▄██▒▒██   ██░░▓█▄   ▌▒▓█  ▄  ░ █ █ ▒          │
│           ▒ ▓███▀ ░░ ████▓▒░░▒████▓ ░▒████▒▒██▒ ▒██▒         │
│                                                              │
│         ▀▀▀▀▀▀▀▀▀▀▀▀  M A C H I N A E  ▀▀▀▀▀▀▀▀▀▀▀▀          │
│                                                              │
│            ·  universal llm-assisted playbook  ·             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

[![Licence: CC BY 4.0](https://img.shields.io/badge/licence-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status: stable design](https://img.shields.io/badge/status-stable%20design-brightgreen.svg)](#)
[![Language: en-GB](https://img.shields.io/badge/language-en--GB-blue.svg)](#)

**TL;DR** — Universal, modular playbook for shipping software with LLM collaborators: a sober Core plus domain appendices and cross-cutting modules, activated by trigger.

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

## Licence

This work is licensed under the [Creative Commons Attribution 4.0 International Licence](https://creativecommons.org/licenses/by/4.0/) (CC BY 4.0). See [`LICENSE`](LICENSE) for the full text.
