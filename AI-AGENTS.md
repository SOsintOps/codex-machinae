# AI-AGENTS.md — Shared Agent Configuration

> **Source of truth for all AI agents working on this project.**
> All agent-specific files (`CLAUDE.md`, `GEMINI.md`, …) MUST align with this document.
> When a rule here conflicts with an agent-specific file, this file wins.

---

## Multi-Agent Alignment Protocol

This project is worked on by multiple AI agents (Claude, Gemini, and others) across separate sessions.
Each agent has its own config file for agent-specific syntax and tooling.
All shared rules live here. Agent-specific files must not contradict this document.

**When updating rules:**
1. Update `AI-AGENTS.md` first.
2. Propagate the change to every agent-specific file.
3. Commit all files in the same commit: `chore(agents): sync AI-AGENTS.md to all agent configs`.

---

## Project Overview

**Name:** Codex Machinae
**Description:** Universal software development playbook under active design. The repo contains the playbook itself and a reference example (`example/00-prd.md`) used to derive general patterns.

**Current scope:** design only. No templates, scaffolds, scripts, or CI until the playbook design stabilises.

**Active refactor:** `MODULARISATION_PLAN.md` is the durable source of truth for the ongoing split of the playbook into Core + Domain Appendices (D1–D7) + Cross-cutting Modules (M1–M4). Any agent resuming work on the playbook structure MUST read this file first, respect its phased execution, and append to its Progress log at the end of each session. The plan may pause mid-phase across sessions — resume from the first unchecked step in the current phase.

---

## Language and Style

- **Working Language:** The official written working language for all project documentation, commits, and agent outputs is **British English**.
- **Tone:** Professional, technical, concise.
- **Technical terms:** Standard industry English.

## Naming Conventions

- **Files:** kebab-case (e.g. `new-section.md`).
- **Commits:** Conventional Commits (e.g. `feat(docs): add section on agentic loops`).
- **Branches:** `<type>/<id>-<description>` (e.g. `feat/US-DOC-001-setup`).

## Protected Paths

- `codex-machinae.md` core sections §1, §8, §9 — no changes without prior human confirmation or an Issue/PR.
- Severity and autonomy parameters §10, §12 — no changes unless explicitly requested to evolve the system.
- `example/00-prd.md` — read-only reference. Do not modify; patterns are extracted from it and promoted into the playbook.

## Workflow (all agents)

1. Read `PROJECT_STATUS.md` to understand current context before acting.
2. If `MODULARISATION_PLAN.md` exists and its Progress log shows the refactor is open, treat it as the active work plan: read it end-to-end before touching the playbook, and honour Phase 0 gates before moving any content.
3. Plan before acting on any non-trivial change.
4. Apply changes surgically; do not refactor beyond the task scope.
5. Update `PROJECT_STATUS.md` at the end of each session; if a modularisation phase advanced, also append to the Progress log in `MODULARISATION_PLAN.md`.
6. **End-of-phase alignment (mandatory when a phase closes).** Before committing the phase-close:
   (a) update `PROJECT_STATUS.md` — current phase, modified-files list, next action;
   (b) update the `MODULARISATION_PLAN.md` status header and tick the phase's checkboxes;
   (c) verify that all tracking files (`PROJECT_STATUS.md`, `MODULARISATION_PLAN.md` header,
       `MODULARISATION_PLAN.md` Progress log) agree on the current phase number;
   (d) commit all tracking-file updates in the same commit as the phase-close or immediately after.
7. Commit with Conventional Commits.

## Editorial Rules

- Maximum line length: 120 characters.
- Always use first-level headings for each main document.
- Keep cross-references (§...) up to date.

## Out of Scope (for this phase)

Tooling artefacts — templates, bootstrap scripts, CI workflows, release automation — are explicitly deferred. They will be produced once the playbook design is stable. Do not reintroduce them pre-emptively.

---

## Agent-Specific Files

| File | Agent | Notes |
|------|-------|-------|
| `CLAUDE.md` | Claude (Anthropic) | Tool use, hooks, permission model |
| `GEMINI.md` | Gemini CLI (Google) | Gemini-specific tooling and workflow |

<!-- Add a row whenever a new agent is introduced to the project. -->
