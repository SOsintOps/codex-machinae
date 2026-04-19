# Codex Machinae — Modularisation Plan

**Status:** Draft v2 — Phases 0–8 closed, Phase 9 ready to start
**Created:** 2026-04-18
**Owner:** human + Claude (multi-session)
**Goal:** Split the playbook into a universal **Core** + **Domain Appendices** (per project type) +
**Cross-cutting Modules** (activated by trigger), so the playbook applies to any software project
— not just web services.

---

## Context for a resuming agent

`codex-machinae.md` (≈1450 lines) mixes universal process rules with concrete guidance that
implicitly assumes a web service (REST API, Docker, blue-green deploy, JWT auth, SQL migrations).
The user wants it to become a true meta-framework: a sober Core usable by any project, plus
activatable appendices per project type (library, CLI, embedded, ML, mobile, static site, web
service) and cross-cutting modules (surveillance, security-sensitive, release/distribution).

The refactor respects the **Emergent Expansion Protocol** (§2.2): every module has a trigger
condition; nothing is mandatory until the trigger fires.

**Hard rule for resuming sessions:** read the Decisions log at the bottom — all Phase 0 choices
are frozen. Never leave numbering gaps: renumber Core incrementally at the end of every
extraction phase (the final sweep in Phase 10 is a verification, not the renumbering itself).

---

## Resumption protocol (use when tokens run out or a new session starts)

**Ground truth hierarchy — trust in this order:**

1. **Git state** (`git status`, `git log`, `git diff`) — authoritative record of what changed
2. **This plan's Progress log** — author's claim of where we are
3. **This plan's Phase checkboxes** — design intent

If they disagree: trust Git, then update the plan to match reality.

**Steps to resume (any Claude, any session):**

1. Read `PROJECT_STATUS.md` for global context
2. Read this file end-to-end, focusing on Decisions log, current phase, and Progress log
3. Run `git status` and `git log -5` — understand what is committed vs uncommitted
4. **Cross-check:**
   - Clean working tree + last commit matches the most recent Progress-log entry → resume at the
     first unchecked item in the next phase
   - Clean working tree + last commit is behind Progress log → the log is wrong; update it to
     match Git
   - Dirty working tree → a phase was interrupted mid-way. Read the diff. Three options:
     a. If the partial work is coherent and safe, finish that sub-step, commit, update Progress log
     b. If the partial work is broken, `git stash` or ask the human before discarding
     c. Never `git reset --hard` without explicit human approval
5. Before making any change, verify current Core numbering by scanning `codex-machinae.md`
   headings — do not trust the plan's section numbers if Git shows they have been renumbered
6. Write the next step's intent into the Progress log **before** doing the work, not after. If
   tokens run out mid-step, the next session sees the intent and can finish it
7. At phase boundaries, commit + append to Progress log atomically (single session turn)

**Policy on checkpoint commits inside a phase:**

- Each phase is designed as a single logical commit. Prefer that
- For large phases (Phase 8 sub-phases, Phase 2, Phase 6), safe intermediate commits labelled
  `refactor(playbook): [phase X] wip — <substep>` are allowed to protect progress
- At phase end, intermediate commits may be kept (not squashed) — they improve auditability

**Never leave the repo in a broken state:**

- After any commit, cross-references must resolve (or the phase is not complete)
- If an edit creates a broken (§...) reference, fix it in the same commit, not later

---

## Target architecture

```
codex-machinae.md
├── Part I — Core (universal — applies to every software project)
│   ├── §1  Requirements and planning
│   ├── §2  Project structure + Emergent Expansion
│   ├── §3  Code quality (principles, naming, commits, metrics, errors)
│   ├── §4  Security fundamentals (principles + secrets only)
│   ├── §5  Testing fundamentals (pyramid, coverage, assertions, schema-primary)
│   ├── §6  Documentation fundamentals (README, CHANGELOG, code comments)
│   ├── §7  CI/CD fundamentals (pipeline as concept, rollback principle, adapter pattern)
│   ├── §8  Boundary Contracts
│   ├── §10 Change classification  (kept at §10 until Phase 10 renumbering)
│   ├── §12 Remediation (risk-modulated pattern)
│   ├── §15 Project lifecycle
│   └── §16 Conventions for AI agents
│
├── Part II — Domain Appendices (activated by project type)
│   ├── D1 Web Service         (REST/GraphQL, cloud deploy)
│   ├── D2 Library / SDK       (published package)
│   ├── D3 CLI Tool
│   ├── D4 Embedded / Firmware
│   ├── D5 ML / Data Pipeline
│   ├── D6 Mobile App
│   └── D7 Static Site / Frontend-only
│
├── Part III — Cross-cutting Modules (activated by trigger)
│   ├── M1 Surveillance                 (from §§9, 11, 13, 14)
│   ├── M2 Security-sensitive           (from §§4.3, 4.5, 4.6)
│   ├── M3 Release & Distribution
│   └── M4 Classification & Taxonomy    (framework-agnostic: MECE, governance, versioning,
│                                         and the scouting protocol that directs the AI to
│                                         find domain-specific frameworks per project)
│
└── Appendices
    ├── A — Checklists (Core + per-module split)
    ├── B — Templates  (Core + per-module split)
    └── C — Glossary (merged)
```

