# Project Status — Codex Machinae

## Objective
Evolve `codex-machinae.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` (Cortex project) and promoting them into the playbook.

All documentation and commits are in **British English**.

## Current Phase
Design — modularisation in flight. The playbook is being split into Core + Domain Appendices
(D1–D7) + Cross-cutting Modules (M1–M4), per `MODULARISATION_PLAN.md`. Tooling (templates,
bootstrap scripts, CI) remains deferred until the design stabilises.

## Modified Files (cumulative, current state)
- `codex-machinae.md`:
  - §2: Minimum Core of Existence + Emergent Expansion Protocol.
  - §1.8: Definition of Done split into Core + Contextual.
  - §8: Boundary Contracts (Hardware/UI/Data/API, inbound/outbound); now explicitly scopes
    compatibility testing to M1 rather than implying it is universal.
  - §9 (was §10): Change classification (unchanged content, renumbered).
  - §10 (was §12): Remediation workflow, risk-modulated; §10.3 replaced "agentic loop" with
    "L1 automation"; §10.4 replaced "the classifier detects" with "a change is classified as".
  - §11 (was §15), §12 (was §16): renumbered, content unchanged pending Phase 7 lifecycle
    generalisation.
  - Part II — Domain Appendices (D1–D7): scaffolding present (triggers + placeholders).
  - Part III — Cross-cutting Modules (M1–M4): M1 Surveillance fully populated from former
    §§9, 11, 13, 14; M2/M3/M4 still scaffolds.
- `MODULARISATION_PLAN.md`: durable plan; Phases 0, 1, 2 closed.
- `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: point agents at the plan on resume.

## Logical State
- Playbook structure: Core §§1–12 contiguous; Part II scaffolding; M1 live; M2–M4 scaffolds.
- Reference example: `example/00-prd.md` (Cortex) — unchanged; inspiration / quality benchmark.
- Roadmap: `STRATEGY_TRANSFORMATION.md` — absorbed in Phase 10 of the modularisation plan.

## Next Action
1. **Phase 3 — Security split** (Core §4 ↔ M2): slim §4 to principles + input validation
   concept + secrets; move §4.3 auth, §4.5 PR checklist, §4.6 OWASP into `M2 Security-sensitive`;
   renumber §4 sub-sections contiguously; sweep refs.
2. Subsequent phases per `MODULARISATION_PLAN.md` (4–10).
3. Phase C (Lessons Learned Report + Promotion protocol) — deferred until modularisation lands,
   then slot in as a new Core section.
