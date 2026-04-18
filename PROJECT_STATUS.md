# Project Status — Codex Machinae

## Objective
Evolve `codex-machinae.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` (Cortex project) and promoting them into the playbook.

All documentation and commits are in **British English**.

## Current Phase
Design. The repository has been stripped of premature scaffolding (templates, bootstrap scripts, CI). Only the playbook, the reference example, and the multi-agent configuration remain. Tooling will be produced once the playbook design stabilises.

## Modified Files
- `codex-machinae.md` §2: replaced prescriptive mandatory folder tree with "Minimum Core of Existence" + "Emergent Expansion Protocol"; §2.4 now covers both single- and multi-agent configurations.
- `codex-machinae.md` §8: generalised from "Dependency Surface Map" to "Boundary Contracts" (Hardware / UI / Data / API axes, inbound/outbound direction); cross-references swept across §1.8, §2.2, §5, §9, §10, §12, §14, §15, Appendix A, Appendix C.
- `codex-machinae.md` §1.8: split Definition of Done into Core (always applies) and Contextual (applies when precondition holds, recorded as `n/a` otherwise).
- `codex-machinae.md` §12: reframed Remediation as a risk-modulated pattern applicable to any classified change, not only dependency bumps; L0/L1 are now explicitly optional ladder rungs; §12.6 renamed from "Major version protocol" to "Contract-breaking change protocol".

## Logical State
- Playbook: `codex-machinae.md` — §2, §8, §1.8, §12 refactored per the Meta-Framework direction. Remaining prescriptive artefacts: §6 Documentation, §7 CI/CD, §9 Surveillance agents (still framed as mandatory), §13 Compatibility database, §14 Self-testing — all candidates for "optional module" framing.
- Reference example: `example/00-prd.md` (Cortex) — unchanged; source of patterns.
- Roadmap: `STRATEGY_TRANSFORMATION.md` — Phase A points 1, 2, 3, 5 executed. Phase A point 4 (abstract remediation) executed. Phase B (Guest Agent), Phase C (Lessons Learned loop), Phase D (independent versioning) pending.

## Next Action
1. Frame Part II (§§8–14) as the optional "Surveillance module" activated by Emergent Expansion when a project has tracked contracts.
2. Begin Phase C: draft the Lessons Learned Report template and the Promotion protocol (pattern from project → playbook).
3. Absorb `STRATEGY_TRANSFORMATION.md` into the playbook where its ideas have landed, then remove it from the repo.
