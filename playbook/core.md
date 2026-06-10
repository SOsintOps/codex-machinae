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

### 2.5 Project-size profile

The project declares a **size profile** that modulates which checklist items (Appendix A)
are mandatory, recommended, or optional. The profile is declared once in the agent
configuration file (§2.4) and applies for the project's lifetime unless explicitly changed.

| Profile | Typical team | Typical codebase | When to choose |
|---------|-------------|------------------|----------------|
| **Solo** | 1 person | < 5 000 lines | Side projects, prototypes, personal tools, early-stage exploration |
| **Small** | 2–5 people | 5 000–50 000 lines | Startup MVPs, internal tools, focused microservices |
| **Large** | 6+ people | > 50 000 lines | Production systems, multi-team projects, regulated environments |

**How profiles interact with checklists:**

Each checklist item in Appendix A carries an implicit default of **mandatory for all
profiles**. Items that are downgraded for smaller profiles are tagged inline:

- ⬇ `[Small: recommended]` — mandatory for Large, recommended for Small and Solo.
- ⬇ `[Solo: optional]` — mandatory for Large and Small, optional for Solo.
- ⬇ `[Small: optional]` — mandatory for Large, optional for Small and Solo.

Items without a tag are mandatory regardless of profile. The tagging is deliberately
conservative: most items remain mandatory because the playbook's value comes from
discipline, not from cutting corners. The profile exists to acknowledge that a solo
developer maintaining a personal tool does not need the same ceremony as a regulated
production system.

**Rules:**

1. The profile does not affect Core sections (§§1–12) — those rules apply universally.
   Only checklist *items* in Appendix A are modulated.
2. "Recommended" means the item should be done unless there is a concrete reason not to.
   "Optional" means the item adds value but can be skipped without risk.
3. A project may upgrade its profile at any time (Solo → Small, Small → Large). Downgrading
   requires a conscious review: items that were mandatory under the old profile and are now
   optional must be explicitly evaluated, not silently dropped.
4. When in doubt, choose the higher profile. Over-engineering process is cheaper than
   under-engineering quality.

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
- A schema change on a shared contract is a contract-breaking change (§10.7) regardless of whether any current consumer happens to tolerate it

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

### 10.4 Human-agent handover

When the circuit breaker trips (§10.3), the agent MUST produce a **handover dossier** before degrading to L2. The dossier is attached to the tracking issue and contains:

| Section | Content |
|---------|---------|
| **Trigger summary** | Which contract, what classification, what change triggered the sequence |
| **Attempt log** | For each failed L1 attempt: PR link, fix-claim, test result, reason for failure |
| **Root-cause hypothesis** | The agent's best assessment of why the fix did not hold (schema mismatch, upstream regression, environmental) |
| **Blast radius** | Files, endpoints, and downstream consumers affected |
| **Suggested next steps** | Concrete actions the human can take, ranked by likelihood of success |
| **Reproduction steps** | Minimal steps or commands to reproduce the failure locally |

The dossier reduces the human's ramp-up time from "read three PRs and guess" to "read one summary and act". The agent does not attempt further automation on the affected contract until the human explicitly re-enables L1.

### 10.5 Adoption workflow

When a change is classified as introducing new capabilities in an existing contract: cross-reference with the Boundary Contract Map, add a wrapper in the client, write a contract test, open an adoption PR + tracking issue for UI changes.

### 10.6 Deprecation tracking

Record the deprecation, cross-reference with the Boundary Contract Map, open a `deprecation-watch` issue. Migration is always human-led.

### 10.7 Contract-breaking change protocol

Triggered whenever a tracked contract breaks (major version bump of an outbound dependency, incompatible schema change, endpoint removal, hardware protocol revision, UI-flow breaking change). Actions: L1 disabled for the affected contract, coverage baseline resettable, Boundary Contract Map mandatorily regenerated, test harness verified end-to-end, issue opened as a tracking epic.

### 10.8 Human report

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

