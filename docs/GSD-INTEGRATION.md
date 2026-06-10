# Using Codex Machinae with GSD

**Date:** 2026-06-10
**Status:** Operational guide — companion to [GSD-COMPARISON.md](GSD-COMPARISON.md)
**Applies to:** Codex Machinae 2.0.0 · GSD skill suite for Claude Code (notes for GSD-CC where relevant)

---

## 1. Why combine them

[GSD-COMPARISON.md](GSD-COMPARISON.md) establishes that the two frameworks own
disjoint layers: Codex Machinae defines **what "done" and "good" mean** (the
quality floor — testing, security, documentation, CI/CD, change risk); GSD
defines **how work moves from idea to verified code** (sessions, subagents,
artefacts, state). Run alone, each has a known gap:

- GSD alone ships fast, but nothing stops a phase from completing with zero
  coverage and secrets in code, provided the plan's own criteria pass.
- Codex Machinae alone sets a high floor, but every rule must be applied by
  hand — its acknowledged weakness is mechanical adoption cost
  ([limitations](../playbook/limitations.md), item 1).

Combined, GSD becomes the engine and Codex Machinae the law it enforces. This
guide describes the wiring. GSD is Claude Code-specific; the same pattern
applies to any workflow engine that (a) reads a project-level agent
configuration file and (b) gates phase completion on declared success criteria.

---

## 2. The division of authority

One rule prevents every conflict between the two systems:

> **Codex Machinae artefacts are normative; GSD artefacts are operational.**
> Where both describe the same fact, the playbook artefact wins, and the GSD
> artefact must be regenerated or corrected to match — never the reverse.

| Concern | Authority | Instrument |
|---------|-----------|------------|
| Quality floor (tests, security, complexity, docs) | Codex Machinae | Core §§3–7, active modules |
| Change risk and autonomy ceiling | Codex Machinae | §9 classification, §10 ladder |
| External promises | Codex Machinae | Boundary Contract Map (§8) |
| Work breakdown and sequencing | GSD | ROADMAP.md, per-phase PLAN.md |
| Session state and resumability | GSD | STATE.md, checkpoints |
| Agent dispatch and parallelism | GSD | Orchestrator + subagents |

---

## 3. Setup

### 3.1 Install both in the repository

