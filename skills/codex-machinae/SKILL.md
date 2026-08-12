---
name: codex-machinae
description: Process playbook for shipping software with LLM collaborators. Use when starting a new project, when adopting process on an existing codebase (retrofit), when a dependency or boundary contract changes or breaks, when preparing a release, or when coordinating multiple agents on one repository.
---

# Codex Machinae

A process playbook for building, testing, and maintaining software with AI
agents as collaborators. It prescribes **how to work** — requirements,
structure, quality, testing, remediation — never what to build.

Everything activates by **trigger**. This file carries the steps and the
routing; the deep rules live in [reference/](reference/) and are loaded only
when their condition fires. Loading reference that no trigger asked for is a
violation of the playbook's own first principle (Emergent Expansion).

Section references like `§5.3` resolve inside [reference/core.md](reference/core.md);
`D1…D7`, `M1…M4`, and `Appendix A…D` name files under
[reference/domains/](reference/domains/), [reference/modules/](reference/modules/),
and [reference/appendices/](reference/appendices/).

## Operating rules — always apply

1. Read the repo's agent-configuration file before any action. Update
   `PROJECT_STATUS.md` at session end — four sections: Objective, Modified
   Files, Logical State, Next Action (§2.3).
2. A **project-size profile** — Solo, Small, or Large — must be declared in
   the agent config; it modulates every checklist obligation (§2.5). If none
   is declared, ask for one before Phase work starts.
3. **Emergent Expansion** (§2.2): no folder, file, or process exists until a
   trigger fires. Propose expansions as *"I suggest adding `<path>` to cover
   `<concern>` because `<trigger>`. Cost of omission: `<what breaks>`"* — and
   wait for acceptance. Propose removal when a trigger lapses.
4. Autonomy is bounded (§12.1–§12.5): touch only the client/adapter layer and
   tests unless directed otherwise; ship a regression test with every fix;
   for complex features propose the approach in writing and await approval
   before code; never claim an action you did not perform.
5. An item is **done** only when the Core Definition of Done passes and every
   contextual check is satisfied or recorded `n/a` — never silently skipped
   (§1.8).
6. More than one agent on the repo → load the coordination protocol first
   (§12.7): lead designation, scope partitioning, single-writer artefacts.

## Route by situation

| Situation | Route |
|---|---|
| New project, way to the PRD not yet clear, effort exceeds one session | **Decision mapping** first (§1.9), then Phase 0 |
| New project, requirements clear | **Phase 0** below |
| Existing codebase adopting the playbook | **Phase R** below |
| Dependency / contract changed or broke | **Classification → remediation** below |
| Release being prepared | Module **M3** (+ D2/D6 if library/mobile) |
| Feature work in flight | **Phase 2** loop below |

## Lifecycle

### Phase 0 — Ideation and requirements (§11.1, checklist A.1)

0. If the effort exceeds one agent session *and* open decisions block the
   PRD: run **decision mapping** (§1.9) — chart the decisions as a map of
   typed tickets (research / prototype / grilling / task), resolve one per
   session, collapse the cleared map into the artefacts below. Plan, don't
   do: no production code while a map is open.
1. Write the PRD — what and why, never how (§1.2).
2. User stories with binary acceptance criteria, each falsifiable at the
   starting commit; stories cut as vertical slices sized to one agent
   session (§1.3–§1.4).
3. ADRs for decisions passing the three-test bar: hard to reverse,
   surprising without context, real trade-off (§1.5).
4. State-of-the-art research when a §1.7 trigger fires; findings land in the
   research register.
5. Backlog ordered by priority (§1.6); Definition of Done agreed (§1.8);
   critical dependencies in `DEPENDENCIES.md`.

**Done when:** checklist A.1 passes for the declared profile.

### Phase 1 — Technical bootstrap (§11.2, checklist A.2)

Minimum Core of Existence only — `README.md`, `PROJECT_STATUS.md`, agent
config (§2.1) — then: linting/formatting hooks (§3.4), base CI (§7), initial
Boundary Contract Map (§8), `.env.example` where secrets exist (§4.3).

**Done when:** checklist A.2 passes; CI is green on an empty-but-real build.

### Phase 2 — Active development (§11.3, checklists A.3–A.4)

