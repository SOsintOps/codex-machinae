# Project Status — Codex Machinae

## Objective
Evolve `codex-machinae.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` (Cortex project) and promoting them into the playbook.

All documentation and commits are in **British English**.

## Current Phase
Phase C — Hardening. Gemini review findings promoted into the playbook. Three structural
improvements applied: Contract Map example (Appendix B.8), Human-Agent Handover protocol
(§10.4), and Known Limitations and Roadmap section.

## Modified Files (cumulative, current state)
- `codex-machinae.md`: Core + Modules + Domains + Phase C hardening (B.8 example, §10.4
  handover, Known Limitations section, TOC updated).
- `gemini_revision_260419.md`: Comprehensive senior analyst review (input to Phase C).
- `MODULARISATION_PLAN.md`: All phases (0–10) closed.
- `README.md`: Minimal redesign (stable design badge).
- `LICENSE`: CC BY 4.0.
- `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: Agent configuration sync.

## Logical State
- Playbook structure: Stable and modular.
- Gemini review: Findings formalised — strengths validated, weaknesses acknowledged in
  "Known limitations and roadmap", two actionable suggestions implemented (Contract Map
  example, Human-Agent Handover).
- Reference example: `example/00-prd.md` (Cortex) — unchanged; quality benchmark.

## Phase C Changelog
- **B.8 Contract Map example** — complete `COMPATIBILITY.md` for a hypothetical web service
  covering all four axes (api, data, ui, hardware=0). Lowers comprehension barrier.
- **§10.4 Human-agent handover** — codified dossier format when circuit breaker trips.
  Reduces human ramp-up time on failed L1 sequences.
- **Known Limitations and Roadmap** — new section before appendices. Acknowledges mechanical
  barrier, stub gaps, checklist density. Each with planned mitigation.
- **§10.5–10.8 renumbered** — subsections after the new §10.4 shifted by one; cross-refs
  updated (§10.6 → §10.7 in two locations).

## Next Action
1. Tooling phase — develop reference implementations (AST Walker, coverage-ratchet CI step,
   surveillance-agent scaffold) to lower the compliance barrier.
2. Fill remaining stubs — prioritise D2 (Library/SDK) and D3 (CLI Tool).
3. Project-size profiles — introduce solo/small/large gates on Appendix A checklists.