---

## MVP scope (Decisions log item)

Selection is driven by **meta-framework merit**, not by any specific project. The chosen MVP
maximises coverage breadth of orthogonal runtime/deploy models and uses the cheapest-to-fill
modules as early validators of the cross-cutting pattern.

| Target | Scope | Merit-based rationale |
|--------|-------|-----------------------|
| Core §§1–… (renumbered incrementally) | Full rewrite | Universal foundation |
| **D1 Web Service**       | Full content | Most common domain; maximum leverage on existing web-biased text; where most of §4, §6, §7 already implicitly live |
| **D4 Embedded / Firmware** | Full content | Diametrically opposite to D1 (no cloud, no rolling deploy, hardware-in-loop); stress-tests Core sobriety — if any Core section smuggles in a web assumption, D4 surfaces it |
| **D5 ML / Data Pipeline** | Full content | Adds an orthogonal data-centric axis; validates data-specific threads already latent in the playbook (§5.9 golden queries, §7.4 migrations) |
| **M1 Surveillance**      | Full content | Already well written in §§9, 11, 13, 14; extract + reframe is cheap and validates the cross-cutting pattern |
| **M2 Security-sensitive** | Full content | Extract of §§4.3, 4.5, 4.6 is cheap and shows the pattern at a second angle |
| **M4 Classification & Taxonomy** | Full content | New content but small; validates the scouting-protocol pattern binding a module to §1.7 SOTA Scout |
| **M3 Release & Distribution** | Stub (heading + trigger + 2–3 bullets) | Deferred; meaningful only once D2/D3/D6 are fleshed out |
| **D2 Library / SDK**     | Stub | Deferred |
| **D3 CLI Tool**          | Stub | Deferred |
| **D6 Mobile App**        | Stub | Deferred |
| **D7 Static Site**       | Stub | Deferred |

**Two distinct project roles — do not conflate:**

| Role | Direction of flow | Projects |
|------|-------------------|----------|
| **Inspiration / quality benchmark** — a well-structured piece of work whose level of rigour, tone, and organisation sets the bar for what the playbook should produce. Read-only by CLAUDE.md; the playbook takes inspiration but does not copy it | observation → playbook design choices | `example/00-prd.md` (Cortex) |
| **Downstream application target** — the playbook, once ready, will be applied to retrofit started-but-unfinished work | playbook → project | `~/github/zero-to-hero-workshop` branch `the-italian-job` (full-stack Next.js web app); `~/github/safe-heaven` (RPi 5 / Hailo / drone / radar / local LLM) |

The downstream projects are **post-MVP customers**, not inputs to MVP design. It is a useful
coincidence that the merit-based MVP (D1 + D4 + D5 + M1 + M2 + M4) already covers what they
will need — it is not the reason for the MVP choice.

Expected retrofit scenarios after Phase 10:

- Italian Job → activate Core + D1 + M2 + M4 (optionally M1) to bring the branch in line with
  the playbook's structure and Definition of Done
- SafeHeaven → activate Core + D4 + D5 + M1 + M2 + M4 to organise the research-phase repo into
  a playbook-conformant project before code is written in earnest

Additional downstream targets can be added over time without changing MVP scope.

---

## Current-section → new-home classification