The loop, per user story: respect the DoD; tests at every appropriate tier
of the pyramid (§5); coverage ratchet never loosens (§5.3); Conventional
Commits (§3.3); CHANGELOG on user-visible change (§6.3); contract map updated
after significant refactors (§8).

### Phase 3 — Maturity (§11.4) · Phase 4 — Major upgrade (§11.5)

Phase 3: fixes ride the autonomy ladder (below); quarterly threshold review.
Phase 4: a major dependency upgrade disables L1 — everything is human-led
until the contract map is regenerated and the harness re-verified.

### Phase R — Retrofit (§11.6, template B.9)

For codebases that predate the playbook. One-time convergence, not a phase
sequence: **debt-scoping audit** → retroactive contract map → adoption in
tiers (T1 safety net, then T2 structure, then T3 process; T1 is
non-negotiable and first). Enter the lifecycle at Phase 2 or 3 when T1+T2
are complete.

## When something changes or breaks

1. **Classify** the change (§9): bucket + severity (`safe` / `additive` /
   `breaking` / `p0`), checked against the never-auto-merge list (§9.3).
2. **Remediate** on the autonomy ladder (§10.1): L0 auto-merge (safe, green
   tests) · L1 agent PR with fix-claim behind the correctness gate (§10.2) ·
   L2 human-led (breaking, p0, or missing machinery). Circuit breaker: 3
   open L1 PRs or 5 attempts in 14 days pauses automation and produces a
   handover dossier (§10.3–§10.4).
3. Wide mechanical refactors that defeat vertical slicing are sequenced as
   **expand–contract** (§10.7).

## Domain appendices — load on trigger

| Trigger | Load |
|---|---|
| HTTP/API service, anything deployed serverside | [D1 Web Service](reference/domains/D1-web-service.md) |
| Published package consumed as a dependency | [D2 Library / SDK](reference/domains/D2-library-sdk.md) |
| Command-line tool | [D3 CLI Tool](reference/domains/D3-cli-tool.md) |
| Firmware, hardware peripherals, RTOS | [D4 Embedded / Firmware](reference/domains/D4-embedded-firmware.md) |
| ML models, training, data pipelines | [D5 ML / Data Pipeline](reference/domains/D5-ml-data-pipeline.md) |
| iOS/Android app, store distribution | [D6 Mobile App](reference/domains/D6-mobile-app.md) |
| Static site, frontend-only deployment | [D7 Static Site](reference/domains/D7-static-site.md) |

## Cross-cutting modules — load on trigger

| Trigger | Load |
|---|---|
| External dependencies need continuous compatibility monitoring | [M1 Surveillance](reference/modules/M1-surveillance.md) |
| Auth, payments, PII, or other security-sensitive surface | [M2 Security-sensitive](reference/modules/M2-security-sensitive.md) |
| Versioned artefacts released to users or registries | [M3 Release & Distribution](reference/modules/M3-release-distribution.md) |
| The project classifies domain entities into a controlled vocabulary | [M4 Classification & Taxonomy](reference/modules/M4-classification-taxonomy.md) |

## Reference index

- [reference/core.md](reference/core.md) — the full Core: §1 requirements
  (incl. §1.9 decision mapping), §2 structure and profiles, §3 quality,
  §4 security, §5 testing, §6 documentation, §7 CI/CD, §8 boundary
  contracts, §9 classification, §10 remediation, §11 lifecycle, §12 agent
  conventions.
- [reference/appendices/A-checklists.md](reference/appendices/A-checklists.md) —
  per-phase checklists, profile-aware. Consult at every phase gate.
- [reference/appendices/B-templates.md](reference/appendices/B-templates.md) —
  PRD, story, ADR, dependencies, contract map, retrofit audit, decision map
  templates. Copy, never retype.
- [reference/appendices/C-glossary.md](reference/appendices/C-glossary.md) —
  the vocabulary; consult when a term in this file is unfamiliar.
- [reference/appendices/D-tooling.md](reference/appendices/D-tooling.md) —
  specifications for the AST Walker, Coverage Ratchet, and Surveillance
  Agent scaffolds.
- [reference/limitations.md](reference/limitations.md) — what the playbook
  deliberately does not cover.

---

*Codex Machinae is licensed CC BY 4.0. Attribution: "Codex Machinae —
https://github.com/SOsintOps/codex-machinae". The reference tree is
generated from the repository's `playbook/` sources by `tools/build.py`;
edit the sources, not the copies.*
