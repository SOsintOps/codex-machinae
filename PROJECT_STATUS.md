# Project Status — Codex Machinae

## Objective
Evolve `codex-machinae.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` (Cortex project) and promoting them into the playbook.

All documentation and commits are in **British English**.

## Current Phase
Tooling specifications added. Appendix D defines contracts for three reference tools
(AST Walker, Coverage Ratchet, Surveillance Agent Scaffold) — spec-only, no
implementations. Known Limitations updated to point to Appendix D.

## Modified Files (cumulative, current state)
- `codex-machinae.md`: Core + Modules + Domains + Phase C hardening + Phase R (§11.6) +
  Multi-agent (§12.7) + Tooling specs (Appendix D).
- `gemini_revision_260419.md`: Comprehensive senior analyst review + strategic synthesis.
- `MODULARISATION_PLAN.md`: All phases (0–10) closed.
- `README.md`: Minimal redesign (stable design badge).
- `LICENSE`: CC BY 4.0.
- `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: Agent configuration sync.

## Logical State
- Playbook structure: Stable, modular, retrofit-capable, multi-agent-ready, tooling-specified.
- Tooling: Appendix D defines input/output/behaviour contracts for D.1 AST Walker,
  D.2 Coverage Ratchet, D.3 Surveillance Agent Scaffold. Implementations live in
  dedicated repositories, validated against these specs.
- Reference example: `example/00-prd.md` (Cortex) — unchanged; quality benchmark.

## Recent Changelog
- **Appendix D — Tooling Specifications** — three tool contracts: D.1 AST Walker
  (contract-map generator with detection rules, language support, delta mode), D.2
  Coverage Ratchet (CI step with baseline file, escape valves, regression reporting),
  D.3 Surveillance Agent Scaffold (cron-based contract tester with manifest, heartbeat,
  issue-tracker integration).
- **Known Limitations updated** — mechanical barrier mitigation now points to Appendix D.
- **Glossary** — three new entries: AST Walker, Coverage ratchet (tool), Surveillance
  agent scaffold.
- *(Previous: §12.7 Multi-agent, A.9; §11.6 Phase R, A.8, B.9.)*

## Next Action
1. **Project-size profiles —** Introduce solo/small/large gates on Appendix A checklists.