| Current section | New home | Notes |
|-----------------|----------|-------|
| §1 Requirements and planning    | Core §1                     | Universal, minor rewording |
| §2 Project structure            | Core §2                     | Already universal |
| §3.1 Architectural principles   | Core §3                     | Universal |
| §3.2 Naming conventions         | Core §3                     | Universal (multi-language examples) |
| §3.3 Conventional Commits       | Core §3                     | Universal |
| §3.4 Linting and formatting     | Core §3                     | Concept universal; tool table as reference |
| §3.5 Complexity metrics         | Core §3                     | Universal |
| §3.6 Error handling             | Core §3                     | Universal |
| §3.7 Dependency management      | Core §3                     | Applies when runtime deps exist |
| §3.8 Branching strategy         | Core §3                     | Universal |
| §4.1 Security principles        | Core §4 (slimmed)           | Universal |
| §4.2 Input validation           | Core §4                     | Concept; examples in modules |
| §4.3 Auth and authorisation     | M2 Security-sensitive       | Web/service-specific |
| §4.4 Secrets management         | Core §4                     | Applies whenever secrets exist |
| §4.5 Security PR checklist      | M2 Security-sensitive       | Currently web-biased |
| §4.6 OWASP Top 10               | M2 Security-sensitive       | Web-app-specific |
| §5.1 Testing pyramid            | Core §5                     | Universal |
| §5.2 Rules per tier             | Core §5 (lighter) + D1/D6 specifics |   |
| §5.3 Coverage ratchet           | Core §5                     | Universal |
| §5.4 Test data strategy         | Core §5                     | Universal |
| §5.5 Tests in CI                | Core §5                     | Universal (timings indicative) |
| §5.6 Assertion discipline       | Core §5                     | Universal |
| §5.7 Schema-primary validation  | Core §5                     | Applies when contracts exist |
| §5.8 Two-layer regression       | Core §5                     | Applies when upstream exists |
| §5.9 Golden queries             | D5 ML / Data Pipeline       | DB/data-migration-specific |
| §6.1 Required documents         | Core §6                     | Universal |
| §6.2 Code documentation         | Core §6                     | Universal |
| §6.3 API documentation          | D1 Web Service + D2 Library | Domain-specific |
| §6.4 CHANGELOG                  | Core §6                     | Universal |
| §7.1 Pipeline overview          | Core §7                     | Concept universal |
| §7.2 Pipeline stages            | Core §7 (stages) + D1 (Docker/staging specifics) | Split |
| §7.3 Rollback                   | Core §7                     | Universal principle |
| §7.4 Database migration         | D5 ML / Data Pipeline       | DB-specific |
| §7.5 Environments               | D1 Web Service              | Cloud-biased |
| §7.6 Configuration as code      | Core §7                     | Universal |
| §7.7 Adapter pattern for CI     | Core §7                     | Universal |
| §8 Boundary Contracts           | Core §8                     | Already universal |
| §9 Surveillance agents          | M1 Surveillance             | |
| §10 Change classification       | Core §10                    | Pattern universal |
| §11 Compatibility test matrix   | M1 Surveillance             | |
| §12 Remediation workflow        | Core §12                    | Already universal |
| §13 Compatibility database      | M1 Surveillance             | |
| §14 Self-testing/observability  | M1 Surveillance             | |
| §15 Project lifecycle           | Core §15                    | Strip module-specific steps |
| §16 Agent conventions           | Core §16                    | Universal |
| Appendix A                      | A (Core) + per-module split | |
| Appendix B                      | B (Core) + per-module split | |
| Appendix C                      | C (merged)                  | |

---

## Phased execution

One commit per phase. Progress is tracked in the **Progress log** at the bottom.
Every phase is resumable: the plan's state is the filesystem + the progress log.

### Phase 0 — Approve plan (HUMAN GATE) — ✅ CLOSED 2026-04-18

- [x] Human confirmed the classification table
- [x] Human confirmed the domain list (7) and module list (4, incl. new M4)
- [x] All four Open Questions answered (see Decisions log)
- [x] MVP scope frozen (see table above)

### Phase 1 — Skeleton — ✅ CLOSED 2026-04-18

- [x] Add `Part II — Domain Appendices` (D1–D7) and `Part III — Cross-cutting Modules` (M1–M4)
      with empty headings
- [x] Under each heading write only: activation trigger + "in addition to Core" placeholder
- [x] Update TOC to reflect the new parts
- [x] Commit: `refactor(playbook): add module and domain scaffolding`

### Phase 2 — Surveillance Module (M1) — ✅ CLOSED 2026-04-18

- [x] Move §§9, 11, 13, 14 into `M1 Surveillance` (Part III)
- [x] Rewrite the module intro: activation trigger = "Boundary Contract Map populated with at least
      one outbound contract worth monitoring"
- [x] Scrub surveillance-specific wording from Core §8, §10, §12 (they stay in Core)
- [x] **Renumber Core** to close the gaps left by the extraction; sweep all (§...) cross-references
- [x] Commit: `refactor(playbook): extract Surveillance Module (M1) from Part II`

### Phase 3 — Security split (Core §4 ↔ M2) — ✅ CLOSED 2026-04-18

- [x] Core §4 slimmed to: §4.1 principles, §4.2 input-validation concept, §4.3 secrets (renumbered from §4.4)
- [x] Move §4.3 auth → M2.1, §4.5 PR checklist → M2.2, §4.6 OWASP → M2.3
- [x] M2 activation trigger retained: "project handles authentication, authorisation, or PII"
- [x] Renumbered Core §4 sub-sections contiguously; swept (§4.x) cross-references
- [x] Commit: `refactor(playbook): split security into Core + M2 Security-sensitive`

### Phase 4 — Testing split (Core §5 ↔ D5) — ✅ CLOSED 2026-04-18

- [x] Core §5 keeps pyramid, coverage, test data, CI, assertion, schema-primary, two-layer regression
- [x] Moved §5.9 golden queries into `D5 ML / Data Pipeline` as D5.1
- [x] Core §§5.1–5.8 already contiguous (§5.9 was at tail); no Core renumbering required
- [x] No external (§5.9) cross-references to sweep; only the D5 placeholder meta-text
- [x] Commit: `refactor(playbook): move domain-specific testing to modules`

### Phase 5 — Documentation split (Core §6 ↔ D1/D2/D3) — ✅ CLOSED 2026-04-18