1. The major-version protocol activates (§10.7)
2. L1 disabled, everything is L2
3. Contract map regenerated (§8)
4. Coverage baseline reset (§5.3)
5. Test harness verified
6. Return to Phase 3 after migration

### 11.6 Phase R — Retrofit (existing projects)

Phase R applies when the Codex Machinae is adopted on a project that already has code,
history, and technical debt. Unlike Phases 0–4, Phase R is not sequential — it is a
one-time convergence protocol that brings the project into a state from which it can
enter the normal lifecycle at Phase 2 or Phase 3 depending on its maturity.

**Trigger:** the project has existing source code, a repository with history, and at
least one deployed or distributable artefact. If the project is greenfield, start at
Phase 0 instead.

#### 11.6.1 Debt-scoping audit

Before any change, produce a structured assessment of the gap between the project's
current state and the playbook's expectations. The audit covers:

| Area | What to check | Output |
|------|---------------|--------|
| Requirements artefacts | PRD, user stories, ADRs, backlog | List of missing or incomplete artefacts |
| Project structure | Directory layout (§2.1), configuration files, agent config (§2.4) | Conformance delta |
| Code quality | Linting, formatting, commit conventions (§3) | Gap list with estimated effort |
| Security posture | Secrets management (§4.3), input validation (§4.2) | Risk register |
| Test coverage | Current coverage vs playbook baseline (§5.3), tier distribution | Coverage report + ratchet starting point |
| Documentation | README, CHANGELOG, code comments (§6) | Missing-doc list |
| CI/CD | Pipeline maturity vs §7 expectations | Pipeline gap analysis |
| Boundary contracts | Existing integration points vs contract map (§8) | Draft contract map |

The audit result is a document (`RETROFIT_AUDIT.md`) committed to the repository root.
It is the single source of truth for retrofit planning.

#### 11.6.2 Retroactive contract mapping

Generate the Boundary Contract Map (§8) from the existing codebase. For each integration
point discovered:

1. Classify by axis (api, data, ui, hardware) and direction (inbound, outbound, bidirectional)
2. Record the current compatibility status (`untested`, `compatible`, `incompatible`)
3. Note any undocumented or implicit contracts — these are the highest-risk items

The contract map is the foundation for activating M1 Surveillance and for understanding
the project's blast radius on dependency changes.

#### 11.6.3 Prioritised adoption plan

Using the audit and the contract map, produce an ordered adoption plan. The plan groups
work into three tiers:

| Tier | Criteria | Examples |
|------|----------|----------|
| **T1 — Safety net** | Items that prevent silent regression or data loss | Coverage ratchet (§5.3), secrets audit (§4.3), CI pipeline baseline (§7) |
| **T2 — Structure** | Items that bring the project into conformance with Core conventions | Directory layout (§2.1), agent config (§2.4), CHANGELOG (§6.3), contract map (§8) |
| **T3 — Process** | Items that enable ongoing lifecycle operations | Surveillance activation (M1), checklist adoption (Appendix A), Definition of Done (§1.8) |

Each tier is a commit boundary. T1 is non-negotiable and must be completed before T2
begins. T2 and T3 may be interleaved if the project's context demands it, but T1 always
comes first.

#### 11.6.4 Module activation

During retrofit, modules and domain appendices are activated exactly as in a greenfield
project: when the trigger fires (§2.2). The difference is that triggers may already be
satisfied by the existing codebase. The agent or analyst walks the trigger list and
activates every module whose condition is met.

Modules activated during retrofit follow the same rules as in the normal lifecycle, but
the initial state of their artefacts (compatibility records, security reviews, taxonomy
registries) is populated retroactively rather than incrementally.

#### 11.6.5 Entry into the normal lifecycle

Once T1 and T2 are complete, the project enters the normal lifecycle:

- If the project is actively developed and receives regular feature work → enter at
  **Phase 2** (§11.3).
- If the project is stable and receives only maintenance and dependency updates → enter
  at **Phase 3** (§11.4).

