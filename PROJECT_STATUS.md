# Project Status — Codex Machinae

## Objective
Evolve `codex-machinae.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` (Cortex project) and promoting them into the playbook.

All documentation and commits are in **British English**.

## Current Phase
Design — modularisation in flight. The playbook is being split into Core + Domain Appendices
(D1–D7) + Cross-cutting Modules (M1–M4), per `MODULARISATION_PLAN.md`. Phases 0–9 closed.
Phase 10 (final verification) is next. Tooling (templates, bootstrap scripts, CI) remains
deferred until the design stabilises.

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
    - D1 Web Service: D1.1–D1.6 fully populated (API doc, deploy, environments, request-path
      testing, rate-limiting/back-pressure, observability).
    - D2 SDK: D2.1 API doc + post-MVP stub.
    - D3 CLI: D3.1 API doc + post-MVP stub.
    - D4 Embedded / Firmware: D4.1–D4.6 fully populated (HAL, cross-compilation, HIL testing,
      flash/OTA, power/thermal budgets, bring-up checklist).
    - D5 ML / Data Pipeline: D5.1–D5.6 fully populated (golden queries, DB migration,
      training reproducibility, dataset versioning, drift monitoring, evaluation contracts).
    - D6 Mobile App: stub with post-MVP scope bullets.
    - D7 Static Site: stub with post-MVP scope bullets.
  - Part III — Cross-cutting Modules:
    - M1 Surveillance: fully populated + polished (domain-composition table, compat-db
      directory example, strengthened cardinality guard).
    - M2 Security-sensitive: M2.1–M2.4 populated (auth, PR checklist, OWASP with review
      table, dependency-vulnerability management with SLA).
    - M3 Release & Distribution: stub with post-MVP scope bullets.
    - M4 Classification & Taxonomy: M4.1–M4.8 fully populated (MECE principles, governance,
      scouting protocol, adoption patterns, audits, machine-readable formats, upstream
      contribution, illustrative examples).
- `MODULARISATION_PLAN.md`: durable plan; Phases 0–9 closed (progress log up to date).
- `README.md`: minimal redesign (H1 + ASCII banner + 3 badges + CAUTION + TL;DR).
- `LICENSE`: CC BY 4.0 (official legal text).
- `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: point agents at the plan on resume.

## Logical State
- Playbook structure: Core §§1–12 contiguous; Part II complete for MVP (D1/D4/D5 fully populated,
  D2/D3/D6/D7 stubs with post-MVP scope); Part III complete for MVP (M1/M2/M4 fully populated,
  M3 stub with post-MVP scope).
- Reference example: `example/00-prd.md` (Cortex) — unchanged; inspiration / quality benchmark.
- Roadmap: `STRATEGY_TRANSFORMATION.md` — to be absorbed in Phase 10.

## Next Action
1. **Phase 10 — Final verification**: verify Core numbering, cross-reference sweep, TOC audit,
   absorb `STRATEGY_TRANSFORMATION.md`, update this file, mark plan complete, remove WIP
   notice from README.
2. Phase C (Lessons Learned Report + Promotion protocol) — deferred until modularisation lands,
   then slot in as a new Core section.
