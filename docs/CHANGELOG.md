# Changelog

All notable changes to Codex Machinae are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project uses date-based versioning (YYYY-MM-DD) rather than semantic versioning,
as it is a design document, not a software release.

---

## [2026-08-12] — Agent skill: S1 authoring

Phase S1 of `docs/SKILL-ROADMAP.md`. S0 scoping decisions locked in a single
grilling round: name `codex-machinae`, one model-invoked skill with disclosed
reference, living in-repo.

### Added
- **`skills/codex-machinae/SKILL.md`** — the playbook packaged as an agent
  skill: model-facing description with trigger branches; a body (~160 lines)
  carrying the always-apply operating rules, a route-by-situation table, the
  condensed lifecycle (Phases 0–4 and R with completion criteria), the
  classification → autonomy ladder, trigger tables for D1–D7 and M1–M4, and
  a reference index. CC BY attribution line in the footer.
- **`skills/codex-machinae/reference/`** — the skill's disclosed-reference
  tree: 17 byte-for-byte copies of the `playbook/` sources (Core, domains,
  modules, appendices, limitations), excluding monolith-only scaffolding
  (frontmatter, part intros).

### Changed
- **`tools/build.py`** — now generates and `--check`-verifies both artefacts
  (monolith + skill reference tree) from the same `playbook/` sources.
- `README.md` — quick start gains the skill option; repository table and
  roadmap updated (item 5: S1 done).
- `docs/SKILL-ROADMAP.md` — S0 recorded as resolved, S1 marked shipped.

## [2026-08-12] — Wayfinder-derived planning practices and skill roadmap

Practices adapted from the *wayfinder* skill and its sibling skills
(`mattpocock/skills`), reconciled with the playbook's artefacts after a review
of published field feedback on the skill set.

### Added
- **§1.9 Decision mapping (wayfinding)** — trigger-based protocol for the gap
  Phase 0 used to assume away: when an effort exceeds one agent session and
  open decisions still block the PRD, chart them as a decision map (tracker
  issue or `docs/decisions/MAP.md`) and resolve decision tickets one per
  session until the way is clear. Covers ticket types (research / prototype /
  grilling / task, HITL vs AFK), frontier and claim-by-assignee, fog of war
  with graduation, out-of-scope semantics, the plan-don't-do rule, and the
  grilling round protocol. Exit collapses the map into PRD, ADRs, and stories.
- **§11.1 step 0** — Phase 0 now enters through decision mapping when the §1.9
  trigger fires.
- **§12.7.2 "By decision ticket"** — fourth scope-partitioning strategy:
  dynamic claim-based partitioning for parallel sessions working one map.
- **§10.7 expand–contract** — sequencing rule for wide mechanical refactors
  whose blast radius defeats vertical slicing.
- **Appendix B.10 / B.11** — Decision Map and decision ticket templates.
- **Appendix A.1** — conditional checklist block for efforts that triggered
  decision mapping.
- **Appendix C** — glossary entries: decision map, decision ticket, frontier,
  fog of war, graduation, HITL/AFK, grilling, vertical slice, expand–contract.
- **`docs/SKILL-ROADMAP.md`** — roadmap for packaging the playbook as an
  agent skill (authoring, setup skill, distribution, validation).

### Changed
- **§1.3 User story** — two slicing rules added: vertical slice (the
  "what can be demoed" test) and session sizing for agent-executed stories.
- **§1.4 Acceptance criteria** — criteria must be falsifiable at the starting
  commit; three non-grading shapes named and banned.
- **§1.5 ADR** — "significant" now defined by a three-part bar (hard to
  reverse, surprising without context, real trade-off), curbing ADR inflation.
- `README.md` — line-count badge updated (~3 800 → ~3 900); Appendix B
  description and repository/roadmap tables extended.

## [2026-06-10] — GSD comparison and integration guide

### Added
- `docs/GSD-COMPARISON.md` — comparative analysis of Codex Machinae and the
  GSD workflow engine: nature, lifecycle coverage, risk models, where they
  overlap, where they diverge, and how they compose.
- `docs/GSD-INTEGRATION.md` — operational guide to running the playbook under
  GSD: division of authority, agent-config wiring, lifecycle and artefact
  mapping, gate wiring, autonomy governance via §9–§10, retrofit and
  post-milestone handover.
- `docs/FAQ.md` — new entry on combining the playbook with workflow engines.

### Fixed
- `README.md` — the autonomy-level summary had L0 and L2 inverted
  ("L0 human-only … L2 fully automated"); corrected to match §10.1
  (L0 auto-merge, L1 agent-assisted with human review, L2 human-led).

## [2026-06-10] — Physical modularisation and repository hygiene

### Added
- **`playbook/` source tree** — the playbook is now maintained as modular sources:
  frontmatter, Core, the seven domain appendices, the four cross-cutting modules,
  known limitations, and the four appendices, one file each. Adopters can copy the
  whole directory and load only the files whose triggers fire (§2.2), instead of
  carrying the full monolith into every agent session.
- **`tools/build.py`** — assembles `codex-machinae.md` from the `playbook/` sources
  by byte-for-byte concatenation; `--check` mode verifies monolith and sources are
  in sync (intended as a CI gate).

### Changed
- `codex-machinae.md` is now a **generated artefact** — edit the `playbook/`
  sources and rebuild; an assembly notice in the frontmatter says so.
- `README.md` — playbook line-count badge and repository table corrected
  (~3 100 → ~3 800 lines, actual count 3 769).
