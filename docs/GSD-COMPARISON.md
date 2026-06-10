# Codex Machinae vs GSD — A Comparative Analysis

**Date:** 2026-06-10
**Compared versions:** Codex Machinae 2.0.0 (Draft) · GSD skill suite (`gsd-*`, ~70 skills) with notes on the GSD-CC variant
**Status:** Working analysis — not normative

---

## 1. Purpose

Both Codex Machinae and GSD (Get Shit Done) address the same problem space: how to
build and maintain software when AI agents are active collaborators rather than
autocomplete. They attack it from opposite ends, and the differences are
structural, not cosmetic. This document maps where they overlap, where they
diverge, and how they can be combined.

**One-sentence verdict:** Codex Machinae is a *process specification* (the
"what" and "to what standard"); GSD is an *execution engine* (the "how" and "in
what order"). They are complementary, not competing.

---

## 2. What each one is

### Codex Machinae

A prescriptive, LLM-agnostic playbook covering the full software lifecycle:
requirements (§1), structure (§2), code quality (§3), security (§4), testing
(§5), documentation (§6), CI/CD (§7), Boundary Contracts (§8), change
classification (§9), remediation (§10), lifecycle phases 0–4 plus retrofit
Phase R (§11), and AI-agent conventions (§12). Domain appendices (D1–D7) and
cross-cutting modules (M1–M4) activate by trigger. It is documentation: it does
not execute anything, hold runtime state, or orchestrate agents. Projects
implement its rules with their own tooling; Appendix D specifies contracts for
three reference tools (AST walker, coverage ratchet, surveillance scaffold).

### GSD

An executable workflow system installed as Claude Code skills. It drives a
three-tier hierarchy (milestones → phases → plans) through a repeating cycle:
**discuss → plan → execute → verify**. Its core idea is *context engineering*:
every stage runs in a fresh context window via specialised subagents
(`gsd-planner`, `gsd-executor`, `gsd-verifier`, `gsd-plan-checker`, mappers,
researchers, auditors), with a thin orchestrator that delegates aggressively.
All state lives in committed artefacts under `.planning/` (PROJECT.md,
REQUIREMENTS.md, ROADMAP.md, STATE.md, per-phase CONTEXT/RESEARCH/PLAN/SUMMARY/
UAT/REVIEW files). It enforces *that* decisions are made, documented, and
verified — it is agnostic about *what* the decisions are.

---

## 3. Comparison at a glance

| Axis | Codex Machinae | GSD |
|------|----------------|-----|
| **Nature** | Prescriptive process specification (a document) | Executable workflow engine (skills + subagents) |
| **Primary question** | "What standard must the work meet?" | "What is the next step, and who executes it?" |
| **Lifecycle coverage** | Full: requirements → development → deployment → maintenance → monitoring → retrofit | Development loop only: idea → roadmap → phased build → verify → milestone close |
| **Post-release operations** | Yes: surveillance agents (M1), dependency SLAs (M2.4), release engineering (M3), Phase 3/4 maintenance | No — ends at milestone completion and git tag |
| **State management** | Committed documents (PROJECT_STATUS.md, COMPATIBILITY.md, baselines); no runtime state machine | Explicit state machine: STATE.md as single source of truth, resumable checkpoints, handoffs |
| **Agent orchestration** | Conventions only (§12): autonomy levels, single-writer rules, handover protocol — no dispatch mechanism | Real orchestration: fresh-context subagents, wave-based parallelism, completion markers, revision loops |
| **Autonomy model** | Risk-based ladder L0/L1/L2 tied to change classification (§9–§10), with circuit breaker and handover dossier | Mode-based: manual / semi-auto / `gsd-autonomous`, with escalation and abort gates |
| **Testing** | Prescribes strategy: four-tier pyramid, coverage ratchet, contract tests, two-layer snapshots (§5) | Requires tests pass as a gate; prescribes no strategy, tiers, or coverage targets |
| **Security** | Prescribes requirements: input validation, secrets, M2 checklists, OWASP review, vulnerability SLAs | Optional audit agents (`gsd-security-auditor`, `gsd-secure-phase`); no mandatory standard |
| **CI/CD** | Prescribes a five-stage pipeline, config-as-code, forge adapter pattern (§7) | Local commits and tags only; CI integration out of scope |
| **Code quality** | Hard thresholds: complexity ≤ 15, nesting ≤ 4, lint rule-zero, naming conventions (§3) | Configurable code-review agent (quick/standard/deep); no fixed thresholds |
| **Documentation** | Required set: README, CHANGELOG, DEPENDENCIES, ADRs, runbooks, PRD (§6) | Produces its own planning artefacts; code/user documentation not prescribed |
| **External boundaries** | First-class: Boundary Contract Map, cardinality guard, surveillance triggers (§8, M1) | Not modelled — closest analogue is INTEGRATIONS.md from `gsd-map-codebase` (descriptive, not enforced) |
| **Change risk** | Nine classification buckets, never-auto-merge list, severity-driven remediation (§9–§10) | No change taxonomy; risk handled conversationally at escalation gates |
| **Scaling rule** | Project-size profiles Solo/Small/Large modulate checklist weight (§2.5) | Config toggles and model profiles (quality/balanced/budget) modulate workflow weight |
| **Existing projects** | Phase R retrofit protocol with T1/T2/T3 adoption tiers (§11.6) | `gsd-map-codebase` + `gsd-ingest-docs` bootstrap planning from an existing repo |
| **Multi-agent** | Coordination protocol §12.7: lead agent, scope partitioning, mixed-LLM via shared artefacts | Native: parallel subagents are the default execution model (single human session) |
| **Provider coupling** | LLM-agnostic by design (Claude, Gemini, GPT, local) | Claude Code-specific (skills, subagent types, `claude -p`) |
| **Adoption cost** | High without tooling (acknowledged in limitations; mitigated by Appendix D specs and size profiles) | Low — install skills, run `/gsd:new-project` |

---

## 4. Where they genuinely overlap

The overlap is narrower than it first appears, but real:

1. **Requirements before code.** Codex Machinae's PRD + user stories +
   acceptance criteria (§1, templates B.1–B.2) parallels GSD's
   PROJECT.md → REQUIREMENTS.md → ROADMAP.md pipeline. Both refuse to start
   building from a vague prompt.
2. **Decision records.** ADRs (§1.5, append-only) vs GSD's locked decisions in
   CONTEXT.md (and the append-only DECISIONS.md in GSD-CC). Same intent —
   decisions survive context loss — different granularity and ceremony.
3. **Session state in committed files.** PROJECT_STATUS.md updated every
   session (§2.3) vs STATE.md updated after every step. GSD's version is
   richer (machine-routable); the playbook's is lighter (human-readable note).
4. **Verification loops with iteration caps.** The playbook's L1 correctness
   gate and circuit breaker (3 open PRs / 5 failures → degrade to L2) rhymes
   with GSD's plan-checker and verifier loops (max 3 iterations → escalate).
   Both encode the same insight: unsupervised retry must have a ceiling.
5. **Agents ground on artefacts, not memory.** §12.2 (ground on live data
   before fixing) and GSD's fresh-context principle are two formulations of
   the same rule: never trust accumulated conversational context.

---

## 5. Where they diverge structurally

### 5.1 Content standards vs workflow mechanics

This is the central divide. Codex Machinae answers questions GSD deliberately
leaves open: which test tiers exist, what coverage may do (only rise), how
secrets are handled, what a commit message looks like, when a change may
auto-merge. GSD answers questions the playbook deliberately leaves open: who
plans, in which context window, in what order, with which artefact as input,
and what happens when verification fails at 2 a.m. in unattended mode.

A team running only GSD ships fast with full traceability of *process* but no
floor on *engineering quality* — nothing stops a phase from completing with 0%
coverage and secrets in code, provided the plan's own criteria pass. A team
running only Codex Machinae has a high floor but must hand-roll all the
mechanics: there is no command that produces a compliant PRD or dispatches the
remediation workflow.

### 5.2 Lifecycle horizon

GSD's world ends at `/gsd:complete-milestone` (audit, archive, tag). Codex
Machinae's most distinctive machinery starts roughly there: M1 surveillance
agents probing upstream dependencies on cron, compatibility records, heartbeat
signals, classifier retrospectives, Phase 4 major-upgrade lockdown. The
playbook treats *maintenance under autonomous agents* as the hard problem; GSD
treats *construction under autonomous agents* as the hard problem.

### 5.3 Risk modelling

Codex Machinae classifies every change into nine buckets with a severity and a
never-auto-merge list, and derives the autonomy level (L0/L1/L2) from the
classification. GSD has no change taxonomy: in autonomous mode the agent
escalates when *it* judges something ambiguous, and approval gates (GSD-CC's
APPROVALS.jsonl) are coarse-grained. The playbook's model is auditable and
deterministic; GSD's is adaptive and judgment-based. For regulated or
security-sensitive work, the playbook's model is the stronger one; for greenfield
iteration, GSD's is faster.

### 5.4 Boundary Contracts have no GSD counterpart

The Boundary Contract Map (§8) — a generated JSON inventory of every external
promise, with risk weights, test-coverage flags, and a CI cardinality guard —
is the playbook's most original mechanism and has no analogue in GSD.
GSD's INTEGRATIONS.md (from `gsd-map-codebase`) describes integrations once,
for context; it is not regenerated, not diffed, and gates nothing.

### 5.5 Portability vs leverage

Codex Machinae works with any agent (and survives switching providers); the
price is that nothing runs by itself. GSD extracts maximum leverage from one
specific runtime (Claude Code subagents, fresh sessions, parallel waves); the
price is lock-in to that runtime.

---

## 6. The GSD-CC variant

GSD-CC (`.gsd/` directory, slices/tasks instead of phases/plans) moves a
noticeable step *towards* Codex Machinae's philosophy while remaining an
execution engine:

- **BDD acceptance criteria** (Given/When/Then) per task — close to the
  playbook's user-story template B.2.
- **Explicit task boundaries** ("DO NOT CHANGE" lists, checked at unify) — a
  lightweight cousin of the never-auto-merge list (§9.3).
- **Mandatory UNIFY reconciliation** per slice (plan vs actual, deviations,
  boundary violations) — the closest thing in the GSD family to a
  classification-style audit gate.
- **Append-only DECISIONS.md and cost tracking (COSTS.jsonl)** — auditability
  features in the playbook's spirit.

Even so, GSD-CC still prescribes no testing strategy, security floor, or CI/CD
standard. The divide of §5.1 holds for both variants.

---

## 7. Using them together

The frameworks compose cleanly because they own disjoint layers:

| Layer | Owner |
|-------|-------|
| What "done" and "good" mean (quality floor, security, testing, docs, CI/CD) | Codex Machinae |
| How work moves from idea to verified code (sessions, subagents, artefacts, state) | GSD |

Practical integration points:

1. **Inject the playbook as the standard.** Reference Codex Machinae (or the
   relevant Core sections + active domains/modules) from the project's
   `CLAUDE.md` / `AI-AGENTS.md` (§2.4). GSD's planner and executor then
   inherit the playbook's rules as constraints, and GSD's gates start
   enforcing the playbook's definition of done.
2. **Map the playbook's Definition of Done (§1.8) into GSD acceptance
   criteria.** Phase plans whose success criteria embed the §5 test tiers and
   §3.5 thresholds turn GSD's mechanical gates into Codex Machinae compliance
   checks.
3. **Use Phase R alongside `gsd-map-codebase`.** On an existing repo, GSD's
   mappers produce the codebase analysis; the retrofit audit (B.9) consumes it
   to plan T1/T2/T3 adoption — each tier becoming a GSD phase.
4. **Let the change classification govern GSD autonomy.** Run
   `gsd-autonomous` only for work that classifies as `safe`/`additive`
   (L0/L1); force manual mode for anything on the never-auto-merge list (L2).
5. **Hand over at milestone completion.** Where GSD stops (tag created),
   activate M1/M3: surveillance manifests, release cadence, dependency SLAs.

The reverse composition also holds: the playbook's acknowledged weakness is
mechanical adoption cost (limitations.md, item 1), and GSD is precisely the
kind of machinery that lowers it.

---

## 8. Summary judgement

| If you need… | Reach for… |
|--------------|-----------|
| A repeatable way to drive an AI agent from idea to working code today | GSD |
| An engineering quality floor that survives agent and provider churn | Codex Machinae |
| Unattended building of a greenfield milestone | GSD (`gsd-autonomous`) |
| Unattended *maintenance* of a shipped system | Codex Machinae (M1 + §9–§10) |
| Both — which is the realistic case for any project that ships | GSD as the engine, Codex Machinae as the law it enforces |

Neither subsumes the other. GSD without a standard produces well-orchestrated
work of unspecified quality; Codex Machinae without an engine produces a
high standard that costs discipline to meet. Together, the playbook defines
the contract and GSD executes it.