- [x] Core §6 keeps §6.1 required docs (universal subset), §6.2 code docs, §6.3 CHANGELOG (renumbered from §6.4)
- [x] Split §6.3 API documentation across three appendices: REST row → D1.1, SDK rows → D2.1, CLI row → D3.1
      (extends the original plan's D1/D2 scope by also extracting the CLI row into D3 — see Progress log)
- [x] Renumbered Core §6 sub-sections contiguously; swept (§6.x) cross-references
- [x] Commit: `refactor(playbook): split documentation into Core + domain appendices`

### Phase 6 — CI/CD split (Core §7 ↔ D1/D5) — ✅ CLOSED 2026-04-18

- [x] Core §7 kept: §7.1 pipeline overview (generalised diagram), §7.2 abstract stages (generalised Build/Stage/Deploy), §7.3 rollback principle (universalised table), §7.4 configuration-as-code (renumbered from §7.6), §7.5 CI adapter pattern (renumbered from §7.7)
- [x] Moved §7.2 deploy specifics (blue-green, rolling, canary, /healthz, feature flags) → D1.2; §7.5 environments table → D1.3
- [x] Moved §7.4 database migration → D5.2, including the irreversible-migration rule
- [x] Renumbered Core §7 sub-sections contiguously; swept (§7.x) cross-references
- [x] Commit: `refactor(playbook): split CI/CD into Core + D1 Web Service + D5 Data`

### Phase 7 — Lifecycle generalisation (Core §11) — ✅ CLOSED 2026-04-18

- [x] Rewrote §11 Phases 0–4 using the "Core steps + activation blocks" pattern so nothing module-specific is mandatory until a trigger fires
- [x] Added activation blocks: M1 Surveillance (Phases 1, 2, 3), M2 Security-sensitive (Phase 3), D1/D2/D3 (Phase 2), and "persistent structured data" (Phase 1)
- [x] Fixed four reference bugs along the way: §1.7 → §1.8 (DoD) in Phases 0 and 2; §2.3 → §2.4 (agent configuration) in Phase 1; §2.2 → §2.3 (PROJECT_STATUS.md) in Phase 2
- [x] Commit: `refactor(playbook): generalise lifecycle phases`

### Phase 8 — Module and domain content (MVP set) — ✅ CLOSED 2026-04-19

Full content for the MVP targets (D1, D4, D5, M1, M2, M4); stubs only for D2, D3, D6, D7, M3.
**Split into sub-phases — one commit each — so token exhaustion never loses more than one module.**

#### Phase 8.1 — D1 Web Service (full)
- [x] Trigger, extracted §§6.3, 7.2 specifics, 7.5; domain-specific testing patterns; deploy strategies
- [x] Commit: `refactor(playbook): flesh out D1 Web Service`

#### Phase 8.2 — D4 Embedded / Firmware (full)
- [x] Trigger (fixed hardware target, memory/energy limits), hardware-in-loop testing, flash/OTA,
      device-protocol contracts
- [x] Commit: `refactor(playbook): flesh out D4 Embedded / Firmware`

#### Phase 8.3 — D5 ML / Data Pipeline (full)
- [x] Trigger, extracted §5.9 golden queries, §7.4 migrations, training pipeline, model drift,
      dataset versioning
- [x] Commit: `refactor(playbook): flesh out D5 ML / Data Pipeline`

#### Phase 8.4 — M1 Surveillance (polish)
- [x] Most content is already filled in Phase 2; this sub-phase polishes cross-references,
      adds examples, ensures the activation trigger is sharp
- [x] Commit: `refactor(playbook): polish M1 Surveillance`

#### Phase 8.5 — M2 Security-sensitive (polish)
- [x] Most content is already filled in Phase 3; polish, examples, sharpen trigger
- [x] Commit: `refactor(playbook): polish M2 Security-sensitive`

#### Phase 8.6 — M4 Classification & Taxonomy (full, framework-agnostic)
- [x] Design principles (MECE, parsimony, stable IDs, semver of the taxonomy itself)
- [x] Governance (ownership, proposal/deprecation protocol, RFC for new terms)
- [x] **Scouting protocol** — the AI researches domain-specific frameworks per project; binds to
      §1.7 SOTA Scout so scouting is a first-class, repeatable activity rather than an ad-hoc step
- [x] Adoption patterns — how to integrate a found framework without reinventing it
- [x] Audits (coverage, ambiguity, false-pos/neg metrics, drift over time)
- [x] Machine-readable formats (JSON Schema / JSON-LD / OWL / STIX-like serialisations)
- [x] Upstream contribution protocol — when a project's local extension deserves promotion back
- [x] Illustrative examples section (non-prescriptive): threat intel → MITRE ATT&CK/STIX/FT3;
      vulnerability → CVE/CWE/CAPEC; sharing policy → TLP; intelligence cycle → F3EAD;
      biomedicine → SNOMED/ICD; geospatial → ISO 19115. Examples exist to show the *shape*
      of adoption, never as a default catalogue
- [x] Commit: `refactor(playbook): flesh out M4 Classification & Taxonomy`

#### Phase 8.7 — Stubs (D2, D3, D6, D7, M3)
- [x] Each stub: heading + trigger + 2–3 bullets
- [x] Commit: `refactor(playbook): add stubs for D2, D3, D6, D7, M3`

### Phase 9 — Appendices A/B/C reorganisation

- [ ] Split Appendix A checklists into Core + per-module
- [ ] Split Appendix B templates into Core + per-module
- [ ] Update Appendix C glossary with new terms (D1–D7, M1–M3, "module", "domain")
- [ ] Commit: `refactor(playbook): reorganise appendices by module`

### Phase 10 — Final verification

Renumbering happens incrementally in Phases 2–6 (never leave gaps). This phase is a full audit.

- [ ] Verify Core §§ numbering is contiguous with no gaps or duplicates
- [ ] Run a full (§...) cross-reference sweep: every reference resolves to an existing heading
- [ ] Verify TOC matches actual headings
- [ ] Absorb remaining `STRATEGY_TRANSFORMATION.md` content into the playbook; delete the file
- [ ] Update `PROJECT_STATUS.md` to reflect the new state
- [ ] Update `MODULARISATION_PLAN.md` status to "complete"
- [ ] **Remove the WORK IN PROGRESS notice from `README.md`** (added under the ASCII art at
      the start of modularisation; must come off when the playbook design is stable)
- [ ] Commit: `refactor(playbook): finalise modularisation — audit, xrefs, status`

---

## Open questions

None. All Phase 0 decisions are recorded in the Decisions log below.

---

## Decisions log (append-only)

- 2026-04-18: Architecture frozen — `Core + Domain Appendices (D1–D7) + Cross-cutting Modules (M1–M4)`.
- 2026-04-18: **Q1 MVP scope** — full content for D1, D4, D5, M1, M2, M4; stubs for D2, D3, D6, D7, M3.
  Rationale: merit-based — D1/D4/D5 span three orthogonal runtime/deploy models (cloud, embedded
  hardware, data pipeline) and jointly stress-test Core sobriety; M1/M2 are cheap extractions of
  existing text; M4 validates the scouting-protocol binding to §1.7. Real-world projects
  (Italian Job, SafeHeaven, Cortex) are illustrative references, not drivers.
- 2026-04-18: **Q2 File layout** — single file `codex-machinae.md`. Split into separate files is
  deferred until size forces it.
- 2026-04-18: **Q3 Renumbering** — never leave numbering gaps. Renumber Core incrementally at the
  end of every extraction phase; final sweep in Phase 10 is an audit, not a renumber.
- 2026-04-18: **Q4 Surveillance framing** — Option A (cross-cutting module M1), consistent with
  M2/M3/M4. Rationale: surveillance is a capability, not a project phase; it composes with any
  domain.
- 2026-04-18: **Added M4 Classification & Taxonomy** — cross-cutting module for MECE design,
  governance, versioning, and the **scouting protocol** the AI follows per project to find
  domain-specific frameworks. M4 is framework-agnostic: it does NOT ship a curated catalogue;
  it directs the AI to research what exists in each project's domain (threat intel, biomedicine,
  geospatial, …) and propose adoption. Illustrative examples (MITRE ATT&CK, STIX, FT3, CAPEC,
  TLP, F3EAD, SNOMED, ICD, ISO 19115) are included only to show the *shape* of adoption, never
  as defaults. Binds tightly to §1.7 SOTA Scout for repeatability. FT3 reference:
  github.com/stripe/ft3 — Stripe's ATT&CK-style fraud taxonomy.

