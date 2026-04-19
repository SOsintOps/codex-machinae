# Project Status — Codex Machinae

## Objective
Evolve `codex-machinae.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` (Cortex project) and promoting them into the playbook.

All documentation and commits are in **British English**.

## Current Phase
Phase R — Retrofit protocol codified. §11.6 added to the lifecycle with five subsections
(debt-scoping audit, retroactive contract mapping, prioritised adoption tiers, module
activation, lifecycle entry). Supporting artefacts: A.8 Phase R checklist, B.9 Retrofit
Audit template, four glossary entries.

## Modified Files (cumulative, current state)
- `codex-machinae.md`: Core + Modules + Domains + Phase C hardening + Phase R (§11.6,
  A.8, B.9, glossary entries).
- `gemini_revision_260419.md`: Comprehensive senior analyst review + strategic synthesis.
- `MODULARISATION_PLAN.md`: All phases (0–10) closed.
- `README.md`: Minimal redesign (stable design badge).
- `LICENSE`: CC BY 4.0.
- `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: Agent configuration sync.

## Logical State
- Playbook structure: Stable, modular, and retrofit-capable.
- Retrofit path: §11.6 provides a complete convergence protocol for existing projects,
  addressing the critical gap identified in the Claude-Gemini review.
- Reference example: `example/00-prd.md` (Cortex) — unchanged; quality benchmark.

## Phase R Changelog
- **§11.6 Phase R — Retrofit** — five subsections: debt-scoping audit (§11.6.1),
  retroactive contract mapping (§11.6.2), prioritised adoption plan with T1/T2/T3 tiers
  (§11.6.3), module activation (§11.6.4), lifecycle entry (§11.6.5).
- **A.8 Phase R checklist** — structured checklist covering all five retrofit stages.
- **B.9 Retrofit Audit template** — ready-to-use `RETROFIT_AUDIT.md` with gap assessment
  table, contract map summary, module activation register, and adoption plan scaffold.
- **Glossary** — four new entries: Phase R (Retrofit), Retrofit audit, Debt-scoping,
  Adoption tier.

## Next Action
1. **Multi-Agent Protocol (§12.3) —** Define optional rules for collaborative AI
   environments (analyst's prerogative whether to activate).
2. **Tooling phase —** Develop reference implementations (AST Walker, coverage-ratchet CI step).
3. **Project-size profiles —** Introduce solo/small/large gates on Appendix A checklists.