- This changelog backfilled with the 2026-04-19 repository reorganisation entry,
  which had been omitted at the time.

### Errata
- Commit `b109771` (2026-04-23) carries the message "add password-protected
  iban-redactor archive and update .gitignore", but no archive was ever added:
  the commit only extended `.gitignore` with a review-artifact pattern. The
  history is not rewritten; this note serves as the correction of record.

## [2026-04-19] — Repository reorganisation (backfilled 2026-06-10)

### Added
- `docs/FAQ.md` — inspirations, framework references, and common questions.
- `docs/SECURITY.md` — vulnerability reporting policy.

### Changed
- Service documents (`CHANGELOG.md`, `CONTRIBUTING.md`, `MODULARISATION_PLAN.md`)
  moved into `docs/`.
- `.gitignore` extended: agent configuration files, `PROJECT_STATUS.md`, and
  cross-AI review artifacts are now excluded from tracking.

## [2026-04-19] — Post-modularisation evolution

### Added
- **§2.5 Project-size profiles** — Solo/Small/Large declaration that modulates Appendix A
  checklist items as mandatory, recommended, or optional.
- **§11.6 Phase R — Retrofit** — convergence protocol for adopting the playbook on
  existing projects: debt-scoping audit, retroactive contract mapping, prioritised
  adoption tiers (T1/T2/T3), module activation, lifecycle entry.
- **§12.7 Multi-agent coordination** — optional protocol for multi-agent and mixed-LLM
  collaboration: lead designation, scope partitioning, conflict prevention, shared
  artefacts protocol, inter-agent handover.
- **Appendix D — Tooling Specifications** — contracts for three reference tools:
  D.1 AST Walker (contract-map generator), D.2 Coverage Ratchet (CI step),
  D.3 Surveillance Agent Scaffold (cron-based contract tester).
- **A.8 Phase R checklist** — structured checklist covering all retrofit stages.
- **A.9 Multi-agent setup checklist** — covers designation, partitioning, and operations.
- **B.9 Retrofit Audit template** — ready-to-use `RETROFIT_AUDIT.md`.
- Appendix A items tagged with profile downgrade markers where applicable.
- Glossary entries: Phase R, Retrofit audit, Debt-scoping, Adoption tier, Lead agent,
  Scope partition, Inter-agent handover, Project-size profile, AST Walker,
  Coverage ratchet (tool), Surveillance agent scaffold.

### Changed
- **Known Limitations and Roadmap** — all three mitigations now concrete: mechanical
  barrier → Appendix D, checklist density → §2.5, incomplete domains → planned D2/D3.
- `README.md` redesigned with architecture diagram, quick start, and repository
  structure table.

## [2026-04-19] — Phase C hardening

### Added
- **B.8 Contract Map example** — complete `COMPATIBILITY.md` for a hypothetical web
  service covering all four axes (api, data, ui, hardware).
- **§10.4 Human-agent handover** — codified dossier format when circuit breaker trips.
- **Known Limitations and Roadmap** — new section acknowledging mechanical barrier,
  stub gaps, and checklist density.
- `gemini_revision_260419.md` — cross-evaluation: Gemini senior review, Claude
  counter-evaluation, Gemini strategic synthesis.

### Changed
- §10.5–10.8 renumbered after §10.4 insertion; cross-references updated.

## [2026-04-19] — Modularisation complete (Phases 0–10)

### Added
- **Part II — Domain Appendices** (D1–D7): D1 Web Service, D4 Embedded/Firmware,
  D5 ML/Data Pipeline fully populated; D2, D3, D6, D7 as stubs.
- **Part III — Cross-cutting Modules** (M1–M4): M1 Surveillance, M2 Security-sensitive,
  M4 Classification & Taxonomy fully populated; M3 as stub.
- **Appendix A** split into Core + conditional blocks per module/domain.
- **Appendix B** expanded: B.5 Compatibility record, B.6 OWASP review, B.7 Taxonomy term.
- **Appendix C** glossary extended with 12+ new terms.
- `MODULARISATION_PLAN.md` — complete plan with decisions log, progress log, and
  resumption protocol.

### Changed
- Core renumbered to contiguous §§1–12 after extraction of surveillance (§§9, 11, 13, 14),
  security (§§4.3, 4.5, 4.6), testing (§5.9), documentation (§6.3), and CI/CD
  (§§7.2, 7.4, 7.5) content into modules and domain appendices.
- §11 Project lifecycle rewritten with "Core steps + activation blocks" pattern.
- All cross-references swept and verified.

### Removed
- `STRATEGY_TRANSFORMATION.md` — fully absorbed into the playbook.
- Part II (Surveillance) and Part III (Management) flat headers — replaced by the new
  three-part architecture.

## [2026-04-18] — Pre-modularisation refactors

### Changed
- §2 recast as emergent architecture with anti-scaffolding protocol.
- §8 generalised from compatibility testing to Boundary Contracts (4-axis taxonomy).
- §1.8 Definition of Done split into Core and Contextual.
- §12 Remediation reframed as risk-modulated pattern (L0/L1/L2).
- Project rebranded from "development playbook" to **Codex Machinae**.

## [2026-04-16] — Initial release

### Added
- `codex-machinae.md` — initial playbook (monolithic, web-service-centric).
- Multi-agent configuration: `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- `PROJECT_STATUS.md` — session-state tracking.
- CC BY 4.0 licence.