---

## Progress log (append-only, one line per session)

- 2026-04-18 — Plan drafted (v1). Phase 0 opened.
- 2026-04-18 — Phase 0 closed. MVP scope frozen. M4 added.
- 2026-04-18 — M4 reframed: framework-agnostic scouting protocol (not a fixed catalogue);
  binds to §1.7 SOTA Scout.
- 2026-04-18 — Reference projects (Italian Job, SafeHeaven) reclassified as illustrative.
  MVP rationale rewritten on merit.
- 2026-04-18 — Further clarification: Italian Job and SafeHeaven are **downstream application
  targets** (playbook → project). `example/00-prd.md` (Cortex) is **inspiration / quality
  benchmark** — a well-structured reference whose rigour sets the bar, not a mechanical pattern
  source. The playbook takes inspiration from Cortex but never copies it; the downstream projects
  are post-MVP customers; their domain alignment with the MVP is coincidental, not causal.
- 2026-04-18 — Added Resumption protocol (ground-truth hierarchy, resume steps, checkpoint
  commit policy). Split Phase 8 into sub-phases 8.1–8.7 so token exhaustion loses at most one
  module of work. Ready for Phase 1.
- 2026-04-18 — Phase 1 intent: add Part II (D1–D7) and Part III (M1–M4) empty headings with
  activation triggers + "in addition to Core" placeholders; update TOC. Single commit.
- 2026-04-18 — Phase 1 executed. TOC reflects Core (flat §§1–16 with §§9, 11, 13, 14 marked
  as M1-extraction candidates), Part II (D1–D7), Part III (M1–M4). Old `PART II — SURVEILLANCE
  AND MAINTENANCE` and `PART III — MANAGEMENT` body headers removed; sections §§8–16 now live
  flat under `PART I — CORE`. D1, D4, D5, M1, M2, M4 scaffolded with phase references for their
  full-content fill; D2, D3, D6, D7, M3 scaffolded as stubs. Ready for Phase 2 (M1 extraction).