1. Copy the [`playbook/`](../playbook/) directory (preferred for agent
   sessions — token-frugal) or the monolithic `codex-machinae.md` into the
   repository, per the [Quick start](../README.md#quick-start).
2. Install GSD and initialise it: `/gsd:new-project` for greenfield, or
   `/gsd:map-codebase` followed by `/gsd:new-project` on an existing repo.
   GSD creates `.planning/`; the playbook's documents live in `docs/` and the
   repository root. The two trees do not collide.

### 3.2 Wire the playbook into the agent configuration

The single highest-leverage step. The playbook already requires an agent
configuration file (§2.4 — `CLAUDE.md` or shared `AI-AGENTS.md`); GSD's
planner, executor, and reviewer subagents all read it. Add to it:

```markdown
## Engineering standard

This project follows Codex Machinae. Before planning or executing any task:

1. Read `playbook/core.md` (§§1–12). It is normative, not advisory.
2. Read the domain appendices and modules whose triggers have fired
   (currently active: <list them — e.g. D1, M2>). See §2.2.
3. Declared project-size profile: <Solo | Small | Large> (§2.5).
4. Phase success criteria MUST include the Definition of Done (§1.8) and the
   per-phase checklist items from Appendix A applicable to this profile.
5. Changes matching the never-auto-merge list (§9.3) MUST NOT be executed in
   unattended mode; stop and escalate.
```

From this point on, GSD's mechanical gates start enforcing the playbook's
definition of done, because every fresh-context subagent inherits these rules.

### 3.3 Declare the profile once, reuse it twice

The playbook's project-size profile (§2.5) and GSD's configuration both
modulate process weight. Align them:

| Playbook profile (§2.5) | Suggested GSD configuration |
|--------------------------|------------------------------|
| Solo | `budget`/`balanced` model profile, research optional, code review `quick` |
| Small | `balanced`, research on, plan verification on, code review `standard` |
| Large | `quality`, research on, plan verification on, code review `deep`, verify-work mandatory |

---

## 4. Mapping the lifecycle

The playbook's phases (§11) and GSD's workflow align cleanly:

| Playbook lifecycle (§11) | GSD command(s) | Notes |
|--------------------------|----------------|-------|
| Phase 0 — Ideation & requirements (§11.1) | `/gsd:new-project` (questioning → REQUIREMENTS.md → ROADMAP.md) | The PRD (template B.1) remains the normative requirements document; GSD's REQUIREMENTS.md is the operational checklist derived from it. Record architectural choices as ADRs (B.3), not only as CONTEXT.md decisions. |
| Phase 1 — Technical bootstrap (§11.2) | First GSD phase in ROADMAP.md | Make §11.2's outputs the phase's success criteria: directory structure, lint+CI, agent config, initial Boundary Contract Map, `.env.example`. |
| Phase 2 — Active development (§11.3) | Per-phase cycle: `/gsd:discuss-phase` → `/gsd:plan-phase` → `/gsd:execute-phase` → `/gsd:verify-work` | See §5 below for gate wiring. |
| Phase 3 — Maturity & maintenance (§11.4) | `/gsd:complete-milestone`, then outside GSD | GSD hands over at the milestone tag; M1 surveillance and §9–§10 remediation take over (§7 below). |
| Phase 4 — Major dependency upgrade (§11.5) | Dedicated GSD phase, manual mode only | §11.5 disables L1 automation; correspondingly, never run this phase under `gsd-autonomous`. |
| Phase R — Retrofit (§11.6) | `/gsd:map-codebase` + tiered phases | See §6 below. |

---

## 5. Wiring the gates

### 5.1 Definition of Done → phase success criteria

GSD's executor marks tasks complete when the plan's success criteria pass, and
its verifier audits the phase against the same criteria. Embed the playbook
there, at planning time — instruct the planner (via the agent config, §3.2
above) that every PLAN.md must carry, in addition to feature-specific criteria:

- Tests written per the applicable tiers of the pyramid (§5.1), and the
  coverage ratchet not regressed (§5.3 / tooling D.2).
- Lint rule-zero and complexity thresholds respected (§3.4–§3.5).
- CHANGELOG.md updated for any user-visible change (§6.3).
- Boundary Contract Map regenerated if any external promise changed (§8);
  cardinality guard green.
- If M2 is active: the per-PR security checklist (§M2.2) passes.

### 5.2 Code review depth → profile and modules

Map `/gsd:code-review` depth to risk: `quick` for Solo-profile internal
changes, `standard` as default, `deep` whenever M2 is active or the diff
touches a contract in the Boundary Contract Map with `risk_weight: high`.

### 5.3 UAT → acceptance criteria

`/gsd:verify-work` walks the built feature test by test. Feed it the user
stories' GIVEN–WHEN–THEN acceptance criteria (template B.2) rather than ad-hoc
prompts; its `{phase}-UAT.md` output then doubles as the playbook-required
acceptance evidence. (GSD-CC users get this alignment for free — its task
plans already carry BDD criteria.)

---

## 6. Autonomy governance: §9–§10 decide when GSD runs unattended

GSD's autonomy modes (manual / semi-auto / `gsd-autonomous`) have no native
risk model; the playbook supplies one. Translate the remediation ladder
(§10.1) into GSD operating modes:

| Classification (§9) | Playbook level | GSD mode |
|---------------------|----------------|----------|
| `safe` | L0 | `gsd-autonomous` permitted end-to-end |
| `additive` | L1 | Semi-auto: `--auto` planning, but human reviews before merge |
| `breaking` / `p0` / never-auto-merge match | L2 | Manual mode only; agent stops and escalates |

Two playbook mechanisms carry over directly:

- **Never-auto-merge list (§9.3).** Reproduce it verbatim in the agent config
  (§3.2, rule 5). An unattended GSD run that would touch endpoint removal,
  auth protocol, data-rewriting migrations, or a critical advisory must stop.
- **Circuit breaker (§10.3).** GSD's revision loops already cap iterations
  (escalate after 3 failed attempts); extend the same posture across runs — if
  unattended executions fail repeatedly on the same phase, degrade that phase
  to manual mode and produce a handover dossier (§10.4) rather than retrying.

---

## 7. Retrofit and the post-milestone handover

### 7.1 Existing projects: Phase R driven by GSD

Phase R (§11.6) and `gsd-map-codebase` are natural partners:

1. Run `/gsd:map-codebase` — its seven analysis documents (stack,
   architecture, conventions, testing, concerns…) are the raw material for
   the **debt-scoping audit**.
2. Fill the `RETROFIT_AUDIT.md` template (B.9) from that analysis.
3. Turn each adoption tier into a GSD phase: **T1 safety net** (coverage
   baseline, secrets audit, CI) → **T2 structure** (layout, agent config,
   CHANGELOG, contract map) → **T3 process** (surveillance, checklists,
   Definition of Done). T1 must complete before anything else executes —
   make it the first phase in ROADMAP.md.

### 7.2 Shipped milestones: activate what GSD does not cover

`/gsd:complete-milestone` ends with an audit, archives, and a git tag. That
tag is the handover point:

- Activate **M1 Surveillance** if the contract map has outbound contracts —
  the cron-driven agents (pkg-watch, api-probe, security-watch…) have no GSD
  equivalent and own the maintenance phase.
- Activate **M3 Release & Distribution** if D2/D3/D4/D6 is active: cadence,
  changelog automation, freeze windows.
- Findings from surveillance flow through §9 classification → §10
  remediation; fixes large enough to warrant planned work re-enter GSD as a
  phase in the next milestone.

---

## 8. Artefact correspondence

| Playbook artefact | Nearest GSD artefact | Relationship |
|-------------------|----------------------|--------------|
| PRD (`docs/prd/`, B.1) | PROJECT.md + REQUIREMENTS.md | PRD is normative; GSD files are its operational projection |
| User stories + AC (B.2) | Phase success criteria, UAT scripts | Feed B.2 criteria into PLAN.md and `/gsd:verify-work` |
| ADRs (`docs/adr/`, B.3) | CONTEXT.md locked decisions (GSD-CC: DECISIONS.md) | Promote significant CONTEXT.md decisions to ADRs; ADRs are append-only and survive milestone archival |
| Definition of Done (§1.8) | PLAN.md success criteria | Embedded at planning time (§5.1 above) |
| PROJECT_STATUS.md (§2.3) | STATE.md | Keep both; single-writer rule (§12.7.4) applies — GSD's orchestrator may update both, other agents read-only |
| CHANGELOG.md (§6.3) | — (no equivalent) | Playbook-only; make updating it a standing success criterion |
| Boundary Contract Map (§8) | INTEGRATIONS.md (descriptive only) | Playbook-only as an enforced artefact; regenerate via tooling D.1 |
| Coverage baseline (§5.3) | — (no equivalent) | Playbook-only; enforce via tooling D.2 in CI |

---

## 9. Boundaries and pitfalls

- **Do not let GSD artefacts substitute required documents.** SUMMARY.md is
  not a CHANGELOG entry; CONTEXT.md is not an ADR; INTEGRATIONS.md is not a
  contract map. The playbook's document set (§6) remains mandatory.
- **Two state files, one writer each.** PROJECT_STATUS.md (human-readable
  session note, §2.3) and STATE.md (machine-routable workflow state) coexist;
  under multi-agent operation apply the single-writer rule (§12.7.4) to both.
- **GSD is Claude Code-specific.** In mixed-LLM teams (§12.7.6), only the
  Claude agent drives GSD; `AI-AGENTS.md` remains the shared source of truth,
  and other agents interact through committed artefacts, not `.planning/`
  internals.
- **`.planning/` hygiene.** GSD's directory is operational state. Decide
  explicitly whether to track it; if tracked, exclude it from the playbook's
  documentation requirements (it is not part of §6's document set).
- **Unattended mode is a privilege the classification grants, not a default.**
  When in doubt about a change's bucket, it is L2 (§10.1: "everything is L2"
  is a valid adoption of the pattern).