The `RETROFIT_AUDIT.md` remains in the repository as a historical record. It is not
updated after entry into the normal lifecycle — `PROJECT_STATUS.md` takes over.

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

### 12.7 Multi-agent coordination (optional)

This subsection activates only when the analyst chooses to employ more than one agent on
the same project. It is not a requirement — single-agent operation remains the default.
The protocol is LLM-agnostic: an "agent" may be any model (Claude, Gemini, Copilot, or
any other provider). Multi-agent covers both multiple instances of the same LLM and
mixed-LLM teams. Every participating agent must individually comply with §§12.1–12.6
regardless of the coordination protocol.

#### 12.7.1 Lead agent designation

The analyst nominates one agent as the **lead**. The lead is the single writer for
coordination artefacts (`PROJECT_STATUS.md`, the Boundary Contract Map, `CHANGELOG.md`).
All other agents read those files but do not modify them. If an agent needs a
coordination artefact updated, it requests the change from the lead or from the analyst.

The lead designation is recorded in the project's agent-configuration file (§2.4) so
that every agent can identify it at session start.

#### 12.7.2 Scope partitioning

Each agent receives an explicit perimeter before starting work. Partitioning may be by:

| Strategy | When to use | Example |
|----------|-------------|---------|
| **By module/domain** | Large projects with independent subsystems | Agent A owns D1, Agent B owns D5 |
| **By directory** | When module boundaries map cleanly to folders | Agent A owns `src/api/`, Agent B owns `src/ml/` |
| **By user story** | Sprint-based work with non-overlapping stories | Agent A works on US-007, Agent B on US-012 |

The analyst documents the partition in the agent-configuration file or in
`PROJECT_STATUS.md`. An agent must not operate outside its assigned perimeter without
explicit analyst approval.

#### 12.7.3 Conflict prevention

1. **File-level exclusivity** — a file being modified by one agent is off-limits to
   others until the change is committed. Agents declare intent before editing by noting
   the target file in their session log.
2. **Lead coordination** — when two agents must touch the same file, the lead (or the
   analyst) determines the sequence. The second agent waits until the first agent's
   commit is merged.
3. **Merge conflicts** — if a conflict arises despite the protocol, resolution always
   requires human intervention. No agent auto-resolves merge conflicts in a multi-agent
   context.

#### 12.7.4 Shared artefacts protocol

Files are classified by write access:

| Category | Write access | Examples |
|----------|-------------|----------|
| **Single-writer** | Lead agent only | `PROJECT_STATUS.md`, contract map (§8), `CHANGELOG.md` |
| **Partitioned** | Owning agent per scope partition | Source code, tests, domain-specific docs |
| **Human-only** | No agent writes without explicit approval | Never-auto-merge list (§9.3), agent-configuration file (§2.4) |

An agent encountering a file outside its write-access category must request the change
through the lead or the analyst rather than editing directly.

#### 12.7.5 Inter-agent handover

When work passes from one agent to another (shift change, scope transfer, or escalation),
the outgoing agent produces a structured handover note:

| Field | Content |
|-------|---------|
| **Scope completed** | List of files changed, stories closed, tests added |
| **Decisions taken** | Architectural or design choices made during the session |
| **Open blockers** | Issues that prevented completion, with root-cause hypotheses |
| **Context for the next agent** | Key findings, relevant file locations, state of any in-progress work |

The handover note is appended to the session log or committed as a standalone file in
the project's documentation directory. The receiving agent reads it before starting work.

#### 12.7.6 Mixed-LLM considerations

When agents from different LLM providers collaborate:

- Each agent's configuration file (§2.4) is provider-specific (`CLAUDE.md`, `GEMINI.md`,
  etc.) but all share the common rules in `AI-AGENTS.md`.
- Agents must not assume shared context or memory between providers. All coordination
  happens through committed artefacts, not through implicit state.
- The analyst is responsible for ensuring that provider-specific instructions do not
  contradict the shared rules or the scope partition.

---