- 2026-04-18 — Phase 2 intent: extract §§9, 11, 13, 14 into M1 as M1.1–M1.4; renumber Core
  §10→§9 (Change classification), §12→§10 (Remediation), §15→§11 (Lifecycle), §16→§12 (Agent
  conventions); scrub surveillance-specific prose from Core §8 and the new §9/§10; sweep all
  (§X.Y) cross-references. Two sub-commits: (a) wip checkpoint — extract to M1 and fix refs
  to moved sections; (b) final — renumber remaining Core, scrub prose, sweep refs, close phase.
- 2026-04-18 — Phase 2 executed as a single commit (extraction + renumber + sweep + prose
  scrub all coherent). M1.1–M1.4 populated verbatim from §§9, 11, 13, 14 with headings
  reshaped (### M1.X / #### M1.X.Y). Core renumbered to contiguous §§1–12. Cross-reference
  sweep done via sed (§9→M1.1, §10→§9, §11→M1.2, §12→§10, §13→M1.3, §14→M1.4, §15→§11,
  §16→§12) plus heading renumbering. Scrubs applied: §8 explicitly scopes compatibility
  testing to M1; §10.3 replaces "agentic loop" with "L1 automation"; §10.4 replaces "the
  classifier detects" with "a change is classified as". TOC updated; Part I header note on
  "candidates for extraction" removed. Ready for Phase 3 (security split).
- 2026-04-18 — Out-of-phase housekeeping: added `LICENSE` (CC BY 4.0) at repo root and
  refreshed `README.md` header (H1 first, banner below, three badges, TL;DR, Licence
  section). Commit `abc8a45`. Pushed to `origin/main`. Not a phase step — pure repo hygiene
  before continuing the modularisation.
- 2026-04-18 — Phase 3 intent: move Core §4.3 (auth) → M2.1, §4.5 (PR checklist) → M2.2,
  §4.6 (OWASP Top 10) → M2.3; renumber Core §4.4 (secrets) → §4.3 so Core §4 becomes
  contiguous §§4.1–4.3; replace the M2 placeholder with a proper activation-trigger intro
  plus M2.1–M2.3 subsections. Cross-reference sweep: §4.4 → §4.3 (lines ≈1029, 1388),
  §4.5 → M2.2 (lines ≈1389, 1399). §4.2 reference unchanged (line ≈1400). Single commit.
- 2026-04-18 — Phase 3 executed as a single commit. Core §4 is now §4.1 principles, §4.2
  input validation, §4.3 secrets management (renumbered from §4.4). M2 placeholder replaced
  with populated M2.1 auth, M2.2 PR checklist, M2.3 OWASP (verbatim extraction; polish
  deferred to Phase 8.5). Core §4.3 ends with a one-sentence pointer to M2 so readers see
  the composition. Cross-references updated: §4.4 → §4.3 (lines 1008, 1390); §4.5 → M2.2
  (lines 1391, 1401); §4.2 unchanged (line 1402). TOC unchanged (no sub-section numbering
  there). Ready for Phase 4 (testing split Core §5 ↔ D5).
- 2026-04-18 — Phase 4 intent: move §5.9 golden queries out of Core §5 into D5 as D5.1;
  §§5.1–5.8 already contiguous so no Core renumbering required. Replace D5 placeholder with
  a populated preamble + D5.1 verbatim extraction, leaving remaining D5 scope (§7.4
  migrations, training-pipeline reproducibility, dataset versioning, drift monitoring,
  evaluation contracts) marked as Phase 8.3 work. No external §5.9 cross-references to
  sweep (only the self-reference in the D5 placeholder meta-text). Single commit.
- 2026-04-18 — Phase 4 executed as a single commit. §5.9 removed from Core §5; replaced by
  a one-sentence pointer to D5 at the §5.8 tail. D5 placeholder replaced with a populated
  preamble + D5.1 verbatim extraction; an italic marker retains the Phase 8.3 backlog (§7.4
  migrations, reproducibility, versioning, drift, evaluation). No cross-reference sweep was
  needed — grepping §5.x after the edit confirms only references to §§5.3–5.7 remain, all
  of which are unchanged. Ready for Phase 5 (documentation split Core §6 ↔ D1/D2).
- 2026-04-18 — Phase 5 intent: remove §6.3 from Core and split its 4-row table across three
  appendices — REST row → D1.1, SDK rows (TS + Python) → D2.1, CLI row → D3.1. The CLI
  destination extends the plan text ("D1 and D2") because leaving the CLI row in Core would
  reintroduce a web/SDK-agnostic gap, and the CLI contract surface is the archetypal D3
  concern. Renumber Core §6.4 → §6.3 so Core §6 becomes contiguous §§6.1–6.3. Replace D1,
  D2, D3 placeholders with populated preambles + the appropriate Dx.1 subsection; D1's
  Phase 8.1 backlog marker retained for deploy/environments/request-path patterns; D2 and
  D3 retain Phase 8.7 stub markers for their remaining scope. Cross-references: drop the
  "(see §6.3)" citation at §5.7 line 650 (the enum-single-declaration rule stands on its
  own); §6.4 → §6.3 (line 1417); §6.3 → D1.1 / D2.1 / D3.1 (line 1422, PR release
  checklist — reword as conditional). Single commit.
- 2026-04-18 — Phase 5 executed as a single commit. Core §6.3 removed and replaced by a
  one-sentence pointer naming the three destination appendices. Core §6.4 renumbered to
  §6.3 (CHANGELOG). D1, D2, D3 placeholders replaced with populated preambles + D1.1, D2.1,
  D3.1 verbatim extractions (one table row each, per domain). Phase 8.1 backlog marker
  preserved for D1 (deploy/env/request-path); Phase 8.7 stub markers preserved for D2 and
  D3 (their non-doc scope). Cross-references updated: "(see §6.3)" dropped at §5.7 line 650
  because the enum-single-declaration rule is universal and does not need a pointer to API
  docs; §6.4 → §6.3 in Appendix A release checklist; §6.3 → "D1.1 / D2.1 / D3.1, where
  applicable" in the same checklist to make the conditional nature explicit. Ready for
  Phase 6 (CI/CD split Core §7 ↔ D1/D5).
- 2026-04-18 — Phase 6 intent: generalise Core §7 so its pipeline, stages, and rollback
  concepts are universal, and move web/data specifics into D1 and D5. Core §7 becomes
  contiguous §§7.1–7.5: §7.1 pipeline overview (strip Docker/staging from the ASCII diagram
  sub-text), §7.2 abstract pipeline stages (§7.2.1 Build loses "Docker image"; §7.2.3 Stage
  becomes "pre-production validation"; §7.2.4 Deploy becomes abstract with a pointer to
  domain appendices for strategy specifics), §7.3 rollback principle (drop the
  data-migration row and the irreversible-migration rule; add one sentence that domain
  appendices own class-specific rollback protocols), §7.4 configuration-as-code (was §7.6),
  §7.5 CI adapter pattern (was §7.7). D1 gains D1.2 Deploy strategy (blue-green, rolling,
  canary, /healthz, feature flags from §7.2.4 specifics) and D1.3 Environments (table from
  §7.5). D5 gains D5.2 Database migration (§7.4 verbatim) plus the irreversible-migration
  rule. Cross-references: line 1447 (§7.2.3) → "D1.2 where applicable" in release
  checklist; line 1449 (§7.4) → D5.2; §7 whole-chapter references unchanged at lines 981
  and 1418; D1 and D5 backlog markers rewritten to reflect what Phase 6 now fills vs what
  remains for Phase 8.1/8.3. Single commit.
- 2026-04-18 — Phase 6 executed as a single commit. Core §7 now contiguous §§7.1–7.5 with
  universalised content throughout. §7.1 pipeline diagram sub-text reworked ("package
  artefact" instead of "Docker image"; "pre-prod" instead of "staging"); explanatory
  sentence added naming domain appendices as the source of concrete meanings. §7.2 stages
  rewritten abstractly: Build covers binary/firmware/wheel/bundle; Stage covers
  sandbox/simulator/HIL; Deploy names strategy specifics as domain-specific. §7.3 rollback
  table pared to three universal rows (health-check, manual, irreversible) with a closing
  sentence that hands class-specific protocols to the owning appendix. §7.6 and §7.7
  renumbered to §7.4 and §7.5. D1.2 Deploy strategy and D1.3 Environments populated
  verbatim from the old §7.2.4 and §7.5; D5.2 Database migration populated verbatim from
  the old §7.4 plus the irreversible-migration rule (cross-ref to Core §7.3). Release
  checklist line 1458 reworded to "Pre-production smoke tests green on promotion" so the
  universal §7.2.3 reference still applies; line 1460 → "D5.2, where applicable". §7
  whole-chapter references unchanged. Ready for Phase 7 (lifecycle generalisation).
- 2026-04-18 — Phase 7 intent: rewrite §11 phases 0–4 using the "Core steps + activation
  blocks" pattern (aligned with §2.2 Emergent Expansion). §11.5 Phase 4 is already
  universal and stays verbatim. §11.1 Phase 0 is almost universal — only a ref fix
  (§1.7 → §1.8 for DoD). §11.2 Phase 1: Core steps become 1–6 (directory, lint, CI, CLAUDE
  writeup, contract map, .env.example); M1 block holds surveillance agents + first
  compatibility record; persistent-data block holds the seed script. §11.3 Phase 2: Core
  keeps user-story flow, PROJECT_STATUS updates, tests, coverage ratchet, CHANGELOG,
  contract-map upkeep; M1 block holds agent-produced compatibility records + fix/adoption
  PRs; D1/D2/D3 block holds API-doc updates. §11.4 Phase 3: Core keeps L0/L1 fix posture,
  quarterly baseline/threshold review, never-auto-merge list; M1 block holds continuing
  surveillance + monthly classifier retrospective; M2 block holds the annual OWASP review.
  Along the way, fix four reference bugs: line 959 §1.7 → §1.8 (DoD), line 967 §2.3 → §2.4
  (CLAUDE.md is Agent configuration), line 976 §1.7 → §1.8, line 977 §2.2 → §2.3
  (PROJECT_STATUS.md). Single commit.
- 2026-04-18 — Phase 7 executed as a single commit. §11 introduction rewritten to name the
  "Core steps + activation blocks" pattern and to tie it to §2.2 Emergent Expansion.
  §11.1 Phase 0 kept as a single Core list with the §1.7 → §1.8 ref fix. §11.2 Phase 1
  split into Core (6 items) + M1 block (surveillance agents, first compat record) +
  persistent-data block (seed script). §11.3 Phase 2 split into Core (6 items) + M1 block
  (background compat records + fix/adoption PRs) + D1/D2/D3 block (API-doc updates).
  §11.4 Phase 3 split into Core (3 items) + M1 block (continuing surveillance + monthly
  classifier retrospective at M1.4.2) + M2 block (annual OWASP review at M2.3). §11.5
  Phase 4 left verbatim (already universal), with the phase-label "phase 3" capitalised to
  "Phase 3" for consistency. All four ref bugs fixed in the same pass. Ready for Phase 8
  (module and domain content, MVP set).
- 2026-04-19 — Phase 8.1 intent: flesh out D1 Web Service. D1.1–D1.3 already populated
  (Phases 5–6). Add D1.4 Request-path testing, D1.5 Rate-limiting and back-pressure,
  D1.6 Observability hooks. Remove the Phase 8.1 backlog marker. Single commit.
- 2026-04-19 — Phase 8.1 executed as a single commit. D1 now has D1.1 API documentation,
  D1.2 Deploy strategy, D1.3 Environments (from Phases 5–6), plus D1.4 Request-path testing
  (contract tests, negative-path, latency, idempotency), D1.5 Rate-limiting and back-pressure
  (headers, circuit breaker, timeout, bulkhead), D1.6 Observability (structured logging,
  metrics, tracing, health/readiness). Ready for Phase 8.2 (D4 Embedded / Firmware).
- 2026-04-19 — Phase 8.2 intent: flesh out D4 Embedded / Firmware. Replace the placeholder
  with D4.1 Hardware boundary contracts, D4.2 Cross-compilation and toolchain, D4.3
  Hardware-in-the-loop testing, D4.4 Flash and OTA update strategy, D4.5 Power and thermal
  budgets, D4.6 Bring-up checklist. Single commit.
- 2026-04-19 — Phase 8.2 executed as a single commit. D4 now has D4.1–D4.6 covering HAL,
  cross-compilation, HIL testing, flash/OTA, power/thermal budgets, bring-up checklist.
  Ready for Phase 8.3 (D5 ML / Data Pipeline).
- 2026-04-19 — Phase 8.3 intent: flesh out D5 ML / Data Pipeline. D5.1 (golden queries)
  and D5.2 (database migration) already populated. Add D5.3 Training-pipeline
  reproducibility, D5.4 Dataset versioning, D5.5 Drift monitoring, D5.6 Evaluation
  contracts. Remove the Phase 8.3 backlog marker. Single commit.
- 2026-04-19 — Phase 8.3 executed as a single commit. D5 now has D5.1–D5.6. Ready for
  Phase 8.4 (M1 polish).
- 2026-04-19 — Phase 8.4 intent: polish M1 Surveillance. Sharpen activation trigger with
  concrete "when in doubt" guidance, add domain-composition table, add directory-tree
  example to M1.3.1, strengthen M1.4.4 with §8.4 cross-reference and scheduled
  re-generation. Single commit.
- 2026-04-19 — Phase 8.4 executed as a single commit. M1 polished. Ready for Phase 8.5
  (M2 polish).
- 2026-04-19 — Phase 8.5 intent: polish M2 Security-sensitive. Sharpen trigger with
  concrete examples, add domain-composition note, expand M2.3 with annual-review table,
  add M2.4 Dependency-vulnerability management (response SLA, transitive deps). Single
  commit.
- 2026-04-19 — Phase 8.5 executed as a single commit. M2 polished with M2.4 added. Ready
  for Phase 8.6 (M4 Classification & Taxonomy).
- 2026-04-19 — Phase 8.6 intent: flesh out M4 Classification & Taxonomy. Replace the
  placeholder with M4.1 Design principles (MECE, parsimony, stable IDs), M4.2 Governance
  (ownership, RFC, deprecation), M4.3 Scouting protocol (binding to §1.7), M4.4 Adoption
  patterns, M4.5 Audits (coverage, ambiguity, drift), M4.6 Machine-readable formats, M4.7
  Upstream contribution protocol, M4.8 Illustrative examples. Single commit.
- 2026-04-19 — Phase 8.6 executed as a single commit. M4 fully populated with M4.1–M4.8.
  Ready for Phase 8.7 (stubs D2, D3, D6, D7, M3).
- 2026-04-19 — Phase 8.7 intent: replace generic placeholders in D2, D3, D6, D7, M3 with
  concrete bullet-point stubs listing post-MVP scope. Single commit.
- 2026-04-19 — Phase 8.7 executed as a single commit. All Phase 8 sub-phases (8.1–8.7)
  closed. Phase 8 marked CLOSED. PROJECT_STATUS.md updated. Ready for Phase 9
  (Appendices A/B/C reorganisation).
