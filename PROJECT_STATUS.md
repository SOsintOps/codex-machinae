# Project Status — dev_playbook

## Objective
Evolve `software-development-playbook.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` (Cortex project) and promoting them into the playbook.

All documentation and commits are in **British English**.

## Current Phase
Design. The repository has been stripped of premature scaffolding (templates, bootstrap scripts, CI). Only the playbook, the reference example, and the multi-agent configuration remain. Tooling will be produced once the playbook design stabilises.

## Modified Files
- `software-development-playbook.md` §2: replaced prescriptive mandatory folder tree with "Minimum Core of Existence" + "Emergent Expansion Protocol"; §2.4 now covers both single- and multi-agent configurations.

## Logical State
- Playbook: `software-development-playbook.md` v2.0.0 Draft — prescriptive, to be refactored per the Meta-Framework direction.
- Reference example: `example/00-prd.md` (Cortex) — unchanged; source of patterns.
- Roadmap: `STRATEGY_TRANSFORMATION.md` — design notes guiding the refactor; to be absorbed into the playbook and removed.

## Next Action
Continue Phase A of the Meta-Framework refactor:
1. Generalise §8 "Dependency Surface Map" into abstract "Boundary Contracts" (Hardware, UI, Data, API) — requires human confirmation (§8 is a protected section).
2. Split §1.8 Definition of Done into **Core DoD** (process integrity) and **Contextual DoD** (project goals) — requires human confirmation (§1 is a protected section).
3. Recast §12 Remediation (L0-L2) as a pattern applicable by risk rather than a per-dependency requirement.
