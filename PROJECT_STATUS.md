# Project Status — Codex Machinae

## Objective
Evolve `codex-machinae.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` (Cortex project) and promoting them into the playbook.

All documentation and commits are in **British English**.

## Current Phase
Design — modularisation in flight. The playbook is being split into Core + Domain Appendices
(D1–D7) + Cross-cutting Modules (M1–M4), per `MODULARISATION_PLAN.md`. Phases 0–7 closed.
Phase 8 (module and domain content, MVP set) pending scope clarification. Tooling (templates,
bootstrap scripts, CI) remains deferred until the design stabilises.

## Modified Files (cumulative, current state)
- `codex-machinae.md`:
  - §2: Minimum Core of Existence + Emergent Expansion Protocol.
  - §1.8: Definition of Done split into Core + Contextual.
  - §4 Security: slimmed to §4.1 principles, §4.2 input validation, §4.3 secrets.
  - §5 Testing: §§5.1–5.8 universal; §5.9 Golden queries extracted to D5.1.
  - §6 Documentation: §§6.1–6.3 universal (REST/SDK/CLI rows moved to D1.1/D2.1/D3.1).
  - §7 CI/CD: §§7.1–7.5 universalised (pipeline diagram, rollback table generalised).
  - §8: Boundary Contracts (Hardware/UI/Data/API, inbound/outbound).
  - §9: Change classification.
  - §10: Remediation workflow (risk-modulated).
  - §11: Lifecycle rewritten as "Core steps + activation blocks" pattern (M1/D1/D2/D3/M2).
  - §12: Autonomy rules.
  - Part II — Domain Appendices:
    - D1 Web Service: D1.1 API doc, D1.2 deploy strategy, D1.3 environments populated.
    - D2 SDK: D2.1 API doc row populated.
    - D3 CLI: D3.1 API doc row populated.
    - D5 ML / Data Pipeline: D5.1 golden queries, D5.2 irreversible-migration rule populated.
    - D4, D6, D7: scaffolds (trigger + placeholders).
  - Part III — Cross-cutting Modules:
    - M1 Surveillance: fully populated from former §§9, 11, 13, 14.
    - M2 Security-sensitive: M2.1 auth, M2.2 PR checklist, M2.3 OWASP Top 10 populated.
    - M3, M4: scaffolds.
- `MODULARISATION_PLAN.md`: durable plan; Phases 0–7 closed (progress log up to date).
- `README.md`: minimal redesign (H1 + ASCII banner + 3 badges + CAUTION + TL;DR).
- `LICENSE`: CC BY 4.0 (official legal text).
- `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: point agents at the plan on resume.

## Logical State
- Playbook structure: Core §§1–12 contiguous; Part II partial (D1/D2/D3/D5 populated, rest scaffolds);
  Part III partial (M1 live, M2 populated, M3/M4 scaffolds).
- Reference example: `example/00-prd.md` (Cortex) — unchanged; inspiration / quality benchmark.
- Roadmap: `STRATEGY_TRANSFORMATION.md` — to be absorbed in Phase 10.

## Next Action
1. **Phase 8 — Module and domain content (MVP set)**: populate D1 Web Service, D4 Embedded,
   D5 ML / Data Pipeline; polish M1 Surveillance; polish M2 Security-sensitive; populate M4
   Classification & Taxonomy; add stubs for D2, D3, D6, D7, M3. Scope and Cortex-driven
   benchmark approach pending user confirmation.
2. **Phase 9 — Appendices A/B/C reorganisation** per `MODULARISATION_PLAN.md`.
3. **Phase 10 — Final verification**: absorb `STRATEGY_TRANSFORMATION.md`, update this file,
   mark plan complete, remove WIP notice from README.
4. Phase C (Lessons Learned Report + Promotion protocol) — deferred until modularisation lands,
   then slot in as a new Core section.
