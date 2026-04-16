# Software Development Playbook

**Version:** 2.0.0 — Draft
**Last updated:** 2026-04-15
**Scope:** Framework for developing, testing, deploying, maintaining, and monitoring software projects.

This playbook defines the entire lifecycle of a software project: from requirements gathering through to deployment and continuous dependency monitoring. It is designed for independent developers and small teams operating with autonomous agents (Claude Code, Ruflo, or equivalents).

---

## Table of Contents

### Part I — Development

1. [Requirements and planning](#1-requirements-and-planning)
2. [Project structure](#2-project-structure)
3. [Code quality](#3-code-quality)
4. [Security requirements](#4-security-requirements)
5. [Testing strategy](#5-testing-strategy)
6. [Documentation](#6-documentation)
7. [CI/CD and deployment](#7-cicd-and-deployment)

### Part II — Surveillance and maintenance

8. [Dependency Surface Map](#8-dependency-surface-map)
9. [Surveillance agents](#9-surveillance-agents)
10. [Change classification](#10-change-classification)
11. [Compatibility test matrix](#11-compatibility-test-matrix)
12. [Remediation workflow](#12-remediation-workflow)
13. [Compatibility database](#13-compatibility-database)
14. [Self-testing and observability](#14-self-testing-and-observability)

### Part III — Management

15. [Project lifecycle](#15-project-lifecycle)
16. [Conventions for AI agents](#16-conventions-for-ai-agents)

### Appendices

- [A — Per-phase checklists](#appendix-a--phase-checklists)
- [B — Templates](#appendix-b--templates)
- [C — Glossary](#appendix-c--glossary)

---

# PART I — DEVELOPMENT

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

In addition to the dependency surveillance agents (§9), the playbook includes an agent dedicated to state-of-the-art research. This agent operates differently from the others: it does not monitor a single dependency, but scans the technological landscape surrounding the project.

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

An item is "done" when ALL of the following conditions are met:

- [ ] State-of-the-art research has been conducted where applicable (§1.7)
- [ ] Code is written and complies with style conventions (§3)
- [ ] All Acceptance Criteria are satisfied
- [ ] Tests are written and pass (§5)
- [ ] Coverage has not dropped below the threshold (§5.3)
- [ ] Documentation is up to date (§6)
- [ ] Code has been reviewed (self-review or peer review)
- [ ] CI is green
- [ ] The surface map is updated if external dependencies have been added or removed (§8)
- [ ] `PROJECT_STATUS.md` is updated

---

## 2. Project structure

### 2.1 Mandatory files in the root

Every project MUST contain:

```
project-root/
├── CLAUDE.md                    # Rules for AI agents
├── PROJECT_STATUS.md            # Current status (4 fixed sections)
├── DEPENDENCIES.md              # Critical dependency map and contracts
├── CHANGELOG.md                 # History of changes per release
├── COMPATIBILITY.md             # Compatibility status with external dependencies (generated)
├── docs/
│   ├── prd/                     # PRD and requirements documents
│   │   └── 00-prd.md
│   ├── adr/                     # Architecture Decision Records
│   │   ├── 001-<title>.md
│   │   └── ...
│   ├── api/                     # API documentation (generated or manual)
│   └── runbooks/                # Operational procedures (deploy, rollback, incident)
├── src/                         # Source code
├── tests/                       # Tests (structure mirroring src/)
├── scripts/                     # Build, seed, utility scripts
├── ci/                          # CI/CD configuration
│   └── adapters/                # Adapters for specific forges (github/, gitlab/, etc.)
├── compat-data/                 # Compatibility database
├── compatibility/               # Schema, surface map, catalogues
├── surveillance/                # Surveillance agent configuration
└── .config/                     # Linting, formatting configuration, etc.
    ├── eslint.config.js
    ├── prettier.config.js
    └── ...
```

### 2.2 PROJECT_STATUS.md

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

### 2.3 CLAUDE.md

Operational rules for AI agents. Minimum content:

- Language and writing style (e.g. British English, active voice, short sentences)
- List of forbidden words
- Scope of permitted modifications per autonomy level (L0/L1/L2)
- Naming conventions for branches, commits, files
- Protected paths (files the agent cannot modify without human confirmation)
- Editorial rules (no em dash, max line length, etc.)

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

### 4.3 Authentication and authorisation

- **Passwords.** Never in plain text, never in logs, never in URLs. Hashed with bcrypt/argon2, unique salt per user.
- **Tokens.** JWT with short expiry (15 min access, 7 days refresh). Refresh token rotated on every use.
- **Session.** `HttpOnly`, `Secure`, `SameSite=Strict` cookies. Session ID regenerated after login.
- **API keys.** Never in source code. Never in the frontend. Always in an environment variable or secret manager.
- **Authorisation.** Checked on every request, not only at login. Explicit RBAC or ABAC, never hard-coded.

### 4.4 Secrets management

| Rule | Detail |
|--------|----------|
| **Never in code** | No secrets in source files, commits, or logs. `.gitignore` includes `.env`, `*.key`, `*.pem` |
| **Environment variables** | Primary method for secrets in local and CI environments |
| **Secret manager** | For production: GitHub Secrets, Vault, AWS SSM, or equivalent |
| **Rotation** | Every secret has an expiry date. Rotation is automated or scheduled |
| **Audit** | Every access to a secret is logged. If a secret is compromised, it must be rotated immediately |
| **`.env.example`** | The repo contains a `.env.example` with variable names (without values) and explanatory comments |

### 4.5 Security checklist for every PR

- [ ] No secrets committed (verified by tools: `trufflehog`, `gitleaks`)
- [ ] Input validated with schema at every boundary
- [ ] Parameterised queries (no SQL concatenation)
- [ ] Errors do not expose stack traces or internal details to the user
- [ ] Security headers present (CSP, X-Frame-Options, X-Content-Type-Options)
- [ ] Dependencies free of known vulnerabilities (`npm audit` / `pip-audit` clean)
- [ ] Rate limiting configured for public endpoints
- [ ] Logs do not contain PII or secrets

### 4.6 OWASP Top 10 as baseline

Every web application MUST be protected against the current OWASP Top 10. The team reviews the list annually and verifies that every item is covered by tests or configuration.

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
- Every surface in the surface map has at least one contract test
- Validation uses JSON Schema with `additionalProperties: true` (new fields do not break it)
- Fixtures are generated from real interactions, not written by hand
- Set-based assertion for responses with non-guaranteed ordering

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
- **Golden files.** Only for snapshot testing (UI rendering, response schema). Updated explicitly with a flag (`--update-snapshots`), never silently.
- **Seed script.** For development databases, a deterministic script that populates realistic data. Separate from the tests.

### 5.5 Tests in CI

| Trigger | Tiers executed | Timeout | Parallelism |
|---------|-------------|---------|-------------|
| Push to feature branch | Unit + lint | 5 min | Maximum |
| PR towards main | Unit + scenario + integration | 15 min | Per-tier |
| Merge to main | Unit + scenario + integration + E2E | 30 min | Per-tier |
| Scheduled (nightly) | All + full compat matrix | 60 min | Per-slot |
| Release tag | All + smoke tests on staging | 45 min | Sequential |

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

### 6.3 API documentation

Every public API (REST, SDK, CLI) MUST have documentation generated from the code:

| Type | Recommended tool | Output |
|------|------------------|--------|
| REST API | OpenAPI/Swagger (from annotations) | `docs/api/openapi.yaml` |
| TypeScript SDK | TypeDoc | `docs/api/` |
| Python SDK | Sphinx + autodoc | `docs/api/` |
| CLI | `--help` + generated man page | `docs/cli/` |

API documentation is generated in CI and published automatically. Manually written API documentation that diverges from the code is an announced bug.

### 6.4 CHANGELOG.md

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
  lint +         compile       unit +         smoke +        health
  format +       bundle       scenario +      E2E on        check +
  secret         Docker       integration    staging        rollback
  scan           image                                       ready
```

### 7.2 Pipeline stages

#### 7.2.1 Build

- **Compilation** of the source code (TypeScript → JavaScript, etc.)
- **Bundle** for production (tree shaking, minification, source map)
- **Docker image build** tagged based on commit SHA + semantic version
- **Artefacts:** the build produces immutable artefacts; the same artefact tested on staging is the one deployed to production. Never rebuild for production.

#### 7.2.2 Test

Execution of the test tiers according to the table in §5.5.

#### 7.2.3 Stage

- **Automatic deploy to staging** after green tests on `main`
- **Smoke tests** on staging: subset of E2E that verifies critical functionality
- **Full E2E** on staging for release candidates
- **Staging is a replica of production** (same infrastructure, same secrets [rotated], same database schema)

#### 7.2.4 Deploy

- **Production deploy** triggered by a release tag (`v*.*.*`)
- **Rolling update** or **blue-green** — never a "big bang" deploy without automatic rollback
- **Health check** post-deploy: the application responds on `/healthz` within 60 seconds
- **Automatic rollback** if the health check fails after 3 attempts
- **Feature flags** for risky features: deploy the disabled code, enable gradually

### 7.3 Rollback

Every deploy MUST be reversible. Rollback is a first-class operation, not an emergency.

| Scenario | Action | Target time |
|----------|--------|-------------|
| Health check fails post-deploy | Automatic rollback to the previous version | < 2 minutes |
| Critical bug discovered in production | Manual rollback via CI (one button/command) | < 5 minutes |
| Data migration failed | Restore from backup + application rollback | < 30 minutes |
| Rollback not possible (irreversible migration) | Hotfix forward, immediate deploy | Depends on the fix |

**Rule:** if a deploy includes an irreversible database migration, it must be tagged as `BREAKING` in the CHANGELOG and requires explicit approval before deploying.

### 7.4 Database migration

- **Forward-only migration.** Every migration has an `up` file and a `down` file. The `down` is tested — it is not an empty placeholder.
- **Migration separate from the application deploy.** The migration runs before the deploy. If the migration fails, the deploy does not start.
- **Backward compatibility.** The new version of the code MUST work with both the old and the new version of the database for at least one deploy cycle. This allows rollback without rolling back the database.
- **Data migration vs schema migration.** The two are separate. Schema first, data after. Never in the same migration.

### 7.5 Environments

| Environment | Purpose | Data | Deploy |
|----------|-------|------|--------|
| **Local** | Development | Seed script | Manual |
| **CI** | Automated tests | Generated by tests | Automatic on push |
| **Staging** | Pre-production validation | Anonymised copy of production | Automatic on merge to main |
| **Production** | Real users | Real | Manual/automatic on tag |

### 7.6 Configuration as code

- All CI/CD configuration is in the repository (`.github/workflows/`, `.gitlab-ci.yml`, etc.)
- No "click-ops" configuration in the forge — if it is not in the repository, it does not exist
- Forge-specific configuration in `ci/adapters/<forge>/`
- CI business logic (scripts, classifier, aggregator) lives outside the forge directory — it is portable

### 7.7 Adapter pattern for CI

All CI logic that is specific to GitHub Actions (or GitLab, or Forgejo) lives under `ci/adapters/<forge>/`. The rest (scripts, classifier, aggregator, compatibility database) is portable. Migrating to a new forge is a single-directory swap plus a new adapter.

---

# PART II — SURVEILLANCE AND MAINTENANCE

---

## 8. Dependency Surface Map

The surface map is the heart of the surveillance system. It answers the question: **where exactly in the code do I consume each external dependency?**

### 8.1 Definition of surface

A "surface" is any point of contact between the application code and an external resource:

| Type | Examples |
|------|--------|
| REST endpoint | `GET /api/v1/users`, `POST /api/v2/auth/login` |
| WebSocket | `wss://service.example.com/events` |
| SDK method | `client.users.list()`, `db.query()` |
| Data model | JSON schema, protobuf, ORM models |
| Config/env | Environment variables, feature flags, API keys |
| File format | CSV ingest, JSON export, binary protocol |
| CLI tool | Build, linting, deploy commands |

### 8.2 Surface map format

```json
{
  "surfaces": [
    {
      "dependency": "stripe-api",
      "surface": "rest",
      "endpoint": "POST /v1/charges",
      "file": "src/payments/stripe-client.ts",
      "line": 42,
      "method": "POST",
      "context": "createCharge()",
      "risk_weight": "high",
      "test_coverage": true,
      "last_verified": "2026-04-15"
    }
  ],
  "generated_at": "2026-04-15T10:00:00Z",
  "generator": "manual|ast-walker|grep",
  "surface_count": 47
}
```

### 8.3 Generation

Three strategies, in order of reliability:

1. **AST walker** (best) — static analysis of the source code. Resolves template literals, dynamic imports, type inference. Tools: `ts-morph` for TypeScript, `ast` for Python, `go/ast` for Go.
2. **Structured grep** — pattern search with `ripgrep`. Fast but misses dynamic paths.
3. **Manual** — file curated by hand. Acceptable as an initial stub, to be replaced as soon as possible.

### 8.4 Cardinality guard

If the total surface count drops by more than 10% between one generation and the next, CI MUST fail. Catches: refactors that move API calls outside the recognised pattern, configuration changes that exclude files, walker updates.

---

## 9. Surveillance agents

Agents are autonomous processes that monitor external dependencies at regular intervals.

### 9.1 Architecture

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
   │    (cross-ref with surface map)     │
   └──────────────┬──────────────────────┘
                  │
          ┌───────┴────────┐
          ▼                ▼
   ┌────────────┐   ┌────────────┐
   │ REMEDIATION│   │  ADOPTION  │
   │   (fix)    │   │  (improve) │
   └────────────┘   └────────────┘
```

### 9.2 Agent types

**9.2.1 Package Watch** — detects new versions of dependencies. Frequency: 5 min (RSS) or 1h (JSON API). Filter: stable releases only.

**9.2.2 API Probe** — runs contract tests against every endpoint in the surface map. Frequency: 6h for critical endpoints, 24h for others. Verifies: reachability, schema, semantics, new/missing fields, deprecation headers, rate limits, versioning.

**9.2.3 Docs Watch** — monitors changelogs and official documentation. Frequency: 24h. Method: fetch + textual diff.

**9.2.4 Security Watch** — detects security advisories. Frequency: 15 min. Sources: GHSA, NVD, native audit tools. Any advisory forces L2.

**9.2.5 Container/Image Watch** — detects new Docker images. Frequency: 15 min. Timeout: 90 min with backoff.

**9.2.6 State-of-the-Art Scout** — an agent dedicated to state-of-the-art research. Unlike the other agents: it does not monitor a single dependency, but scans the technological landscape around the project. Frequency: quarterly for stable components, monthly for components under active development.

What it does each cycle:

1. **Technology health check.** For every significant technology in the project, verifies: latest release, release frequency over the past year, open issue trends, documentation status, deprecation or end-of-life announcements.

2. **Alternative scanning.** Searches for new libraries or services that solve the same problem as an existing dependency with a different or better approach. Does not suggest switching — it flags that the alternative exists and leaves the decision to the human.

3. **Pattern evolution.** Verifies whether the architectural patterns used in the project are still best practice or whether the community has moved towards different approaches. Looks for: updates to official style guides, new RFCs, talks from key conferences.

4. **Security landscape.** Verifies whether security practices are aligned with current recommendations (OWASP, NIST, CIS).

5. **Ecosystem health.** Assesses the health of the ecosystem: growing or declining community, significant forks, controversies (licence, governance, ownership).

Output: report in `docs/research/` with findings classified into 5 levels: `healthy` (no action), `watch` (monitor in the next cycle), `evaluate` (create ADR with comparison), `migrate` (plan migration in the backlog), `urgent` (immediate action — end-of-life, critical vulnerability, hostile fork).

The agent proactively suggests research when: a new project is started, a dependency is added, an architectural choice is proposed, the project enters a new phase, or N months have passed since the last research on a component. Full details in §1.7.

### 9.3 Heartbeat

Every agent, every cycle — even when nothing is detected — emits a heartbeat. Alert if the most recent is older than 6 hours.

### 9.4 Multi-source configuration

For every critical dependency, at least two sources with different roles: primary (fast trigger) and backstop (recovery). The backstop reconciles missed versions when the primary comes back online.

---

## 10. Change classification

### 10.1 Buckets

| Bucket | Description |
|--------|-------------|
| `data-model` | Changes to schemas, models, types |
| `api-endpoint` | Endpoints added, removed, modified |
| `sdk-method` | Library methods changed |
| `auth` | Authentication, permissions, policies |
| `config` | Environment variables, feature flags |
| `docs-only` | Documentation only |
| `internal` | Internal refactoring, no surface impact |
| `security` | Security patches |
| `deprecation` | Deprecation of existing surfaces |
| `migration` | Migrations that modify existing data |

### 10.2 Severity

| Severity | Definition | Action |
|----------|------------|--------|
| `safe` | `internal` or `docs-only` only | Auto-merge after green CI |
| `additive` | New endpoints, new fields, new libraries | PR with report |
| `breaking` | Surfaces removed, renamed, signature changed | Draft PR + human review |
| `p0` | Security advisory, protocol change | Draft PR + immediate notification |

### 10.3 Never-auto-merge list

Conditions that always force human review: endpoint removal/rename, response format change, auth protocol change, rate limit reduction, SDK method removal, migration that rewrites data, critical/high security advisory, required field change, WebSocket handshake change, functional test regression.

---

## 11. Compatibility test matrix

### 11.1 Slots

| Slot | Definition | Purpose |
|------|------------|---------|
| `latest` | Version that triggered the cycle | Compatibility with the new change |
| `recent` | Most recent stable version (21-day window) | Masked regressions |
| `baseline` | Pinned version, reviewed quarterly | Declared contract |

### 11.2 Run manifest

At the start of each cycle, before any test, the system freezes versions in a JSON manifest. Eliminates ambiguity if the matrix resolves differently between steps.

### 11.3 Test data

1. **Seed workload** — creates data that exercises every consumed surface
2. **Golden queries** — queries with expected results to verify post-migration integrity
3. **Snapshot regression** — loads snapshots from previous versions and verifies data accessibility

---

## 12. Remediation workflow

### 12.1 Autonomy levels

| Level | Trigger | Action | Approval |
|-------|---------|--------|----------|
| **L0** | `safe`, green tests | Auto-merge | None |
| **L1** | `additive`, agentic fix passes correctness gate | PR with fix-claim | Human review |
| **L2** | `breaking`, `p0`, never-auto-merge match | Draft PR + notification | Human intervention |

### 12.2 Correctness gate (L1)

Green CI is not sufficient. The agent MUST: validate against the specific schema that triggered the failure, include a structured fix-claim, add a regression test, limit changes to the client/adapter layer.

### 12.3 Circuit breaker

3 open L1 PRs OR 5 attempts in 14 days → agentic loop paused, everything degrades to L2, human acknowledgement required.

### 12.4 Adoption workflow

When the classifier detects new capabilities: cross-reference with surface map, add wrapper in the client, write contract test, open adoption PR + tracking issue for UI changes.

### 12.5 Deprecation tracking

Record the deprecation, cross-reference with surface map, open `deprecation-watch` issue. Migration is always human-led.

### 12.6 Major version protocol

L1 disabled, coverage baseline resettable, surface map mandatorily regenerated, test harness verified, issue as tracking epic.

### 12.7 Human report

For each change: what changed, classification, where it impacts (files and lines), what must be modified to maintain operability, what can be adopted, test results, recommended action.

---

## 13. Compatibility database

### 13.1 Format

Flat JSON in the repo, one file per version per dependency. No external database.

### 13.2 Events (append-only)

The `events` array is the complete audit trail. Never modify or remove events.

### 13.3 Aggregation

Each slot produces its own payload; an aggregation job merges them. `pass` only if all slots are `pass`. If any slot is `fail`, the rollup is `fail`. If a slot is `error`, the rollup is `partial`.

### 13.4 Portability

Plain JSON in the repo. Migrating to another forge = copy directory + new CI adapter.

---

## 14. Self-testing and observability

### 14.1 Detection heartbeat

Every polling cycle emits a heartbeat. Alert if the most recent is older than 6 hours.

### 14.2 Classifier retrospective

Monthly job: reviews all `safe` auto-merged records from the past 30 days. False negative rate > 10% → alert to recalibrate.

### 14.3 End-to-end canary

Weekly job: injects a synthetic record to verify the entire detection → classification → issue → surface-map cross-ref → event emission path. Cleans up after verification.

### 14.4 Surface map cardinality guard

If the surface count drops > 10%, CI fails.

---

# PART III — MANAGEMENT

---

## 15. Project lifecycle

### 15.1 Phase 0 — Ideation and requirements

1. Write the PRD (§1.2)
2. Define user stories with acceptance criteria (§1.3, §1.4)
3. Document architectural decisions in ADRs (§1.5)
4. Create the backlog ordered by priority (§1.6)
5. Define the Definition of Done (§1.7)
6. Identify critical dependencies and document them in `DEPENDENCIES.md`

### 15.2 Phase 1 — Technical bootstrap

1. Create the directory structure (§2.1)
2. Configure linting, formatting, pre-commit hooks (§3.4)
3. Configure the base CI pipeline (build + lint + unit test) (§7)
4. Write `CLAUDE.md` with operating rules (§2.3)
5. Generate the initial surface map (§8)
6. Configure surveillance agents (§9)
7. Create the first compatibility record (`untested`)
8. Write `.env.example` with all variables documented (§4.4)
9. Write the seed script for the development database (§5.4)

### 15.3 Phase 2 — Active development

1. Work by User Story, respecting the Definition of Done (§1.7)
2. Update `PROJECT_STATUS.md` at every session (§2.2)
3. Write tests for every appropriate tier (§5)
4. Maintain the coverage ratchet (§5.3)
5. Update API documentation and CHANGELOG (§6)
6. Agents run in the background and produce compatibility records
7. Fix and adoption PRs are reviewed and merged
8. Keep the surface map up to date after significant refactors

### 15.4 Phase 3 — Maturity and maintenance

1. Agents continue surveillance
2. Fixes are primarily L0/L1
3. Quarterly review of baseline and thresholds
4. Monthly classifier retrospective
5. Update the never-auto-merge list
6. Annual review of OWASP Top 10 and security practices

### 15.5 Phase 4 — Major dependency upgrade

1. The major-version protocol activates (§12.6)
2. L1 disabled, everything is L2
3. Surface map regenerated
4. Coverage baseline reset
5. Test harness verified
6. Return to phase 3 after migration

---

## 16. Conventions for AI agents

### 16.1 General rules

- The agent reads `CLAUDE.md` before any action
- The agent updates `PROJECT_STATUS.md` after every session
- The agent never modifies files on the never-auto-merge list without human confirmation
- The agent never modifies business logic — only the client/adapter layer and tests
- The agent always includes a regression test for every fix
- The agent does not pretend to execute operations — if it cannot do something, it says so

### 16.2 Grounding on live data

The first step of any fix loop MUST be: retrieve live data from the dependency and pin it in context. Prevents hallucination of non-existent signatures, endpoints, or behaviours.

### 16.3 Mandatory fix-claim

Every PR produced by the agent MUST include a structured fix-claim (§12.2).

### 16.4 Limited scope

The L1 agent may ONLY add new files, new exports, modify files in the client/adapter layer, and add tests.

The L1 agent may NOT modify existing methods, change existing call sites, alter UI behaviour, modify deploy configuration, or delete files or code.

### 16.5 Proposal before code

For complex features, the agent MUST propose the approach in written form (document or comment) and await human approval before writing code. No "surprise" code.

### 16.6 Structured logging

Every agent action is logged as an event in the compatibility database. Everything is traceable, reproducible, and auditable.

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
- [ ] Surface map generated (even manually) (§8)
- [ ] Surveillance agents configured (§9)
- [ ] First compatibility record created (`untested`)
- [ ] `.env.example` with all variables documented (§4.4)
- [ ] Secret scan configured in CI (§4.5)
- [ ] Seed script for development database (§5.4)
- [ ] Initial coverage baseline committed (§5.3)
- [ ] Heartbeat alert configured (threshold: 6 hours) (§14.1)

### A.3 Checklist for every PR

- [ ] Code follows naming conventions (§3.2)
- [ ] Commit message in Conventional Commits format (§3.3)
- [ ] No lint warnings (§3.4)
- [ ] No secrets committed (§4.5)
- [ ] Input validated with schema at every boundary (§4.2)
- [ ] Tests written for new/modified code (§5)
- [ ] Coverage has not dropped below baseline (§5.3)
- [ ] Documentation updated where necessary (§6)
- [ ] Surface map updated if dependencies added/removed (§8)
- [ ] Errors handled explicitly, no empty catch blocks (§3.6)

### A.4 Checklist for release

- [ ] All tests pass across all tiers (§5.5)
- [ ] CHANGELOG.md updated (§6.4)
- [ ] Version tag created (§3.8)
- [ ] Staging deploy succeeded with green smoke test (§7.2.3)
- [ ] Rollback tested (§7.3)
- [ ] Database migration tested (up AND down) (§7.4)
- [ ] API documentation updated (§6.3)
- [ ] Compat database updated with current state (§13)

### A.5 Surveillance checklist

- [ ] Agents active with recent heartbeat (< 6 hours) (§14.1)
- [ ] Weekly canary passed (§14.3)
- [ ] Monthly retrospective executed (§14.2)
- [ ] Never-auto-merge list reviewed (§10.3)
- [ ] Coverage baseline updated (§5.3)
- [ ] Surface map regenerated after refactor (§8)
- [ ] Thresholds reviewed quarterly (§14)
- [ ] State-of-the-Art Scout run in the current quarter (§1.7.5, §9.2.6)
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
- **Surface count:** [number of surfaces in surface map]
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
| **Surface** | Point of contact between application code and an external resource |
| **Surface map** | Structured inventory of all surfaces |
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
