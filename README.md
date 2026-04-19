# Codex Machinae

```
   ██████╗ ██████╗ ██████╗ ███████╗██╗  ██╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝╚██╗██╔╝
  ██║     ██║   ██║██║  ██║█████╗   ╚███╔╝
  ██║     ██║   ██║██║  ██║██╔══╝   ██╔██╗
  ╚██████╗╚██████╔╝██████╔╝███████╗██╔╝ ██╗
   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
        M   A   C   H   I   N   A   E
    · universal llm-assisted playbook ·
```

<p align="center">

[![Licence: CC BY 4.0](https://img.shields.io/badge/licence-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status: stable design](https://img.shields.io/badge/status-stable%20design-brightgreen.svg)](#)
[![Language: en-GB](https://img.shields.io/badge/language-en--GB-blue.svg)](#)
[![Playbook: ~3 100 lines](https://img.shields.io/badge/playbook-~3%20100%20lines-informational.svg)](#)

</p>

> **Universal, modular meta-framework for shipping software with LLM collaborators.**
> A sober Core plus domain appendices and cross-cutting modules — activated by trigger,
> never by default.

---

## What is Codex Machinae?

Codex Machinae is an opinionated playbook that defines **how** a software project should
be structured, developed, tested, and maintained when one or more AI agents collaborate
with human developers. It is not a template generator or a CLI tool — it is a
**process specification** that any team (or solo developer) can adopt.

Key design principles:

- **Emergent Expansion** (§2.2) — no folder, no module, no process exists until a
  trigger fires. Anti-scaffolding by design.
- **Boundary Contracts** (§8) — every integration point (API, data, UI, hardware) is
  catalogued, classified, and monitored.
- **Risk-modulated remediation** (§10) — fixes are classified by autonomy level
  (L0 human-only, L1 agent-assisted, L2 fully automated) based on blast radius.
- **Profile-aware** (§2.5) — Solo, Small, and Large project profiles modulate checklist
  density so compliance cost scales with project risk.

---

## Architecture

```
codex-machinae.md
│
├── Part I — Core (universal, applies to every project)
│   ├── §1   Requirements and planning
│   ├── §2   Project structure + Emergent Expansion + Profiles
│   ├── §3   Code quality
│   ├── §4   Security fundamentals
│   ├── §5   Testing strategy
│   ├── §6   Documentation
│   ├── §7   CI/CD and deployment
│   ├── §8   Boundary Contracts
│   ├── §9   Change classification
│   ├── §10  Remediation workflow
│   ├── §11  Project lifecycle (incl. Phase R — Retrofit)
│   └── §12  Conventions for AI agents (incl. Multi-agent)
│
├── Part II — Domain Appendices (activate per project type)
│   ├── D1  Web Service          ████████████  full
│   ├── D2  Library / SDK        ░░░░░░░░░░░░  stub
│   ├── D3  CLI Tool             ░░░░░░░░░░░░  stub
│   ├── D4  Embedded / Firmware  ████████████  full
│   ├── D5  ML / Data Pipeline   ████████████  full
│   ├── D6  Mobile App           ░░░░░░░░░░░░  stub
│   └── D7  Static Site          ░░░░░░░░░░░░  stub
│
├── Part III — Cross-cutting Modules (activate by trigger)
│   ├── M1  Surveillance         ████████████  full
│   ├── M2  Security-sensitive   ████████████  full
│   ├── M3  Release & Distrib.   ░░░░░░░░░░░░  stub
│   └── M4  Classification       ████████████  full
│
└── Appendices
    ├── A — Phase checklists (profile-aware)
    ├── B — Templates (PRD, ADR, stories, contract map, retrofit audit)
    ├── C — Glossary
    └── D — Tooling Specifications (AST Walker, Coverage Ratchet, Surveillance Agent)
```

---

## Quick start

### New project (greenfield)

1. Copy `codex-machinae.md` into your repository.
2. Declare a project-size profile in your agent config: `Solo`, `Small`, or `Large` (§2.5).
3. Follow **Phase 0** (§11.1) — write the PRD, define user stories, set the Definition of Done.
4. Follow **Phase 1** (§11.2) — bootstrap the directory structure, CI, and contract map.
5. Activate domain appendices and modules as their triggers fire (§2.2).

### Existing project (retrofit)

1. Copy `codex-machinae.md` into your repository.
2. Follow **Phase R** (§11.6) — the retrofit protocol:
   - **Debt-scoping audit** — assess the gap between your project and the playbook.
   - **Retroactive contract mapping** — generate the Boundary Contract Map from existing code.
   - **Prioritised adoption** — work in tiers: T1 safety net, T2 structure, T3 process.
3. Enter the normal lifecycle at Phase 2 (active development) or Phase 3 (maintenance).

Use the `RETROFIT_AUDIT.md` template (Appendix B.9) to structure the assessment.

---

## Repository structure

| File | Description |
|------|-------------|
| [`codex-machinae.md`](codex-machinae.md) | The playbook — Core + Domain Appendices + Modules + Appendices (~3 100 lines) |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Current project state, updated every session |
| [`MODULARISATION_PLAN.md`](MODULARISATION_PLAN.md) | Historical record of the modularisation refactor (Phases 0–10, closed) |
| [`gemini_revision_260419.md`](gemini_revision_260419.md) | Cross-evaluation: Gemini senior review + Claude counter-evaluation + strategic synthesis |
| [`AI-AGENTS.md`](AI-AGENTS.md) | Shared agent rules (source of truth for all LLMs) |
| [`CLAUDE.md`](CLAUDE.md) | Claude-specific agent configuration |
| [`GEMINI.md`](GEMINI.md) | Gemini-specific agent configuration |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution guidelines |
| [`LICENSE`](LICENSE) | CC BY 4.0 full text |

---

## AI collaboration model

This playbook is designed and maintained by human analysts with AI agent assistance.
Multiple LLMs collaborate across sessions under §12 rules:

- **`AI-AGENTS.md`** — shared source of truth for all agents.
- **`CLAUDE.md`**, **`GEMINI.md`** — provider-specific rules.
- **§12.7** — optional multi-agent coordination protocol (lead designation, scope
  partitioning, conflict prevention). Activated at the analyst's discretion.

Every agent reads `PROJECT_STATUS.md` at session start and updates it at session end.

---

## Roadmap

| Priority | Item | Status |
|----------|------|--------|
| 1 | First downstream retrofit on a real project | Planned |
| 2 | Fill D2 (Library/SDK) and D3 (CLI Tool) stubs | Planned |
| 3 | Build reference implementations against Appendix D specs | Planned |
| 4 | Fill D6 (Mobile), D7 (Static Site), M3 (Release) stubs | Backlog |

---

## Licence

This work is licensed under the
[Creative Commons Attribution 4.0 International Licence](https://creativecommons.org/licenses/by/4.0/)
(CC BY 4.0). See [`LICENSE`](LICENSE) for the full text.

You are free to share and adapt this material for any purpose, including commercial,
as long as you give appropriate credit.
