# Project Status — Codex Machinae

## Objective
Evolve `codex-machinae.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` (Cortex project) and promoting them into the playbook.

All documentation and commits are in **British English**.

## Current Phase
Multi-agent coordination protocol added. §12.7 codifies optional rules for multi-agent
and mixed-LLM collaboration: lead designation, scope partitioning, conflict prevention,
shared artefacts protocol, inter-agent handover, and mixed-LLM considerations.

## Modified Files (cumulative, current state)
- `codex-machinae.md`: Core + Modules + Domains + Phase C hardening + Phase R (§11.6) +
  Multi-agent (§12.7, A.9, glossary entries).
- `gemini_revision_260419.md`: Comprehensive senior analyst review + strategic synthesis.
- `MODULARISATION_PLAN.md`: All phases (0–10) closed.
- `README.md`: Minimal redesign (stable design badge).
- `LICENSE`: CC BY 4.0.
- `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: Agent configuration sync.

## Logical State
- Playbook structure: Stable, modular, retrofit-capable, multi-agent-ready.
- Multi-agent: §12.7 is optional (analyst's prerogative). Covers both multi-instance
  (same LLM) and mixed-LLM (different providers) scenarios. All coordination happens
  through committed artefacts, never implicit state.
- Reference example: `example/00-prd.md` (Cortex) — unchanged; quality benchmark.

## Recent Changelog
- **§12.7 Multi-agent coordination** — six subsections: lead agent designation (§12.7.1),
  scope partitioning (§12.7.2), conflict prevention (§12.7.3), shared artefacts protocol
  (§12.7.4), inter-agent handover (§12.7.5), mixed-LLM considerations (§12.7.6).
- **A.9 Multi-agent setup checklist** — covers designation, partitioning, write-access,
  mixed-LLM consistency, and operational readiness.
- **Glossary** — three new entries: Lead agent, Scope partition, Inter-agent handover.
- *(Previous: §11.6 Phase R Retrofit, A.8, B.9, four glossary entries.)*

## Next Action
1. **Tooling phase —** Develop reference implementations (AST Walker, coverage-ratchet CI step).
2. **Project-size profiles —** Introduce solo/small/large gates on Appendix A checklists.
