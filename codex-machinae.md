# Codex Machinae

**Version:** 2.0.0 — Draft
**Last updated:** 2026-04-15
**Scope:** Framework for developing, testing, deploying, maintaining, and monitoring software projects.

This playbook defines the entire lifecycle of a software project: from requirements gathering through to deployment and continuous dependency monitoring. It is designed for independent developers and small teams operating with autonomous agents (Claude Code, Ruflo, or equivalents).

---

## Table of Contents

### Part I — Core (universal)

1. [Requirements and planning](#1-requirements-and-planning)
2. [Project structure](#2-project-structure)
3. [Code quality](#3-code-quality)
4. [Security requirements](#4-security-requirements)
5. [Testing strategy](#5-testing-strategy)
6. [Documentation](#6-documentation)
7. [CI/CD and deployment](#7-cicd-and-deployment)
8. [Boundary Contracts](#8-boundary-contracts)
9. [Change classification](#9-change-classification)
10. [Remediation workflow](#10-remediation-workflow)
11. [Project lifecycle](#11-project-lifecycle)
12. [Conventions for AI agents](#12-conventions-for-ai-agents)

### Part II — Domain Appendices (activate per project type)

- [D1 Web Service](#d1-web-service)
- [D2 Library / SDK](#d2-library--sdk)
- [D3 CLI Tool](#d3-cli-tool)
- [D4 Embedded / Firmware](#d4-embedded--firmware)
- [D5 ML / Data Pipeline](#d5-ml--data-pipeline)
- [D6 Mobile App](#d6-mobile-app)
- [D7 Static Site / Frontend-only](#d7-static-site--frontend-only)

### Part III — Cross-cutting Modules (activate by trigger)

- [M1 Surveillance](#m1-surveillance)
- [M2 Security-sensitive](#m2-security-sensitive)
- [M3 Release & Distribution](#m3-release--distribution)
- [M4 Classification & Taxonomy](#m4-classification--taxonomy)

### Appendices

- [A — Per-phase checklists](#appendix-a--phase-checklists)
- [B — Templates](#appendix-b--templates)
- [C — Glossary](#appendix-c--glossary)

---

# PART I — CORE (universal)

The Core applies to every project regardless of type. Domain Appendices (Part II) and
Cross-cutting Modules (Part III) add content on top of the Core when their activation trigger
fires. When the Core and a module disagree, the Core wins unless the module explicitly marks
the override.

---

## 1. Requirements and planning

Every feature, bugfix, or project begins with written requirements. Code without documented requirements is technical debt from the first commit.

### 1.1 Requirements document hierarchy

```
PRD (Product Requirements Document)
 └── Epic
      └── User Story
           └── Acceptance Criteria
                └── Technical task
```

Every level is traceable to the one above it. A technical task without a referenced User Story is a warning signal — it could be unnecessary work or scope creep.

### 1.2 PRD (Product Requirements Document)

The PRD is the highest-level document. It defines the **what** and the **why**, never the **how** (that is architecture). Minimum content:

| Section | Content | Required |
|---------|---------|----------|
| **Status and ownership** | Draft version, author, date of last update | Yes |
| **Purpose and scope** | What the system guarantees and what it does NOT cover | Yes |
| **Stakeholders and users** | Who uses the system and in what context | Yes |
| **Functional requirements** | What the system must do, organised by area | Yes |
| **Non-functional requirements** | Performance, security, accessibility, scalability | Yes |
| **Architectural constraints** | Mandatory technologies, integrations, limitations | Yes |
| **Boundaries with other systems** | What is the responsibility of other repos/services/teams | Yes |
| **Open questions** | Known unknowns, with owner and resolution strategy | Yes |
| **Architectural decisions** | Referenced ADR (Architecture Decision Records) | Recommended |
| **Later-phase work** | Work explicitly deferred, with justification | Recommended |
| **Appendices** | Source documents, external references | Recommended |

**Pre-implementation checklist.** Every PRD MUST include a checklist at the beginning of the document listing decisions already made and confirmed. The implementer verifies it before writing any code. If an item on the checklist does not match the code in the repository, implementation halts until the discrepancy is resolved.

### 1.3 User story

Standard format:

```
As a [user role]
I want [action]
So that [benefit]
```

Every User Story MUST have:

- **Unique ID** — format `US-<area>-<number>` (e.g. `US-AUTH-001`)
- **Priority** — P0 (blocker), P1 (must-have for release), P2 (should-have), P3 (nice-to-have)
- **Estimate** — in hours or story points, updated after the first working session
- **Acceptance criteria** — list of verifiable conditions that define "done"
- **Dependencies** — reference to other User Stories that must be completed first
- **Link to PRD** — the PRD section that this story implements

### 1.4 Acceptance criteria

Each criterion is a binary condition (pass or fail). Format:

```
GIVEN [initial context]
WHEN [user or system action]
THEN [expected result]
```

Acceptance criteria become tests. If a criterion cannot be translated into an automated test, it must be rewritten until it can.

### 1.5 Architecture Decision Records (ADR)

Every significant architectural decision is documented in an ADR. Minimum format:

```markdown
# ADR-<number>: <title>

**Status:** proposed | accepted | deprecated | superseded by ADR-<n>
**Date:** YYYY-MM-DD
**Context:** Why this decision is necessary.
**Decision:** What was decided.
**Consequences:** Positive and negative impact of the decision.
**Alternatives rejected:** What was considered and discarded, with justification.
```

ADRs are **append-only** — they are never deleted; they are superseded by new ADRs that reference them.

### 1.6 Backlog management

The backlog is an ordered list by priority. Rules:

- Every item has a status: `todo`, `in-progress`, `blocked`, `review`, `done`
- No item remains `in-progress` for more than one week without an update
- `blocked` items must have a reason and an owner responsible for unblocking
- `done` items must have all Acceptance Criteria satisfied and tests written
- The backlog is reviewed weekly; P3-priority items older than 90 days are archived or deleted

### 1.7 State-of-the-art research

Before implementing a feature, a module, or an integration, the system must prompt the user to conduct state-of-the-art research. This applies both to the project as a whole and to individual parts.

#### 1.7.1 When research is mandatory

| Trigger | What to research | Expected output |
|---------|-----------------|-----------------|
| **New project** (Phase 0) | Existing similar projects, established frameworks, dominant architectural patterns in the domain | Report covering: existing solutions, pros/cons, justified decision on build vs adopt vs fork |
| **Significant new feature** (P0 or P1) | Reference implementations, specialised libraries, documented patterns | "State of the art" section in the User Story with links and evaluation |
| **New dependency** | Available alternatives, maturity/community/maintenance comparison, licence | Comparative table in `DEPENDENCIES.md` with justification for the choice |
| **Technology choice** (language, framework, database) | Recent benchmarks, adoption trends, case studies in the domain | ADR with "Alternatives rejected" section populated from real research |
| **Architectural refactoring** | Current patterns in the industry, documented migrations from other projects | ADR with references to similar experiences |

#### 1.7.2 What to research for each component

For every significant part of the project, research should cover:

**Existing solutions.** Does a library, service, or open-source project already exist that does what I am about to write? If so, is it more mature, tested, and maintained than what I could produce? Rule: do not reinvent the wheel unless the existing wheels are not suited to the road ahead — and document why they are not in the ADR.

**Patterns and best practices.** How do mature projects in the same domain solve this problem? Which architectural patterns have emerged as dominant? Which anti-patterns have been documented? Search: engineering blog posts from relevant companies, recent conferences, RFCs and proposals in reference repositories.

**Technology evolution.** Is the technology I am using still the best choice? Are there newer alternatives that resolve known issues with the current technology? Is the community active or in decline? Search: GitHub star trends, release frequency, number of active contributors, open vs closed issues.

**Experience from others.** Who else has done something similar and what did they learn? What mistakes can I avoid? Search: public post-mortems, case studies, technical forum threads, conference talks.

#### 1.7.3 How the AI agent supports research

The AI agent MUST proactively suggest research at the following moments:

**At the start of a new project:** "Before implementing, shall I research the state of the art for [project domain]? I can look for similar projects, established frameworks, and architectural patterns used in the industry."

**When a new dependency is added:** "You are about to add [library]. Would you like me to check whether there are more recent or mature alternatives? I can compare: maturity, update frequency, community size, licence, and any known issues."

**When an architectural choice is proposed:** "This decision has a long-term impact. Would you like me to look at how other projects in the [X] domain have approached the same problem? I can find public ADRs, engineering blog posts, and case studies."

**When the project enters a new phase:** "The project is about to tackle [new area]. Would you like me to carry out a state-of-the-art check on the technologies and patterns used in this area?"

**During periodic review:** "It has been [N] months since the last state-of-the-art research for [component]. Some of the technologies in use may have better alternatives or significant updates. Would you like me to carry out a check?"

#### 1.7.4 Research register

Document each research exercise in `docs/research/`:

```
docs/research/
├── YYYY-MM-DD-<topic>.md          # Research report
├── YYYY-MM-DD-<topic>.md
└── index.md                        # Index with date, topic, outcome
```

Report format:

```markdown
# Research: [Topic]

**Date:** YYYY-MM-DD
**Trigger:** new project | new feature | new dependency | periodic review
**Author:** human | AI agent | both

## Research question
[What we wanted to know]

## Solutions found
[List with pros/cons/maturity/licence]

## Recommendation
[What to do and why]

## Sources
[Links to documentation, blogs, repositories, papers]

## Decision taken
[What was decided and reference to the ADR if present]
```

#### 1.7.5 State-of-the-art research agent (State-of-the-Art Scout)

In addition to the dependency surveillance agents (M1.1), the playbook includes an agent dedicated to state-of-the-art research. This agent operates differently from the others: it does not monitor a single dependency, but scans the technological landscape surrounding the project.

**Frequency:** quarterly for stable components, monthly for components under active development.

**What it does:**

1. **Technology health check.** For every significant technology in the project (language, framework, database, key libraries), verifies: latest release, release frequency over the past year, trend of open issues, state of documentation, any deprecation or end-of-life announcements.

2. **Alternative scanning.** Searches for new libraries or services that solve the same problem as an existing dependency, but with a different or improved approach. It does not suggest switching — it flags that the alternative exists and leaves the decision to the human.

3. **Pattern evolution.** Verifies whether the architectural patterns used in the project are still considered best practice or whether the community has moved towards different approaches. Searches: updates to official style guides, new RFCs in reference repositories, recent talks from key conferences.

4. **Security landscape.** Verifies whether the project's security practices are aligned with current recommendations (OWASP, NIST, CIS benchmarks). Searches: new vulnerability classes, new scanning tools, updates to recommendations.

5. **Ecosystem health.** Evaluates the overall health of the ecosystem: is the community growing or in decline? Are there significant forks? Are there controversies (licence, governance, ownership) that could impact the project?

**Output:** a report in `docs/research/` with classified findings:

| Finding | Meaning | Action |
|---------|---------|--------|
| `healthy` | The technology is active, maintained, with no superior alternatives | None |
| `watch` | An emerging alternative or trend to monitor exists | Add to the next research cycle |
| `evaluate` | An alternative is mature enough to warrant serious evaluation | Create an ADR with comparison |
| `migrate` | The technology is in decline, deprecated, or has significant issues | Plan migration in the backlog |
| `urgent` | End-of-life, critical vulnerability without a patch, hostile fork | Immediate action |

### 1.8 Definition of Done

The Definition of Done is split into two layers. **Core DoD** applies to every item in every project, regardless of domain, phase, or tooling. **Contextual DoD** applies only when its precondition holds — the item need not satisfy a contextual check when the trigger has not fired.

An item is "done" when all applicable checks below pass.

#### 1.8.1 Core DoD (process integrity — always applies)

- [ ] The planned change is actually complete — no half-finished edits, no placeholder stubs left behind
- [ ] Commit messages follow Conventional Commits (§3.3)
- [ ] `PROJECT_STATUS.md` is updated
- [ ] Protected paths have not been modified without prior approval (agent-config protected-paths list)
- [ ] Cross-references (§…) still resolve; broken links fixed or removed

#### 1.8.2 Contextual DoD (applies when the precondition holds)

| Check | Precondition |
|-------|--------------|
| Code complies with style conventions (§3) | Code was written or modified |
| All Acceptance Criteria are satisfied | The item is backed by a User Story (§1.3) |
| Tests are written and pass (§5) | The project has adopted a testing strategy |
| Coverage has not dropped below the threshold (§5.3) | A coverage threshold is declared |
| CI is green | CI is configured for the project |
| Documentation is up to date (§6) | External-facing behaviour changed |
| Code has been reviewed (self- or peer-) | The project's practice requires review |
| Boundary Contract Map updated (§8) | A contract was added, removed, or changed |
| State-of-the-art research has been conducted (§1.7) | A §1.7 trigger fired for this item |
| ADR written (§1.5) | A significant architectural decision was taken |

An agent MUST declare, for each contextual check, whether the precondition held; checks whose precondition did not hold are recorded as `n/a` rather than silently skipped. This keeps the audit trail explicit.

---

## 2. Project structure

The playbook follows an **emergent architecture** principle: a project starts with the smallest possible footprint and grows only when justified by its PRD and phase. Scaffolding folders up front — "just in case" — is waste and locks the project into structure it may never need.

### 2.1 Minimum Core of Existence

Every project MUST contain, at initialisation, only these files:

```
project-root/
├── README.md                    # One-paragraph orientation
├── PROJECT_STATUS.md            # Current session state (§2.3)
└── <agent-config>               # Rules for the AI agent(s) working on the project (§2.4)
```

Nothing else is mandatory at Phase 0. Every further folder or file is introduced through the Emergent Expansion Protocol (§2.2) when a trigger fires.

### 2.2 Emergent Expansion Protocol

Rather than creating folders defensively, the AI agent proposes expansions as the PRD and the project evolve. When a trigger fires, the agent MUST surface a proposal in this form:

> "I suggest adding `<path>` to cover <concern> because <trigger>. Cost of omission: <what breaks if we don't>."

The human accepts, rejects, or defers. No folder is created without an accepted proposal.

**Expansion catalogue (non-exhaustive).** Folders are added only when their trigger fires:

| Path | Trigger | Covers |
|------|---------|--------|
| `docs/prd/00-prd.md` | A PRD is being written (always, Phase 0 of any non-trivial project) | Requirements |
| `docs/adr/` | First architectural decision needs recording | Decision history |
| `docs/api/` | Project exposes or consumes a programmatic API | API surface |
| `docs/runbooks/` | Project is deployed to any environment | Operational procedures |
| `docs/research/` | State-of-the-art research is triggered (§1.7) | Research register |
| `src/`, `tests/` | Code is about to be written | Implementation |
| `scripts/` | First automation script is needed | Local tooling |
| `ci/` | Automated checks are enabled | CI/CD configuration |
| `ci/adapters/<forge>/` | A specific forge is adopted (GitHub, GitLab, …) | Forge-specific glue |
| `DEPENDENCIES.md` | First external runtime dependency is added | Dependency contracts |
| `CHANGELOG.md` | Project reaches its first release (v0.1.0+) | Release history |
| `COMPATIBILITY.md` | Boundary Contract Map is populated (§8) | Generated compatibility status |
| `compat-data/`, `compatibility/`, `surveillance/` | Surveillance agents are activated (M1.1) | External dependency monitoring |
| `.config/` | Linting/formatting rules diverge from tool defaults | Tooling configuration |

**Rule:** no folder without a fired trigger. Empty scaffolds and `.gitkeep` files are forbidden.

**Rule:** the agent also proposes **removal** when a folder loses its trigger (e.g. last surveillance agent removed → `surveillance/` can be archived).

### 2.3 PROJECT_STATUS.md

Updated at every working session. Four fixed sections:

```markdown
## Objective
What the project must achieve in this phase.

## Modified Files
List of files modified in the last session, with reason.

## Logical State
Current status: what works, what does not, what is blocked.

## Next Action
The next concrete action to perform.
```

### 2.4 Agent configuration

Operational rules for the AI agent(s) live in one of two layouts, depending on how many agents collaborate on the project:

**Single-agent project.** A single file (e.g. `CLAUDE.md`, `GEMINI.md`) contains all rules.

**Multi-agent project.** Rules are split into two layers:

- `AI-AGENTS.md` — shared source of truth for all agents. When a rule here conflicts with an agent-specific file, this file wins.
- `CLAUDE.md`, `GEMINI.md`, … — per-agent files covering only agent-specific syntax, tool use, and permissions. They must not contradict `AI-AGENTS.md`.

Whichever layout is used, the configuration MUST cover:

- Language and writing style (e.g. British English, active voice, short sentences)
- List of forbidden words, if any
- Scope of permitted modifications per autonomy level (L0/L1/L2 — see §10)
- Naming conventions for branches, commits, files
- Protected paths (files the agent cannot modify without human confirmation)
- Editorial rules (max line length, punctuation constraints, etc.)

---

## 3. Code quality

### 3.1 Architectural principles

Every project MUST adhere to these principles regardless of language:

**Separation of concerns.** Every module has a single, well-defined responsibility. Code that communicates with external APIs lives in a separate adapter/client layer, apart from business logic and the UI.

**Dependency inversion.** High-level modules do not depend on low-level modules — both depend on abstractions (interfaces, types, contracts). This makes the code testable and the client layer replaceable.

**Fail fast.** Errors are detected and reported as early as possible. Invalid input is rejected at the boundary, not propagated silently.

**Immutability by default.** Prefer immutable data structures and pure functions. Mutable state is confined to explicit store/state managers.

**Explicit over implicit.** No hidden magic: no undeclared global state, no side effects in getters, no circular imports.

### 3.2 Naming conventions

| Element | Convention | Example |
|----------|------------|---------|
| File | kebab-case | `user-profile.ts`, `auth-client.py` |
| Class/Component | PascalCase | `UserProfile`, `AuthClient` |
| Function/method | camelCase (JS/TS), snake_case (Python) | `getUserById()`, `get_user_by_id()` |
| Constant | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT`, `API_BASE_URL` |
| Environment variable | SCREAMING_SNAKE_CASE with project prefix | `ARC_CORTEX_URL`, `APP_SECRET_KEY` |
| Branch | `<type>/<id>-<short-description>` | `feat/US-AUTH-001-login-flow` |
| Commit | Conventional Commits | `feat(auth): add login endpoint` |
| Test file | Same name as the tested file + `.test` or `.spec` | `auth-client.test.ts` |

### 3.3 Conventional Commits

Every commit message follows the format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Permitted types:

| Type | When to use it |
|------|--------------|
| `feat` | New feature |
| `fix` | Bugfix |
| `docs` | Documentation only |
| `style` | Formatting, semicolons, etc. (no logic change) |
| `refactor` | Code change that neither adds a feature nor fixes a bug |
| `test` | Adding or modifying tests |
| `chore` | Build, CI, dependencies, tooling |
| `perf` | Performance improvement |
| `ci` | Changes to the CI/CD pipeline |
| `revert` | Revert of a previous commit |
| `compat` | Change related to compatibility with external dependencies |

The `BREAKING CHANGE:` footer is mandatory for any change that breaks backward compatibility.

### 3.4 Linting and formatting

Every project MUST have:

- **Linter** configured and integrated into CI. CI fails if there are lint errors.
- **Formatter** configured with rules identical to the linter. No debate on style: the formatter decides.
- **Pre-commit hook** (optional but recommended) that runs lint + format before every commit.

Recommended configuration by language:

| Language | Linter | Formatter | Config file |
|-----------|--------|-----------|-------------|
| TypeScript/JavaScript | ESLint (flat config) | Prettier | `eslint.config.js`, `.prettierrc` |
| Python | Ruff (lint + format) | Ruff | `ruff.toml` or `pyproject.toml` |
| Rust | Clippy | rustfmt | `clippy.toml`, `rustfmt.toml` |
| Go | golangci-lint | gofmt | `.golangci.yml` |
| Bash | ShellCheck | shfmt | `.shellcheckrc` |

**Rule zero:** no commit enters the repo with lint warnings. A warning is an error.

### 3.5 Complexity and metrics

Thresholds that CI MUST enforce:

| Metric | Threshold | Action if exceeded |
|---------|--------|-------------------|
| Cyclomatic complexity per function | ≤ 15 | CI fail |
| Lines per function | ≤ 50 (indicative) | Warning |
| Lines per file | ≤ 400 (indicative) | Warning |
| Nesting depth | ≤ 4 levels | CI fail |
| Parameters per function | ≤ 5 | Warning, suggest options object |
| Circular imports | 0 | CI fail |
| `any` type (TypeScript) | 0 in production | CI fail (permitted in tests with justification) |
| `// @ts-ignore` or `# type: ignore` | 0 in production | CI fail (permitted with an explanatory comment) |

### 3.6 Error handling

Universal rules:

- **Never swallow errors silently.** Every `catch` must log, rethrow, or handle explicitly. An empty `catch` is a bug.
- **Typed errors.** Define error classes/types for every domain of the application. Do not use strings as errors.
- **Error boundary.** Every layer of the architecture (UI, business logic, adapter, infra) has its own error boundary that translates errors from the lower layer into errors meaningful to the upper layer.
- **Retry with backoff.** Calls to external services must have retry with exponential backoff and a maximum number of attempts. Never infinite retry.
- **Explicit timeouts.** Every external call has a configured timeout. No call waits indefinitely.

### 3.7 Dependency management

- **Lock file** always committed (`package-lock.json`, `Pipfile.lock`, `Cargo.lock`, `go.sum`).
- **Exact versions** for direct production dependencies. Ranges (`^`, `~`) permitted only for development dependencies.
- **Regular audit.** `npm audit`, `pip-audit`, `cargo audit` run in CI on every PR.
- **Intentional updates.** Dependencies are not updated "because a new version is available" — they are updated when there is a reason (bugfix, security patch, required feature). An update is a tracked task, not a side effect.
- **Phantom dependencies.** CI verifies that there are no imports of packages not declared in the dependencies. Tools: `depcheck` (npm), `deptry` (Python).

### 3.8 Branching strategy

**Trunk-based development** for individual developers and small teams:

- `main` is always deployable
- Short-lived feature branches (max 3–5 days)
- No `develop` branch — it is unnecessary overhead for small teams
- Branch naming: `<type>/<id>-<description>` (e.g. `feat/US-AUTH-001-login`)
- Merge via squash (one commit per feature branch)
- Tags for releases: `v<major>.<minor>.<patch>`

---

## 4. Security requirements

### 4.1 Fundamental principles

**Defence in depth.** No single control is sufficient. Every layer validates its own inputs independently.

**Least privilege.** Every component has only the minimum permissions necessary. API tokens, database users, file system access — everything is reduced to the minimum.

**Zero trust on input.** All input is hostile until proven otherwise: query parameters, request bodies, headers, file uploads, environment variables, data from external APIs.

### 4.2 Input validation

Every entry point of the application MUST validate input:

| Layer | What to validate | How |
|-------|--------------|------|
| **API endpoint** | Type, format, range, length of every parameter | Schema validation (Zod, Pydantic, JSON Schema) |
| **UI form** | Format, length, permitted characters | Client-side + server-side validation (never client-only) |
| **File upload** | Real MIME type (not just extension), size, content | Magic bytes check, antivirus if available |
| **Database query** | Query parameters, injection | Prepared statement / parameterised query (never string concatenation) |
| **Data from external APIs** | Response schema, mandatory fields, types | Same validation as user input — an external API can be compromised |

**Rule:** validation is declarative (schema), not imperative (chain of `if` statements). A schema is testable, documentable, and reusable.

### 4.3 Secrets management

| Rule | Detail |
|--------|----------|
| **Never in code** | No secrets in source files, commits, or logs. `.gitignore` includes `.env`, `*.key`, `*.pem` |
| **Environment variables** | Primary method for secrets in local and CI environments |
| **Secret manager** | For production: GitHub Secrets, Vault, AWS SSM, or equivalent |
| **Rotation** | Every secret has an expiry date. Rotation is automated or scheduled |
| **Audit** | Every access to a secret is logged. If a secret is compromised, it must be rotated immediately |
| **`.env.example`** | The repo contains a `.env.example` with variable names (without values) and explanatory comments |

Authentication, authorisation, per-PR security checklist, and OWASP Top 10 coverage are handled by M2 Security-sensitive, which activates whenever the project handles authentication, authorisation, or PII; serves untrusted clients over a network; or processes attacker-controlled input.

---

## 5. Testing strategy

### 5.1 Testing pyramid

```
          ┌─────────┐
          │   E2E   │  Few, slow, costly. Validate complete user flows.
         ┌┴─────────┴┐
         │Integration │  Medium. Verify that modules work together.
        ┌┴───────────┴┐
        │  Scenarios   │  Contract tests against real or emulated services.
       ┌┴─────────────┴┐
       │     Unit       │  Many, fast, cheap. One function, one behaviour.
       └────────────────┘
```

| Tier | What it tests | Environment | Speed | Quantity |
|------|-----------|----------|----------|----------|
| **Unit** | Single function, pure logic | In-memory, full mock | < 1s per test | Hundreds |
| **Scenario** | Contract with external service | Emulator or real container | < 5s per test | Dozens |
| **Integration** | Interacting modules | Real container, real database | < 30s per test | Dozens |
| **E2E** | Complete user flow | Full stack, real browser | < 2min per test | A handful |

### 5.2 Rules for each tier

**Unit tests:**
- Every public function has at least one test
- Test the behaviour, not the implementation — if a refactor breaks the test but not the behaviour, the test is wrong
- No external dependencies (network, file system, database) — everything mocked
- Naming: `describe('functionName', () => { it('should <behaviour> when <condition>') })`

**Scenario/Contract tests:**
- Every contract in the Boundary Contract Map has at least one contract test
- Validation uses JSON Schema with `additionalProperties: true` (new fields do not break it)
- Fixtures are generated from real interactions, not written by hand
- Assertion discipline follows §5.6 (set-based when order is not part of the contract)

**Integration tests:**
- Every critical flow (login, main CRUD, payment) has at least one integration test
- Tests create their own data and clean it up — no dependency on pre-existing state
- Dynamic port binding for parallel containers — no hard-coded ports

**E2E tests:**
- Coverage of critical user flows (happy path + main error paths)
- Tools: Playwright (web), Detox (mobile), or equivalent
- Automatic retry for flaky tests (max 2 retries), but flaky tests must be fixed, not ignored
- Screenshot/video on failure for debugging

### 5.3 Coverage

**Ratchet model:** coverage can only increase, never decrease.

| Metric | Minimum threshold | Enforcement |
|---------|--------------|-------------|
| Line coverage | Defined in the baseline file, ratchet up-only | CI fail if it drops |
| Branch coverage | Defined in the baseline file, ratchet up-only | CI fail if it drops |
| Per-file coverage | No new file below 70% | CI fail |
| Coverage delta on PR | ≥ 0% (the PR cannot lower coverage) | CI fail |

**Baseline file:** `coverage-baseline.json` in the project root. Contains per-file coverage for the current state. CI compares and fails if any key decreases.

**Escape valve:** a PR may lower coverage only with a footer in the commit message explaining the reason:

```
Low-Coverage-Reason: Refactor of auth-client.ts — tests in follow-up PR #123
```

The escape valve is tracked and reviewed weekly. No escape valve may remain open for more than 2 weeks.

### 5.4 Test data strategy

- **Inline creation.** Tests create the data they need inline, not from shared fixture files. This makes every test self-documenting and independent.
- **Factory pattern.** For complex data, use factory functions that produce valid objects with sensible defaults and targeted overrides.
- **Golden files.** Only for true snapshot testing (UI rendering, rendered documents). For API and data contracts prefer schema-primary validation (§5.7); golden files there couple tests to incidental output ordering and drift silently. Updated explicitly with a flag (`--update-snapshots`), never silently.
- **Seed script.** For development databases, a deterministic script that populates realistic data. Separate from the tests.

### 5.5 Tests in CI

| Trigger | Tiers executed | Timeout | Parallelism |
|---------|-------------|---------|-------------|
| Push to feature branch | Unit + lint | 5 min | Maximum |
| PR towards main | Unit + scenario + integration | 15 min | Per-tier |
| Merge to main | Unit + scenario + integration + E2E | 30 min | Per-tier |
| Scheduled (nightly) | All + full compat matrix | 60 min | Per-slot |
| Release tag | All + smoke tests on staging | 45 min | Sequential |

### 5.6 Assertion discipline: set-based vs sequence-based

Before writing an assertion, decide which of the two shapes the contract actually guarantees; the wrong choice turns every unrelated reorder into a red build.

| Shape | Use when | Assertion form |
|-------|----------|----------------|
| **Set-based** | Order is not part of the contract (listings without `ORDER BY`, parallel fan-in, unordered collections) | Compare as sets or multisets; assert membership and cardinality, not position |
| **Sequence-based** | Order is part of the contract (sorted endpoints, pagination, event streams, log replays) | Compare as ordered lists; any position change is a real failure |

Flakiness from "wrong shape" assertions must be fixed by changing the assertion, not by pinning the implementation to a coincidental order.

### 5.7 Schema-primary validation for contracts

Every outbound or inbound contract on the Boundary Contract Map (§8) is validated primarily against its schema — shape, types, required fields, value ranges, enum membership — and only secondarily against concrete example payloads.

Rules:

- The schema is the source of truth; fixture payloads exist to exercise the schema, not to pin exact bytes
- `additionalProperties: true` on inbound contracts (tolerant reader), `additionalProperties: false` on outbound contracts owned by the project (strict producer)
- Enum values are never duplicated across schema and code — both point to a single declaration
- A schema change on a shared contract is a contract-breaking change (§10.6) regardless of whether any current consumer happens to tolerate it

Golden-file equality is reserved for artefacts where the whole byte sequence *is* the contract (rendered UI snapshots, generated documents, wire-format fixtures). Using golden files for structured API responses couples the test to ordering and serialisation choices that the contract does not actually guarantee.

### 5.8 Two-layer regression snapshots

When the project consumes data or behaviour produced by an upstream system (external API, library output, generated schema, LLM-scored output), snapshots are split into two layers that are reviewed differently:

| Layer | What it captures | Review posture |
|-------|------------------|----------------|
| **Upstream layer** | Output of the upstream system as seen by the project | A diff here is expected whenever upstream changes; review confirms the change is benign and the project still satisfies its contracts |
| **Project layer** | Output of the project's own code given a fixed input | A diff here is a regression of the project itself and must be explained before merge |

Conflating the two layers makes every upstream update look like a project regression and trains reviewers to rubber-stamp snapshot updates. Keep the files separate (e.g. `snapshots/upstream/` vs `snapshots/project/`) and require different reviewers or different labels for updates to each.

Data-migration-specific testing patterns (golden queries that compare pre- and post-migration read results) live in D5 ML / Data Pipeline, which activates whenever the project persists structured data subject to schema evolution.

---

## 6. Documentation

### 6.1 Required documents

| Document | Content | Update |
|-----------|----------|---------------|
| **README.md** | Project purpose, quick start, high-level architecture, links to docs | On every significant change |
| **CHANGELOG.md** | History of changes per release, Keep a Changelog format | On every release |
| **DEPENDENCIES.md** | Critical dependencies, versions, contracts, links to official docs | When a dependency changes |
| **COMPATIBILITY.md** | Compatibility status with external dependencies (generated) | Automatic |
| **PROJECT_STATUS.md** | Current project status | Every session |
| **docs/prd/** | PRD and requirements documents | When requirements change |
| **docs/adr/** | Architecture Decision Records | On every architectural decision |
| **docs/runbooks/** | Operational procedures (deploy, rollback, incident response) | On every process change |

### 6.2 Code documentation

**Code comments — when and how:**

| Comment | Do not comment |
|----------|---------------|
| The **why** behind a non-obvious decision | The **what** (the code already says it) |
| Workarounds with a link to the bug/issue | Obvious code (`i++; // increment i`) |
| Assumptions that may not hold in future | Code that should be rewritten rather than commented |
| Contracts and invariants | TODOs without a reference issue |

**TODO/FIXME/HACK:** permitted ONLY with a reference to an issue:

```typescript
// TODO(US-AUTH-042): Replace with OAuth2 PKCE flow when Stripe supports it
// HACK(#issue-789): Workaround for upstream bug in synapse-client v2.237
```

TODOs without an issue = CI emits a warning. TODOs older than 30 days without an issue = CI fail.

API-surface documentation (REST endpoints, SDK exports, CLI contracts) is domain-specific and lives in the relevant appendix: D1.1 for web services, D2.1 for libraries/SDKs, D3.1 for command-line tools.

### 6.3 CHANGELOG.md

Keep a Changelog format (`keepachangelog.com`):

```markdown
## [Unreleased]

### Added
- New endpoint POST /api/v1/users (#123)

### Changed
- Migrated auth from session to JWT (#456)

### Deprecated
- Endpoint GET /api/v1/legacy-users — use /api/v1/users

### Removed
- Support for Node.js 16

### Fixed
- Fix race condition in WebSocket reconnect (#789)

### Security
- Updated stripe-sdk for CVE-2026-1234
```

The CHANGELOG is written by humans (or the AI agent), not generated from commits. Commits are too granular; the CHANGELOG is for the software's users.

---

## 7. CI/CD and deployment

### 7.1 Pipeline overview

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  COMMIT  │──▶│  BUILD   │──▶│  TEST    │──▶│  STAGE   │──▶│  DEPLOY  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
  lint +         compile +      unit +         smoke +        release +
  format +       package        integration    scenario       health
  secret         artefact       + contract     tests in       check +
  scan                                         pre-prod       rollback
                                                              ready
```

The five-stage skeleton is universal. What "package artefact", "pre-prod environment", and "release" mean concretely depends on the project type — see the relevant domain appendix (D1 for web services, D4 for firmware, D5 for data pipelines, …).

### 7.2 Pipeline stages

#### 7.2.1 Build

- **Compile** the source into runnable form (binary, bytecode, transpiled JS, firmware image, bundled assets, …)
- **Package** the output as the distribution artefact (container image, wheel, executable, firmware blob, mobile bundle, …)
- **Artefacts are immutable:** the artefact tested in the Stage environment is the same artefact released at Deploy. Never rebuild per environment.

#### 7.2.2 Test

Execution of the test tiers according to the table in §5.5.

#### 7.2.3 Stage

- **Install the artefact** in a pre-production environment (staging, sandbox, simulator, hardware-in-the-loop bench, …)
- **Run smoke and scenario tests** against that environment before promotion
- **Promotion to Deploy requires green smoke tests**

The concrete shape of the pre-production environment depends on the project type (see the relevant appendix).

#### 7.2.4 Deploy

- **Release the tested artefact** to its consumers (production servers, package registry, firmware fleet, app store, …)
- **Validate the release** with a health check or acceptance verification appropriate to the artefact
- **Keep the prior version's artefact available** so rollback stays cheap
- **Strategy specifics** (blue-green, rolling, canary, OTA, staged rollout, store review) are domain-specific — see the relevant appendix

### 7.3 Rollback

Every deploy MUST be reversible. Rollback is a first-class operation, not an emergency.

| Scenario | Action | Target time |
|----------|--------|-------------|
| Health check fails post-deploy | Automatic rollback to the previous version | < 2 minutes |
| Critical bug discovered after release | Manual rollback (one button/command) | < 5 minutes |
| Rollback not possible (irreversible change) | Hotfix forward, immediate release | Depends on the fix |

When a specific class of change is inherently hard to reverse (a data migration, a breaking contract publication, a firmware flash), the domain appendix that owns that class defines the rollback protocol for it.

### 7.4 Configuration as code

- All CI/CD configuration is in the repository (`.github/workflows/`, `.gitlab-ci.yml`, etc.)
- No "click-ops" configuration in the forge — if it is not in the repository, it does not exist
- Forge-specific configuration in `ci/adapters/<forge>/`
- CI business logic (scripts, classifier, aggregator) lives outside the forge directory — it is portable

### 7.5 Adapter pattern for CI

All CI logic that is specific to GitHub Actions (or GitLab, or Forgejo) lives under `ci/adapters/<forge>/`. The rest (scripts, classifier, aggregator, compatibility database) is portable. Migrating to a new forge is a single-directory swap plus a new adapter.

---

## 8. Boundary Contracts

A **boundary contract** is any promise the system makes to something outside its own implementation: a device, a human, a data store, another piece of code. The **Boundary Contract Map** is the structured inventory of these promises. It answers the question: **where exactly in the code does each contract live, and who is its counterparty?**

The map is the substrate on which classification (§9) and remediation (§10) operate. When M1 Surveillance is active, it is also the target of compatibility testing (M1.2).

**Applicability.** Boundary Contracts are universal: they apply whenever a project has at least one external boundary worth tracking. A purely internal script with no inbound or outbound contracts does not need a map; a service that exposes APIs, consumes dependencies, drives hardware, or renders a UI does.

### 8.1 Contract axes

Every contract sits on one of four axes. A single contract may touch multiple axes when its shape spans them (for example, a REST endpoint that takes a JSON Schema body is both `api` and `data`).

| Axis | What it covers | Examples |
|------|----------------|----------|
| **Hardware** | Physical or virtual device interfaces | Sensor I/O, GPIO, serial/USB, device drivers, hardware event streams |
| **UI** | Interfaces exposed to humans | Web pages, mobile screens, CLI commands, voice prompts, desktop widgets |
| **Data** | Schemas and serialisation agreements | JSON Schema, protobuf, ORM models, database tables, file formats (CSV, Parquet), on-wire message shapes, environment variables and feature flags |
| **API** | Programmatic interfaces consumed by other code | REST/GraphQL/gRPC endpoints, SDK methods, RPC, webhooks, CLIs invoked by other programs |

Direction matters. Each contract is either:

- **Inbound** — the project exposes it; the counterparty is downstream.
- **Outbound** — the project consumes it; the counterparty is upstream.

Both directions are tracked. Inbound contracts are watched against the promise the project makes to its consumers (regression). Outbound contracts are watched against the promise the upstream makes to the project (drift).

### 8.2 Contract map format

```json
{
  "contracts": [
    {
      "id": "stripe.charges.create",
      "axis": "api",
      "direction": "outbound",
      "counterparty": "stripe-api",
      "shape": "POST /v1/charges",
      "file": "src/payments/stripe-client.ts",
      "line": 42,
      "context": "createCharge()",
      "risk_weight": "high",
      "test_coverage": true,
      "last_verified": "2026-04-15"
    }
  ],
  "generated_at": "2026-04-15T10:00:00Z",
  "generator": "manual|ast-walker|grep",
  "contract_count": 47
}
```

The `shape` field is axis-specific: method + path for `api`, a schema identifier for `data`, a device path or event name for `hardware`, a screen or command identifier for `ui`.

### 8.3 Generation

Three strategies, in order of reliability:

1. **AST walker** (best) — static analysis of the source code. Resolves template literals, dynamic imports, type inference. Tools: `ts-morph` for TypeScript, `ast` for Python, `go/ast` for Go. Applies primarily to `api` and `data` contracts.
2. **Structured grep** — pattern search with `ripgrep`. Fast but misses dynamic paths. Useful for `hardware` device paths, CLI contracts, and well-patterned API calls.
3. **Manual** — curated by hand. Acceptable as an initial stub, to be replaced as soon as an automated generator is viable. Often the only option for `ui` contracts.

Different axes can use different generators; the resulting entries are merged into a single map.

### 8.4 Cardinality guard

If the total contract count drops by more than 10% between one generation and the next, CI MUST fail. The guard applies per-axis as well as globally — a 20% drop in `api` contracts with no corresponding PRD change is a red flag even if the total remains stable. Catches: refactors that move calls outside the recognised pattern, configuration changes that exclude files, walker updates.

---

## 9. Change classification

### 9.1 Buckets

| Bucket | Description |
|--------|-------------|
| `data-model` | Changes to schemas, models, types |
| `api-endpoint` | Endpoints added, removed, modified |
| `sdk-method` | Library methods changed |
| `auth` | Authentication, permissions, policies |
| `config` | Environment variables, feature flags |
| `docs-only` | Documentation only |
| `internal` | Internal refactoring, no contract impact |
| `security` | Security patches |
| `deprecation` | Deprecation of existing contracts |
| `migration` | Migrations that modify existing data |

### 9.2 Severity

| Severity | Definition | Action |
|----------|------------|--------|
| `safe` | `internal` or `docs-only` only | Auto-merge after green CI |
| `additive` | New endpoints, new fields, new libraries | PR with report |
| `breaking` | Contracts removed, renamed, signature changed | Draft PR + human review |
| `p0` | Security advisory, protocol change | Draft PR + immediate notification |

### 9.3 Never-auto-merge list

Conditions that always force human review: endpoint removal/rename, response format change, auth protocol change, rate limit reduction, SDK method removal, migration that rewrites data, critical/high security advisory, required field change, WebSocket handshake change, functional test regression.

---

## 10. Remediation workflow

Remediation is a **risk-modulated response pattern**. It applies to any change that passes through classification (§9) — a dependency bump, an inbound contract update, an internal refactor, a config edit — not only to dependency upgrades.

**When to adopt.** The pattern scales down to "everything is L2" (all changes require a human) and scales up to "L0 is enabled for well-tested safe changes". A small project with no CI and no automated classifier operates entirely at L2 by default; that is a valid adoption of the pattern, not an absence of it. L0 and L1 activate only when the project has the machinery to support them (CI, correctness gate, regression tests, classifier). Projects adopt levels as their risk tolerance and tooling maturity allow.

### 10.1 Autonomy levels

| Level | Applies when | Action | Approval |
|-------|--------------|--------|----------|
| **L0** | Change classified `safe` (§9) and all tests green | Auto-merge | None |
| **L1** | Change classified `additive` and the agent's fix passes the correctness gate (§10.2) | PR with fix-claim | Human review |
| **L2** | Change classified `breaking` or `p0`, or matches any never-auto-merge rule, or the project does not yet have L0/L1 machinery | Draft PR + notification | Human intervention |

The levels are a ladder. A project unable to meet L0's preconditions simply stays at L2 for that class of change; no step is mandatory.

### 10.2 Correctness gate (L1)

Green CI is not sufficient to clear L1. The agent MUST: validate against the specific schema that triggered the failure, include a structured fix-claim, add a regression test, and limit changes to the client/adapter layer.

### 10.3 Circuit breaker

3 open L1 PRs OR 5 attempts in 14 days → L1 automation paused, everything degrades to L2, human acknowledgement required before re-enabling.

### 10.4 Adoption workflow

When a change is classified as introducing new capabilities in an existing contract: cross-reference with the Boundary Contract Map, add a wrapper in the client, write a contract test, open an adoption PR + tracking issue for UI changes.

### 10.5 Deprecation tracking

Record the deprecation, cross-reference with the Boundary Contract Map, open a `deprecation-watch` issue. Migration is always human-led.

### 10.6 Contract-breaking change protocol

Triggered whenever a tracked contract breaks (major version bump of an outbound dependency, incompatible schema change, endpoint removal, hardware protocol revision, UI-flow breaking change). Actions: L1 disabled for the affected contract, coverage baseline resettable, Boundary Contract Map mandatorily regenerated, test harness verified end-to-end, issue opened as a tracking epic.

### 10.7 Human report

For each change, the agent produces a report with: what changed, classification, where it impacts (files and lines), what must be modified to maintain operability, what can be adopted, test results, recommended action, and the autonomy level selected with justification.

---

## 11. Project lifecycle

Each phase lists the **Core steps** that apply to every project, followed by activation blocks that only apply when the named module or domain is active. This structure mirrors the Emergent Expansion Protocol (§2.2): nothing module-specific is mandatory until the module's trigger fires.

### 11.1 Phase 0 — Ideation and requirements

**Core (always):**

1. Write the PRD (§1.2)
2. Define user stories with acceptance criteria (§1.3, §1.4)
3. Document architectural decisions in ADRs (§1.5)
4. Create the backlog ordered by priority (§1.6)
5. Define the Definition of Done (§1.8)
6. Identify critical dependencies and document them in `DEPENDENCIES.md`

### 11.2 Phase 1 — Technical bootstrap

**Core (always):**

1. Create the directory structure (§2.1)
2. Configure linting, formatting, pre-commit hooks (§3.4)
3. Configure the base CI pipeline (build + lint + unit test) (§7)
4. Write `CLAUDE.md` (or the equivalent agent-configuration file) with operating rules (§2.4)
5. Generate the initial contract map (§8)
6. Write `.env.example` with all variables documented — where the project handles secrets (§4.3)

**If M1 Surveillance is active, also:**

- Configure surveillance agents (M1.1)
- Create the first compatibility record (`untested`) (M1.3)

**If the project persists structured data (relational or otherwise), also:**

- Write the seed script for the development data store (§5.4)

### 11.3 Phase 2 — Active development

**Core (always):**

1. Work by User Story, respecting the Definition of Done (§1.8)
2. Update `PROJECT_STATUS.md` at every session (§2.3)
3. Write tests for every appropriate tier (§5)
4. Maintain the coverage ratchet (§5.3)
5. Update the CHANGELOG on every user-visible change (§6.3)
6. Keep the contract map up to date after significant refactors (§8)

**If M1 Surveillance is active, also:**

- Agents run in the background and produce compatibility records (M1.3)
- Fix and adoption PRs generated by the agents are reviewed and merged (M1.1)

**If D1 Web Service, D2 Library/SDK, or D3 CLI Tool is active, also:**

- Update API documentation when the contract surface changes (D1.1 / D2.1 / D3.1)

### 11.4 Phase 3 — Maturity and maintenance

**Core (always):**

1. Fixes are primarily L0/L1 (§9, §10)
2. Quarterly review of baseline and thresholds
3. Update the never-auto-merge list (§9.3)

**If M1 Surveillance is active, also:**

- Agents continue surveillance (M1.1)
- Monthly classifier retrospective (M1.4.2)

**If M2 Security-sensitive is active, also:**

- Annual review of OWASP Top 10 coverage and security practices (M2.3)

### 11.5 Phase 4 — Major dependency upgrade

1. The major-version protocol activates (§10.6)
2. L1 disabled, everything is L2
3. Contract map regenerated (§8)
4. Coverage baseline reset (§5.3)
5. Test harness verified
6. Return to Phase 3 after migration

---

## 12. Conventions for AI agents

### 12.1 General rules

- The agent reads `CLAUDE.md` before any action
- The agent updates `PROJECT_STATUS.md` after every session
- The agent never modifies files on the never-auto-merge list without human confirmation
- The agent never modifies business logic — only the client/adapter layer and tests
- The agent always includes a regression test for every fix
- The agent does not pretend to execute operations — if it cannot do something, it says so

### 12.2 Grounding on live data

The first step of any fix loop MUST be: retrieve live data from the dependency and pin it in context. Prevents hallucination of non-existent signatures, endpoints, or behaviours.

### 12.3 Mandatory fix-claim

Every PR produced by the agent MUST include a structured fix-claim (§10.2).

### 12.4 Limited scope

The L1 agent may ONLY add new files, new exports, modify files in the client/adapter layer, and add tests.

The L1 agent may NOT modify existing methods, change existing call sites, alter UI behaviour, modify deploy configuration, or delete files or code.

### 12.5 Proposal before code

For complex features, the agent MUST propose the approach in written form (document or comment) and await human approval before writing code. No "surprise" code.

### 12.6 Structured logging

Every agent action is logged as an event in the compatibility database. Everything is traceable, reproducible, and auditable.

---

# PART II — DOMAIN APPENDICES

---

Domain Appendices add project-type-specific content on top of the Core. Activate an appendix
when its trigger fires; otherwise ignore it. Multiple appendices may be active for a single
project (a web service that ships a client SDK activates D1 and D2).

Each appendix adds content to the Core; it never replaces Core rules. If an appendix and the
Core disagree, the Core wins unless the appendix explicitly marks the override.

## D1 Web Service

**Activation trigger.** The project exposes HTTP, REST, GraphQL, WebSocket, or gRPC endpoints
to clients outside its own process.

**In addition to Core.** Core §6 required documents, code docs, and CHANGELOG apply. This
appendix adds the API-surface conventions and runtime/deploy patterns specific to networked
services.

### D1.1 API documentation

Every public HTTP/REST, GraphQL, gRPC, or WebSocket endpoint MUST have documentation generated from the code:

| Type | Recommended tool | Output |
|------|------------------|--------|
| REST API | OpenAPI/Swagger (from annotations) | `docs/api/openapi.yaml` |

API documentation is generated in CI and published automatically. Manually written API documentation that diverges from the code is an announced bug.

### D1.2 Deploy strategy

- **Production release** triggered by a release tag (`v*.*.*`)
- **Rolling update** or **blue-green** — never a "big bang" deploy without automatic rollback
- **Canary** for high-risk changes: route a small percentage of traffic to the new version first, promote only after stability metrics hold
- **Health check** post-deploy: the application responds on `/healthz` within 60 seconds
- **Automatic rollback** if the health check fails after 3 attempts
- **Feature flags** for risky features: deploy the disabled code, enable gradually

### D1.3 Environments

| Environment | Purpose | Data | Deploy |
|----------|-------|------|--------|
| **Local** | Development | Seed script | Manual |
| **CI** | Automated tests | Generated by tests | Automatic on push |
| **Staging** | Pre-production validation | Anonymised copy of production | Automatic on merge to main |
| **Production** | Real users | Real | Manual/automatic on tag |

Staging is a replica of production: same infrastructure topology, same secrets (rotated), same database schema. A divergence between staging and production is a bug in the environment definition, not a feature.

### D1.4 Request-path testing

In addition to Core §5 (testing pyramid, coverage ratchet, schema-primary validation), web
services require tests that exercise the request path end-to-end through the network stack.

**Contract tests.** Every inbound API contract (§8, axis `api`, direction `inbound`) has at
least one contract test that sends a real HTTP request to a running instance of the service
and asserts on status code, response schema, and key semantic invariants. Contract tests run
in CI against a throwaway environment (Docker Compose, Testcontainers, or equivalent).

**Negative-path coverage.** For every endpoint, test at least:

| Scenario | Expected behaviour |
|----------|--------------------|
| Missing required field | 400 with a machine-readable error body |
| Invalid type / out-of-range value | 400 |
| Unauthenticated request (when auth required) | 401 |
| Insufficient permissions | 403 |
| Non-existent resource | 404 |
| Malformed `Content-Type` | 415 |
| Rate-limit exceeded | 429 with `Retry-After` header |

**Latency assertions.** Critical endpoints (login, health check, primary read path) carry a
latency ceiling in the test suite. The ceiling is a p95 measured over at least 50 sequential
requests against a local instance. Exceeding it does not break CI by default — it emits a
warning — but the team may promote any ceiling to a hard gate via §5.3 ratchet.

**Idempotency.** Every `PUT` and `DELETE` endpoint is tested for idempotency: sending the
same request twice produces the same observable state as sending it once.

### D1.5 Rate-limiting and back-pressure

**Rate-limiting.** Every public-facing endpoint MUST enforce a rate limit. The limit is
declared per-endpoint (or per-group) and is surfaced to the caller via standard headers:

| Header | Meaning |
|--------|---------|
| `X-RateLimit-Limit` | Maximum requests allowed in the window |
| `X-RateLimit-Remaining` | Requests remaining in the current window |
| `X-RateLimit-Reset` | UTC epoch seconds when the window resets |
| `Retry-After` | Seconds to wait (returned with 429) |

Internal endpoints behind a trusted network boundary may omit rate-limiting if and only if
the Boundary Contract Map (§8) records the trust assumption explicitly.

**Back-pressure.** When a downstream dependency is slow or unavailable, the service MUST shed
load rather than queue unboundedly:

- Circuit breaker on every outbound contract marked `risk_weight: high` in the contract map.
  States: closed → open (after N consecutive failures or error-rate threshold) → half-open
  (probe with a single request) → closed.
- Timeout on every outbound call. The timeout is explicit in the code, never implicit from a
  library default. Suggested starting point: 2× the p99 latency observed in production.
- Bulkhead isolation: failure in one outbound dependency does not exhaust the thread/connection
  pool used by other dependencies. Implementation: per-dependency connection pools, or
  async concurrency limiters.

### D1.6 Observability

**Structured logging.** Every log entry is a structured object (JSON or key-value), never a
free-form string. Mandatory fields:

| Field | Content |
|-------|---------|
| `timestamp` | ISO 8601 with timezone |
| `level` | `debug`, `info`, `warn`, `error` |
| `service` | Service name (from configuration) |
| `trace_id` | Distributed trace identifier (propagated from inbound request) |
| `message` | Human-readable summary |

Log entries MUST NOT contain secrets, tokens, passwords, or PII. When M2 is active, this
rule is enforced by the M2.2 PR checklist.

**Metrics.** At a minimum, every web service exposes:

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total requests, labelled by method, path, status |
| `http_request_duration_seconds` | Histogram | Latency distribution, labelled by method, path |
| `http_active_connections` | Gauge | Current open connections |
| Dependency health | Gauge | One gauge per outbound contract (0 = down, 1 = up) |

Metrics are exposed via a `/metrics` endpoint (Prometheus-compatible) or pushed to the
telemetry backend. The choice is recorded in the contract map (axis `api`, direction
`inbound`, counterparty `telemetry-backend`).

**Distributed tracing.** Every inbound request receives (or propagates) a trace ID using
W3C Trace Context (`traceparent` header). The trace ID is attached to all log entries and
outbound calls for the duration of the request. Tracing is sampled in production (suggested
starting point: 1% of traffic, 100% of errors).

**Health and readiness.** Two endpoints, always present:

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `GET /healthz` | Liveness — is the process alive? | 200 if the process can serve; no dependency checks |
| `GET /readyz` | Readiness — can the process accept traffic? | 200 only when all critical dependencies are reachable |

Both endpoints are excluded from rate-limiting and authentication.

## D2 Library / SDK

**Activation trigger.** The project is published as a reusable package to a registry
(npm, PyPI, Maven Central, crates.io, NuGet, RubyGems, Packagist, Go modules, …) or consumed
directly via VCS reference as a library.

**In addition to Core.** Core §6 required documents, code docs, and CHANGELOG apply. This
appendix adds the patterns specific to published packages.

### D2.1 API documentation

Every public SDK surface (exported modules, classes, functions, types) MUST have documentation generated from the code:

| Type | Recommended tool | Output |
|------|------------------|--------|
| TypeScript SDK | TypeDoc | `docs/api/` |
| Python SDK | Sphinx + autodoc | `docs/api/` |

API documentation is generated in CI and published alongside the package. Manually written API documentation that diverges from the code is an announced bug.

*Further D2 content (semantic-versioning discipline for public contracts, deprecation policy,
backwards-compatibility windows, release notes) to be fleshed out post-MVP in Phase 8.7.*

## D3 CLI Tool

**Activation trigger.** The project's primary interface is a command-line executable invoked
by humans or by scripts.

**In addition to Core.** Core §6 required documents, code docs, and CHANGELOG apply. This
appendix adds the patterns specific to command-line interfaces.

### D3.1 API documentation

The CLI's contract surface (flags, subcommands, exit codes, output modes) MUST be documented and kept in sync with the code:

| Type | Recommended tool | Output |
|------|------------------|--------|
| CLI | `--help` + generated man page | `docs/cli/` |

Documentation is generated from the code (help strings, argument metadata) in CI. Manually written documentation that diverges from `--help` is an announced bug.

*Further D3 content (argument/subcommand design, exit-code contracts, machine-readable output
modes, shell completion, installation channels) to be fleshed out post-MVP in Phase 8.7.*

## D4 Embedded / Firmware

**Activation trigger.** The project runs on fixed hardware with bounded memory, storage,
or energy; or requires toolchains cross-compiling to a target architecture; or depends on
peripherals (sensors, radios, actuators) whose contracts are captured in the Boundary Contract
Map under the Hardware axis.

**In addition to Core.** Core applies fully — requirements, code quality, testing pyramid,
documentation, CI/CD concepts, boundary contracts, change classification, remediation. This
appendix adds the patterns that only arise when the artefact runs on constrained hardware.

### D4.1 Hardware boundary contracts

Every peripheral (sensor, actuator, radio, display, storage) is an outbound contract in the
Boundary Contract Map (§8, axis `hardware`). The contract entry records:

| Field | Content |
|-------|---------|
| `device` | Part number or family (e.g. `BME280`, `SX1276`) |
| `bus` | Communication bus (I2C, SPI, UART, GPIO, USB, CAN, …) |
| `address` | Bus address or pin assignment |
| `driver` | Source file that owns the abstraction |
| `datasheet` | Path or URL to the canonical datasheet |
| `voltage_level` | Logic-level voltage (e.g. 3.3 V, 5 V) |
| `power_budget_mW` | Typical and peak draw (from datasheet) |

**Hardware Abstraction Layer (HAL).** All peripheral access passes through a thin HAL whose
interface is defined independently of the hardware. Application code never reads a register
or toggles a pin directly. The HAL is the contract boundary: changes to the board layout or
to a peripheral revision affect only the HAL implementation, never the application.

### D4.2 Cross-compilation and toolchain

- The project declares the exact toolchain version (compiler, linker, SDK) in a version-locked
  file (`toolchain.toml`, `platformio.ini`, `west.yml`, or equivalent). The same file is used
  by CI and by every developer.
- The build produces a deterministic binary: same source + same toolchain + same flags = same
  output, byte-for-byte. When full determinism is not achievable, the delta is documented in
  an ADR.
- Binary size is tracked as a ratchet (§5.3 pattern): a CI step compares the artefact size
  against a committed baseline. A regression beyond a declared threshold (e.g. +2%) fails
  the build unless the increase is justified in the commit message.

### D4.3 Hardware-in-the-loop (HIL) testing

Core §5 testing pyramid applies. This section adds the tier that can only run on real hardware
or a cycle-accurate simulator.

**HIL tier placement.** HIL tests sit above integration tests in the pyramid. They are slower
and more expensive; they run on merge to `main` or on a nightly schedule, not on every push.

**What HIL tests cover:**

| Category | Example |
|----------|---------|
| Peripheral I/O | Sensor reads return plausible values; actuator commands reach the device |
| Timing | ISR latency stays within the declared deadline |
| Power state transitions | Sleep → wake → resume produces the correct peripheral state |
| Communication protocols | Full frame exchange on bus (CAN, I2C, SPI) with a real or loopback peer |
| Firmware update | OTA or flash-based update completes and the device boots the new image |

**HIL infrastructure.** The CI runner has access to a physical board (or a farm of boards)
via a debug probe (J-Link, ST-Link, OpenOCD, or equivalent). The runner flashes the artefact,
executes the test suite over the debug channel, and collects results. If no physical board is
available, a cycle-accurate simulator (QEMU with the correct machine model, Renode, or vendor
simulator) is an acceptable substitute — but the substitution is recorded in the contract map
so the team knows which contracts are verified on real hardware and which on simulation.

### D4.4 Flash and OTA update strategy

- **Image signing.** Every firmware image is signed before distribution. The bootloader
  verifies the signature before applying the update. Unsigned images are rejected.
- **A/B partitioning.** The device maintains two firmware slots (A and B). The new image is
  written to the inactive slot. If the boot self-test fails, the bootloader reverts to the
  previous slot automatically.
- **Rollback trigger.** The application reports "healthy" to the bootloader within a
  configurable window after first boot (watchdog or explicit confirmation). If the window
  expires without confirmation, the bootloader treats the update as failed and reverts.
- **OTA transport.** When the device has network connectivity, updates are delivered over an
  encrypted channel (TLS 1.2+). The update payload includes a manifest with version, size,
  SHA-256 hash, and signature. The device verifies the manifest before downloading the image.
- **Offline update.** When no network is available, updates are delivered via removable media
  (SD card, USB). The same signing and verification rules apply.
- **Version contract.** The running firmware version is always queryable (via a debug command,
  a status register, or an API endpoint). The version string follows the project's tagging
  convention (§3.8).

### D4.5 Power and thermal budgets

**Power budget.** The project maintains a power budget document (`docs/power-budget.md` or
equivalent) that lists every component's draw in each operating mode:

| Component | Sleep (mW) | Idle (mW) | Active (mW) | Peak (mW) | Source |
|-----------|-----------|-----------|-------------|-----------|--------|
| MCU | — | — | — | — | Datasheet §X.Y |
| Radio | — | — | — | — | Datasheet §X.Y |
| Sensor A | — | — | — | — | Measured |
| … | | | | | |
| **Total** | — | — | — | — | |

The budget is validated against the power source (battery capacity, solar harvest rate, USB
supply) to derive a minimum operating life. Any change that adds a component or increases
duty cycle updates the budget document and verifies that the operating-life target still holds.

**Thermal budget.** When the system operates in an enclosure or in an environment with
constrained dissipation, the same table includes a thermal column (junction temperature at
steady state). The thermal budget is validated by measurement during HIL testing (D4.3) or
by thermal simulation.

### D4.6 Bring-up checklist

When a new board revision arrives, the following checklist is executed before any application
code runs. Each step is recorded in `docs/bring-up/<board-rev>.md`.

- [ ] Visual inspection: correct components populated, no solder bridges
- [ ] Power rail verification: each rail within ±5% of nominal at no-load
- [ ] Programmer connection: debug probe communicates with the MCU
- [ ] Bootloader flash: bootloader boots, serial/debug console active
- [ ] Peripheral smoke test: each peripheral responds to a basic read/write
- [ ] Clock verification: system clock within ±50 ppm of expected frequency
- [ ] Power measurement: idle and active draw match the power budget (D4.5) within ±15%
- [ ] Firmware flash: full application boots on the new board
- [ ] HIL suite pass: all D4.3 tests pass on the new revision

## D5 ML / Data Pipeline

**Activation trigger.** The project trains or fine-tunes models, transforms datasets at scale,
or persists structured data subject to schema evolution (relational or otherwise).

**In addition to Core.** Core §5 testing fundamentals apply. This appendix adds the testing
patterns that only arise when data is being reshaped, and will grow to cover pipeline-
reproducibility, dataset versioning, drift monitoring, and evaluation contracts.

### D5.1 Golden queries for data migrations

For any migration that alters schema or rewrites data, maintain a small curated set of **golden queries** — canonical read queries whose results must match before and after the migration (modulo an explicit, documented allow-list of intentional differences).

Rules:

- Golden queries live alongside the migration script, version-controlled with it
- They are executed automatically against a pre-migration snapshot and the post-migration state; any unexplained divergence blocks promotion of the migration
- Each query has a short rationale explaining which invariant it protects (row counts per tenant, aggregate totals, referential integrity across renamed tables, …)
- "Intentional difference" entries are not free-form prose: they are a structured list referenced from the migration's remediation record (§10)

Golden queries are complementary to schema migrations' own tests; they catch semantic drift that schema-level checks miss (e.g. a column renamed correctly but backfilled with the wrong default).

### D5.2 Database migration

- **Forward-only migration.** Every migration has an `up` file and a `down` file. The `down` is tested — it is not an empty placeholder.
- **Migration separate from the application deploy.** The migration runs before the deploy. If the migration fails, the deploy does not start.
- **Backward compatibility.** The new version of the code MUST work with both the old and the new version of the database for at least one deploy cycle. This allows rollback without rolling back the database.
- **Data migration vs schema migration.** The two are separate. Schema first, data after. Never in the same migration.

**Irreversible-migration rule.** If a deploy includes an irreversible database migration, it must be tagged as `BREAKING` in the CHANGELOG and requires explicit approval before deploying. Because rolling back the application does not undo the migration, the rollback scenario for this class of change is "hotfix forward" — see Core §7.3.

### D5.3 Training-pipeline reproducibility

Every training run MUST be reproducible from its recorded inputs. The minimum record per run:

| Artefact | Content | Storage |
|----------|---------|---------|
| **Run manifest** | Dataset version, code commit, dependency lock, hyperparameters, random seeds, hardware spec (GPU model, driver version) | Version-controlled or experiment tracker |
| **Trained model** | Serialised weights + architecture definition | Model registry (MLflow, W&B, DVC, or equivalent) |
| **Evaluation report** | Metrics on the held-out evaluation set (D5.6) | Stored alongside the model in the registry |
| **Training log** | Loss curves, resource utilisation, wall-clock time | Experiment tracker |

**Determinism.** When the framework supports it, pin every source of non-determinism
(random seeds, CUDA deterministic mode, data-loader shuffle seed). Document any remaining
non-deterministic operations (e.g. certain GPU kernels) in the run manifest so that "same
inputs → same outputs" failures are explained, not mysterious.

**Pipeline-as-code.** The training pipeline is defined in version-controlled code, not in
notebook cells or manual shell commands. A single entry-point command (e.g. `make train`,
`dvc repro`, `python -m train`) reproduces the entire pipeline from raw data to evaluated
model. Interactive notebooks are permitted for exploration but are never the canonical
training path.

### D5.4 Dataset versioning

Datasets are versioned artefacts with the same rigour as code:

- Every dataset has a unique version identifier (content hash, tag, or monotonic version
  number). The identifier is recorded in the run manifest (D5.3).
- Dataset transformations (filtering, labelling, augmentation, splitting) are defined in
  code, not applied manually. The transformation pipeline is version-controlled alongside
  the data schema.
- Large datasets that cannot live in the Git repository are tracked via DVC, Git-LFS, or a
  dedicated registry. The pointer file (`.dvc`, `.gitattributes`, manifest) is committed;
  the data itself is stored externally.
- Schema changes to the dataset (new columns, changed types, dropped features) follow the
  same classification (§9) and remediation (§10) workflow as any other data-model change.

### D5.5 Drift monitoring

Once a model is serving predictions, the project monitors two kinds of drift:

**Data drift.** The distribution of incoming features diverges from the distribution the
model was trained on. Detection methods (choose at least one):

| Method | What it measures | Suggested threshold |
|--------|-----------------|---------------------|
| Population Stability Index (PSI) | Distribution shift per feature | PSI > 0.2 → alert |
| Kolmogorov–Smirnov test | Maximum CDF distance | p < 0.01 → alert |
| Jensen–Shannon divergence | Symmetric distribution divergence | JSD > 0.1 → alert |

**Concept drift.** The relationship between features and the target changes — the model's
predictions degrade even though the input distribution looks stable. Detected by monitoring
live performance metrics (accuracy, precision, recall, or the domain-specific metric defined
in D5.6) against the evaluation baseline. A sustained drop beyond a declared threshold
triggers a retraining investigation.

**Alert flow.** Drift alerts flow through Core classification (§9, bucket `data-model`) and
remediation (§10). Severity mapping:

| Signal | Severity | Action |
|--------|----------|--------|
| Data drift above threshold, no performance drop | L1 — `safe` | Log, monitor next window |
| Data drift + performance drop within tolerance | L2 — `review` | Schedule retraining evaluation |
| Performance drop beyond tolerance | L3 — `breaking` | Retrain or roll back to previous model |

### D5.6 Evaluation contracts

Every model has an **evaluation contract** — a versioned specification of how the model's
quality is measured before promotion to production.

| Element | Content |
|---------|---------|
| **Evaluation dataset** | A held-out set, versioned alongside training data (D5.4), never used during training |
| **Primary metric** | The single metric that gates promotion (e.g. F1, AUROC, RMSE) |
| **Threshold** | The minimum acceptable value of the primary metric; updated via ratchet (§5.3) |
| **Secondary metrics** | Additional metrics reported for context but not gating |
| **Slice analysis** | Performance broken down by critical subgroups (demographic, geographic, temporal) to surface hidden regressions |
| **Comparison baseline** | The currently deployed model's evaluation report; the new model must meet or exceed the primary metric |

The evaluation contract is executed automatically in CI. A model that fails the contract is
not promoted — it is sent back for investigation, not manually overridden.

## D6 Mobile App

**Activation trigger.** The project ships to iOS App Store, Google Play, or any vendor-gated
mobile distribution channel.

**In addition to Core.** *Stub — to be fleshed out post-MVP. Will cover review/submission
workflows, staged rollouts, on-device telemetry, crash reporting, and backwards-compatibility
windows with prior OS versions.*

## D7 Static Site / Frontend-only

**Activation trigger.** The project renders entirely client-side or as a statically-generated
site, with no backend owned by the project itself.

**In addition to Core.** *Stub — to be fleshed out post-MVP. Will cover build/bundle budgets,
hosting/CDN contracts, client-side error reporting, and accessibility audits.*

---

# PART III — CROSS-CUTTING MODULES

---

Cross-cutting Modules add capabilities that compose with any domain. Activate a module when
its trigger fires. A module may be active alongside any set of Domain Appendices.

Each module adds content to the Core; it never replaces Core rules.

## M1 Surveillance

**Activation trigger.** The Boundary Contract Map (§8) contains at least one outbound contract
(dependency, upstream API, device driver, external data source) whose evolution must be
tracked over time. A project with no outbound contracts — a pure offline utility, a one-shot
script — does not need this module. When in doubt: if the project has a lock file
(`package-lock.json`, `poetry.lock`, `Cargo.lock`, …) or calls any external API, the trigger
has fired.

**In addition to Core.** Surveillance runs autonomous agents against outbound contracts at
regular intervals; detected changes flow through Core classification (§9) and remediation
(§10), and the detection path itself is self-tested so the loop stays honest. Every action
produced by the module is an event in the compatibility database (M1.3), which is the audit
trail.

**Relationship to other modules and appendices.** M1 composes with any domain:

| Domain active | M1 watches |
|---------------|------------|
| D1 Web Service | Upstream APIs, cloud-provider SDKs, container base images |
| D4 Embedded | Device-driver versions, toolchain releases, RTOS updates |
| D5 ML / Data | Framework versions (PyTorch, TensorFlow), dataset registry changes, model-serving API drift |
| Any | Language runtime, linter/formatter, CI runner images |

### M1.1 Surveillance agents

Agents are autonomous processes that monitor external dependencies at regular intervals.

#### M1.1.1 Architecture

```
┌─────────────────────────────────────────────────┐
│                  SCHEDULER                       │
│  (cron / CI schedule / workflow_dispatch)         │
└──────┬──────┬──────┬──────┬──────┬───────────────┘
       │      │      │      │      │
       ▼      ▼      ▼      ▼      ▼
   ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
   │Agent ││Agent ││Agent ││Agent ││Agent │
   │Pkg   ││Docker││GitHub││API   ││Docs  │
   │Watch ││Watch ││Watch ││Probe ││Watch │
   └──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘
      │       │       │       │       │
      ▼       ▼       ▼       ▼       ▼
   ┌─────────────────────────────────────┐
   │         CHANGE CLASSIFIER           │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │         IMPACT ANALYSER             │
   │    (cross-ref with contract map)     │
   └──────────────┬──────────────────────┘
                  │
          ┌───────┴────────┐
          ▼                ▼
   ┌────────────┐   ┌────────────┐
   │ REMEDIATION│   │  ADOPTION  │
   │   (fix)    │   │  (improve) │
   └────────────┘   └────────────┘
```

#### M1.1.2 Agent types

**M1.1.2.1 Package Watch** — detects new versions of dependencies. Frequency: 5 min (RSS) or 1h (JSON API). Filter: stable releases only.

**M1.1.2.2 API Probe** — runs contract tests against every endpoint in the contract map. Frequency: 6h for critical endpoints, 24h for others. Verifies: reachability, schema, semantics, new/missing fields, deprecation headers, rate limits, versioning.

**M1.1.2.3 Docs Watch** — monitors changelogs and official documentation. Frequency: 24h. Method: fetch + textual diff.

**M1.1.2.4 Security Watch** — detects security advisories. Frequency: 15 min. Sources: GHSA, NVD, native audit tools. Any advisory forces L2.

**M1.1.2.5 Container/Image Watch** — detects new Docker images. Frequency: 15 min. Timeout: 90 min with backoff.

**M1.1.2.6 State-of-the-Art Scout** — an agent dedicated to state-of-the-art research. Unlike the other agents: it does not monitor a single dependency, but scans the technological landscape around the project. Frequency: quarterly for stable components, monthly for components under active development.

What it does each cycle:

1. **Technology health check.** For every significant technology in the project, verifies: latest release, release frequency over the past year, open issue trends, documentation status, deprecation or end-of-life announcements.

2. **Alternative scanning.** Searches for new libraries or services that solve the same problem as an existing dependency with a different or better approach. Does not suggest switching — it flags that the alternative exists and leaves the decision to the human.

3. **Pattern evolution.** Verifies whether the architectural patterns used in the project are still best practice or whether the community has moved towards different approaches. Looks for: updates to official style guides, new RFCs, talks from key conferences.

4. **Security landscape.** Verifies whether security practices are aligned with current recommendations (OWASP, NIST, CIS).

5. **Ecosystem health.** Assesses the health of the ecosystem: growing or declining community, significant forks, controversies (licence, governance, ownership).

Output: report in `docs/research/` with findings classified into 5 levels: `healthy` (no action), `watch` (monitor in the next cycle), `evaluate` (create ADR with comparison), `migrate` (plan migration in the backlog), `urgent` (immediate action — end-of-life, critical vulnerability, hostile fork).

The agent proactively suggests research when: a new project is started, a dependency is added, an architectural choice is proposed, the project enters a new phase, or N months have passed since the last research on a component. Full details in §1.7.

#### M1.1.3 Heartbeat

Every agent, every cycle — even when nothing is detected — emits a heartbeat. Alert if the most recent is older than 6 hours.

#### M1.1.4 Multi-source configuration

For every critical dependency, at least two sources with different roles: primary (fast trigger) and backstop (recovery). The backstop reconciles missed versions when the primary comes back online.

### M1.2 Compatibility test matrix

#### M1.2.1 Slots

| Slot | Definition | Purpose |
|------|------------|---------|
| `latest` | Version that triggered the cycle | Compatibility with the new change |
| `recent` | Most recent stable version (21-day window) | Masked regressions |
| `baseline` | Pinned version, reviewed quarterly | Declared contract |

#### M1.2.2 Run manifest

At the start of each cycle, before any test, the system freezes versions in a JSON manifest. Eliminates ambiguity if the matrix resolves differently between steps.

#### M1.2.3 Test data

1. **Seed workload** — creates data that exercises every outbound contract
2. **Golden queries** — queries with expected results to verify post-migration integrity
3. **Snapshot regression** — loads snapshots from previous versions and verifies data accessibility

### M1.3 Compatibility database

#### M1.3.1 Format

Flat JSON in the repo, one file per version per dependency. No external database.

```
compat-db/
├── stripe-api/
│   ├── 2026-04-01_v2024-12-18.json
│   └── 2026-04-15_v2025-01-15.json
├── express/
│   ├── 2026-04-10_4.21.0.json
│   └── 2026-04-18_4.21.1.json
└── _aggregated/
    └── 2026-04-18.json
```

#### M1.3.2 Events (append-only)

The `events` array is the complete audit trail. Never modify or remove events.

#### M1.3.3 Aggregation

Each slot produces its own payload; an aggregation job merges them. `pass` only if all slots are `pass`. If any slot is `fail`, the rollup is `fail`. If a slot is `error`, the rollup is `partial`.

#### M1.3.4 Portability

Plain JSON in the repo. Migrating to another forge = copy directory + new CI adapter.

### M1.4 Self-testing and observability

#### M1.4.1 Detection heartbeat

Every polling cycle emits a heartbeat. Alert if the most recent is older than 6 hours.

#### M1.4.2 Classifier retrospective

Monthly job: reviews all `safe` auto-merged records from the past 30 days. False negative rate > 10% → alert to recalibrate.

#### M1.4.3 End-to-end canary

Weekly job: injects a synthetic record to verify the entire detection → classification → issue → contract-map cross-ref → event emission path. Cleans up after verification.

#### M1.4.4 Boundary Contract Map cardinality guard

Delegates to Core §8.4. If the total contract count — or any single-axis count — drops by
more than 10% between generations, CI fails. M1 adds a scheduled re-generation (weekly or on
dependency change) so the guard runs even when no human remembers to regenerate the map.

## M2 Security-sensitive

**Activation trigger.** The project handles authentication, authorisation, or personally
identifiable information; OR serves untrusted clients over a network; OR processes
attacker-controlled input.

**In addition to Core.** Core §4 (Fundamental principles, Input validation, Secrets management)
applies to every project. This module adds the patterns that make sense only when the trigger
above fires: identity handling, a per-PR security checklist, and OWASP coverage.

### M2.1 Authentication and authorisation

- **Passwords.** Never in plain text, never in logs, never in URLs. Hashed with bcrypt/argon2, unique salt per user.
- **Tokens.** JWT with short expiry (15 min access, 7 days refresh). Refresh token rotated on every use.
- **Session.** `HttpOnly`, `Secure`, `SameSite=Strict` cookies. Session ID regenerated after login.
- **API keys.** Never in source code. Never in the frontend. Always in an environment variable or secret manager.
- **Authorisation.** Checked on every request, not only at login. Explicit RBAC or ABAC, never hard-coded.

### M2.2 Security checklist for every PR

- [ ] No secrets committed (verified by tools: `trufflehog`, `gitleaks`)
- [ ] Input validated with schema at every boundary
- [ ] Parameterised queries (no SQL concatenation)
- [ ] Errors do not expose stack traces or internal details to the user
- [ ] Security headers present (CSP, X-Frame-Options, X-Content-Type-Options)
- [ ] Dependencies free of known vulnerabilities (`npm audit` / `pip-audit` clean)
- [ ] Rate limiting configured for public endpoints
- [ ] Logs do not contain PII or secrets

### M2.3 OWASP Top 10 as baseline

Every web application MUST be protected against the current OWASP Top 10. The team reviews the list annually and verifies that every item is covered by tests or configuration.

## M3 Release & Distribution

**Activation trigger.** The project ships versioned artefacts to external consumers
(applies whenever D2, D3, D4, or D6 is active; may also apply to D1 when artefacts are
published to an internal registry).

**In addition to Core.** *Stub — to be fleshed out post-MVP. Will cover semver discipline,
changelog automation, signing and provenance, release notes, and rollback-of-release
protocols.*

## M4 Classification & Taxonomy

**Activation trigger.** The project owns, extends, or depends on a domain-specific ontological
framework (threat intelligence, biomedical coding, geospatial metadata, fraud signalling,
vulnerability cataloguing, …). If the project invents its own terminology, this module
activates on the first naming decision.

**In addition to Core.** *To be filled in Phase 8.6. Will include MECE design principles,
taxonomy governance (ownership, RFC, deprecation), stable identifiers and their versioning,
a scouting protocol binding to §1.7 SOTA Scout that directs the AI to discover domain-specific
frameworks per project, adoption patterns, coverage/ambiguity audits, machine-readable
serialisations, and an upstream contribution protocol. Framework-agnostic: ships no curated
catalogue; examples (MITRE ATT&CK, STIX, FT3, CAPEC, TLP, F3EAD, SNOMED, ICD, ISO 19115) are
illustrative of adoption shape only.*

---

## Appendix A — Phase checklists

### A.1 Phase 0 checklist (Requirements)

- [ ] PRD written with all mandatory sections (§1.2)
- [ ] State-of-the-art research conducted for the project domain (§1.7)
- [ ] Pre-implementation checklist in the PRD completed and verified
- [ ] User stories with acceptance criteria for the first sprint
- [ ] ADRs for fundamental architectural decisions (with "Alternatives rejected" from real research)
- [ ] Backlog created and ordered by priority
- [ ] Definition of Done defined and shared
- [ ] Critical dependencies identified in `DEPENDENCIES.md` (with alternatives comparison §1.7.1)

### A.2 Phase 1 checklist (Bootstrap)

- [ ] Directory structure created (§2.1)
- [ ] Linter + formatter configured and integrated into CI (§3.4)
- [ ] Base CI pipeline working (build + lint + unit) (§7)
- [ ] `CLAUDE.md` written (§2.3)
- [ ] Contract map generated (even manually) (§8)
- [ ] Surveillance agents configured (M1.1)
- [ ] First compatibility record created (`untested`)
- [ ] `.env.example` with all variables documented (§4.3)
- [ ] Secret scan configured in CI (M2.2)
- [ ] Seed script for development database (§5.4)
- [ ] Initial coverage baseline committed (§5.3)
- [ ] Heartbeat alert configured (threshold: 6 hours) (M1.4.1)

### A.3 Checklist for every PR

- [ ] Code follows naming conventions (§3.2)
- [ ] Commit message in Conventional Commits format (§3.3)
- [ ] No lint warnings (§3.4)
- [ ] No secrets committed (M2.2)
- [ ] Input validated with schema at every boundary (§4.2)
- [ ] Tests written for new/modified code (§5)
- [ ] Coverage has not dropped below baseline (§5.3)
- [ ] Documentation updated where necessary (§6)
- [ ] Contract map updated if dependencies added/removed (§8)
- [ ] Errors handled explicitly, no empty catch blocks (§3.6)

### A.4 Checklist for release

- [ ] All tests pass across all tiers (§5.5)
- [ ] CHANGELOG.md updated (§6.3)
- [ ] Version tag created (§3.8)
- [ ] Pre-production smoke tests green on promotion (§7.2.3)
- [ ] Rollback tested (§7.3)
- [ ] Database migration tested (up AND down) (D5.2, where applicable)
- [ ] API documentation updated (D1.1 / D2.1 / D3.1, where applicable)
- [ ] Compat database updated with current state (M1.3)

### A.5 Surveillance checklist

- [ ] Agents active with recent heartbeat (< 6 hours) (M1.4.1)
- [ ] Weekly canary passed (M1.4.3)
- [ ] Monthly retrospective executed (M1.4.2)
- [ ] Never-auto-merge list reviewed (§9.3)
- [ ] Coverage baseline updated (§5.3)
- [ ] Contract map regenerated after refactor (§8)
- [ ] Thresholds reviewed quarterly (M1.4)
- [ ] State-of-the-Art Scout run in the current quarter (§1.7.5, M1.1.2.6)
- [ ] SOTA reports reviewed and actions planned for `evaluate` or `migrate` signals

---

## Appendix B — Templates

### B.1 PRD template

```markdown
# [Project Name] — Product Requirements Document

**Status:** Draft v1
**Owner:** [name]
**Last updated:** [date]

### Pre-implementation checklist

- [ ] [Decision 1 already confirmed]
- [ ] [Decision 2 already confirmed]

---

## 1. Purpose and scope

### 1.1 What this system guarantees
### 1.2 What this system does not cover

## 2. Users and stakeholders
## 3. Functional requirements
## 4. Non-functional requirements

### 4.1 Performance
### 4.2 Security
### 4.3 Accessibility
### 4.4 Scalability

## 5. Architectural constraints
## 6. Open questions

| # | Topic | Owner | Status |
|---|-------|-------|--------|

## 7. Later-phase work

| Item | Phase | Notes |
|------|-------|-------|

## Appendices
```

### B.2 User Story template

```markdown
# US-[AREA]-[NUMBER]: [Short title]

**Priority:** P0 | P1 | P2 | P3
**Estimate:** [hours/points]
**PRD ref:** §[section]
**Dependencies:** US-[xxx], US-[yyy]

## Story
As a [role]
I want [action]
So that [benefit]

## Acceptance Criteria

1. GIVEN [context]
   WHEN [action]
   THEN [result]

2. GIVEN [context]
   WHEN [action]
   THEN [result]

## Technical notes
[notes for the implementer]
```

### B.3 ADR template

```markdown
# ADR-[NUMBER]: [Title]

**Status:** proposed | accepted | deprecated | superseded by ADR-[n]
**Date:** YYYY-MM-DD

## Context
[Why this decision is necessary]

## Decision
[What was decided]

## Consequences
[Positive and negative impact]

## Alternatives rejected
[What was considered and discarded, with rationale]
```

### B.4 DEPENDENCIES.md template

```markdown
# Dependencies

## Critical dependencies

### [Dependency name]
- **Type:** REST API | SDK | Database | Service
- **Version:** [current version]
- **Contract:** [link to contract documentation]
- **Contract count:** [number of contracts in Boundary Contract Map, by axis]
- **Surveillance agent:** [agent id]
- **Last verified:** [date]
- **Notes:** [particular notes, known quirks, workarounds]

## Development dependencies

### [Name]
- **Purpose:** [what it is used for]
- **Version:** [version]
- **Pinned:** yes | no (range)
```

---

## Appendix C — Glossary

| Term | Definition |
|------|------------|
| **PRD** | Product Requirements Document — specification of the what and the why |
| **ADR** | Architecture Decision Record — documented architectural decision |
| **User Story** | Functional requirement from the user's perspective |
| **Acceptance Criteria** | Binary conditions that define "done" |
| **Definition of Done** | Universal checklist applied to every work item |
| **Boundary contract** | A promise the system makes to something outside its own implementation (hardware, UI, data, API); can be inbound (exposed) or outbound (consumed) |
| **Boundary Contract Map** | Structured inventory of all boundary contracts, tagged by axis and direction (§8) |
| **Bucket** | Change category (api-endpoint, data-model, etc.) |
| **Severity** | Level of impact of the change (safe, additive, breaking, p0) |
| **Slot** | A version in the test matrix (latest, recent, baseline) |
| **L0/L1/L2** | Autonomy levels in remediation |
| **Heartbeat** | Periodic signal confirming that an agent is active |
| **Canary** | Synthetic end-to-end test of the surveillance system |
| **Golden query** | Query with expected result to verify data integrity |
| **Fix-claim** | Structured declaration accompanying every agentic fix |
| **Circuit breaker** | Mechanism that disables automation after too many failures |
| **Never-auto-merge** | Conditions that always force human review |
| **Ratchet** | Mechanism that prevents coverage from dropping |
| **Escape valve** | Tracked temporary exception to a ratchet rule |
| **Conventional Commits** | Standard for structured commit messages |
| **Blue-green deploy** | Deployment strategy using two alternating environments |
| **Rolling update** | Gradual deployment that replaces instances one at a time |
| **Feature flag** | Toggle that enables/disables a feature without deployment |
| **SOTA Scout** | Agent that researches the state of the art for project technologies and patterns |
| **Technology health check** | Periodic health verification of a technology (releases, community, trends) |
| **Alternative scanning** | Search for libraries or services alternative to those in use |
| **Pattern evolution** | Monitoring of the evolution of architectural best practices in the industry |
