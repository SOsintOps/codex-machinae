## Appendix D — Tooling Specifications

This appendix defines the **contracts** that reference implementations must satisfy. It
specifies input, output, behaviour, and integration points for each tool. The playbook
does not ship implementations — those live in dedicated repositories and are validated
against these specifications.

Each specification follows a common structure: purpose, activation trigger (when the tool
becomes relevant), interface (input/output), behavioural rules, integration with the
playbook, and acceptance criteria.

### D.1 AST Walker — Contract Map Generator

**Purpose:** Automatically generate or update the Boundary Contract Map (§8) by
statically analysing the project's source code.

**Activation trigger:** the project has a codebase with at least one boundary contract
(API endpoint, database schema, external service call, hardware interface, UI data
binding). Relevant whenever §8 applies.

#### D.1.1 Interface

| Parameter | Description |
|-----------|-------------|
| **Input** | Project root path; language/framework hint (optional — auto-detected when possible); existing `COMPATIBILITY.md` (optional — for delta mode) |
| **Output** | `COMPATIBILITY.md` in the format defined by B.8, written to the project root |
| **Mode: full** | Scans the entire codebase and produces a complete contract map from scratch |
| **Mode: delta** | Compares the current codebase against an existing `COMPATIBILITY.md` and reports additions, removals, and changes |
| **Exit codes** | `0` success; `1` new contracts found (delta mode — CI can gate on this); `2` error |

#### D.1.2 Detection rules

The walker must identify boundary contracts by analysing:

| Axis | What to detect | Typical source patterns |
|------|---------------|------------------------|
| **api — inbound** | Exposed endpoints, RPC handlers, GraphQL resolvers, CLI commands | Route decorators, handler registrations, schema definitions |
| **api — outbound** | HTTP clients, SDK calls, gRPC stubs, message-queue producers | Import of client libraries, fetch/request calls, queue publish |
| **data — inbound** | Database reads, file reads, cache gets, event consumers | ORM queries, file-open for read, cache-get calls, subscriber registrations |
| **data — outbound** | Database writes, file writes, cache sets, event producers | ORM save/insert, file-open for write, cache-set calls, publisher calls |
| **ui — outbound** | Data bindings, props passed to UI components, template variables | Framework-specific patterns (React props, template context, view models) |
| **hardware — inbound** | Sensor reads, GPIO inputs, ADC reads, peripheral status | HAL read calls, register reads, device-file reads |
| **hardware — outbound** | Actuator writes, GPIO outputs, DAC writes, display commands | HAL write calls, register writes, device-file writes |

The walker is not required to detect every contract with zero false negatives. The
specification defines a **minimum recall target of 80%** for the supported languages —
the remaining contracts are added manually. False positives are acceptable as long as
the output clearly marks confidence level (`high`, `medium`, `low`) so the analyst can
triage.

#### D.1.3 Language support

The MVP must support at least two languages from different paradigms:

- **TypeScript** (via `ts-morph` or equivalent AST library)
- **Python** (via the `ast` standard-library module)

Additional languages are added as separate parser plugins. The walker architecture must
allow a new language parser to be added without modifying the core detection logic.

#### D.1.4 Behavioural rules

1. The walker never modifies source code — it is read-only.
2. In delta mode, contracts present in the existing map but no longer detected in the
   code are marked `removed?` (with a question mark) rather than silently deleted.
   Only the analyst confirms actual removal.
3. The output format matches B.8 exactly — the walker's output must be valid input for
   the surveillance agent (D.3).
4. The walker logs every detection decision at debug level so false positives can be
   investigated.

#### D.1.5 Integration points

| Playbook reference | Integration |
|--------------------|-------------|
| §8 Boundary Contracts | The walker automates §8.3 (contract-map generation) |
| §11.2 Phase 1 | "Generate the initial contract map" can be executed by the walker |
| §11.6.2 Phase R | Retroactive contract mapping uses the walker in full mode |
| M1 Surveillance | The walker's output feeds M1.3 compatibility records |
| B.8 Contract Map example | The walker's output format matches this template |

#### D.1.6 Acceptance criteria

- [ ] Full mode produces a valid `COMPATIBILITY.md` for a TypeScript project with REST endpoints and a database
- [ ] Full mode produces a valid `COMPATIBILITY.md` for a Python project with HTTP clients and file I/O
- [ ] Delta mode correctly identifies added and removed contracts against a known baseline
- [ ] Confidence tagging (`high`/`medium`/`low`) is present on every detected contract
- [ ] Exit code 1 in delta mode when new contracts are found
- [ ] Output passes structural validation against B.8 format

---

### D.2 Coverage Ratchet — CI Step

**Purpose:** Enforce the coverage-ratchet mechanism (§5.3) as an automated CI step that
fails the pipeline when test coverage drops below the committed baseline.

**Activation trigger:** the project has a test suite that produces a coverage report.
Relevant whenever §5.3 applies.

#### D.2.1 Interface

| Parameter | Description |
|-----------|-------------|
| **Input** | Path to the coverage report (auto-detected or explicit); path to the baseline file (default: `.coverage-baseline.json`) |
| **Output** | Pass/fail verdict; human-readable summary (lines covered, delta, threshold); updated baseline file (on pass, if `--update` flag is set) |
| **Formats supported** | Cobertura XML, lcov, Istanbul JSON, coverage.py JSON — at minimum two of these |
| **Exit codes** | `0` coverage at or above baseline; `1` coverage below baseline; `2` configuration or parse error |

#### D.2.2 Baseline file format

```json
{
  "version": 1,
  "updated": "YYYY-MM-DDTHH:MM:SSZ",
  "line_coverage_pct": 78.4,
  "branch_coverage_pct": 62.1,
  "escape_valves": [
    {
      "path": "src/legacy/parser.ts",
      "reason": "Legacy code pending rewrite — US-042",
      "expires": "2026-06-30",
      "approved_by": "analyst-name"
    }
  ]
}
```

#### D.2.3 Behavioural rules

1. The ratchet only moves upward. If the current coverage exceeds the baseline, the
   baseline is updated automatically when `--update` is passed (typically on merge to
   the main branch).
2. **Escape valves** (§5.3) are respected: files listed in `escape_valves` are excluded
   from the ratchet comparison. Expired escape valves (past their `expires` date) are
   treated as if they do not exist — the file's coverage counts again.
3. The tool never modifies test files or source code — it is a read-only comparator
   with optional baseline-file write.
4. When coverage drops, the output names the specific files or modules responsible for
   the regression, ordered by impact (largest drop first).

#### D.2.4 Integration points

| Playbook reference | Integration |
|--------------------|-------------|
| §5.3 Coverage ratchet | Direct implementation of the ratchet mechanism |
| §7.2 Pipeline stages | Runs in the Build or Stage phase of the pipeline |
| §11.2 Phase 1 | "Initial coverage baseline committed" is produced by `--update` on first run |
| A.2 Phase 1 checklist | Satisfies "Initial coverage baseline committed (§5.3)" |

#### D.2.5 Acceptance criteria

- [ ] Correctly parses at least two coverage-report formats (e.g. Cobertura XML + Istanbul JSON)
- [ ] Exit code 0 when coverage is at or above baseline
- [ ] Exit code 1 when coverage drops, with file-level regression report
- [ ] Escape valves correctly exclude listed files from comparison
- [ ] Expired escape valves are ignored (file counts toward coverage again)
- [ ] `--update` flag writes the new baseline only when coverage has increased

---

### D.3 Surveillance Agent Scaffold

**Purpose:** Provide a minimal but functional surveillance agent (M1.1) that
periodically runs contract tests, produces compatibility records (M1.3), and opens
issues when a contract breaks.

**Activation trigger:** M1 Surveillance is active and the project has at least one
outbound boundary contract worth monitoring.

#### D.3.1 Interface

| Parameter | Description |
|-----------|-------------|
| **Input** | `COMPATIBILITY.md` (contract map); test commands per contract (configured in a manifest file); issue-tracker integration config (GitHub Issues, GitLab Issues, or Linear) |
| **Output** | Compatibility records (M1.3 format, written to `docs/compatibility/`); issues opened for broken contracts; heartbeat signal (M1.4.1) |
| **Execution model** | Cron-scheduled (recommended: every 6 hours, configurable). Stateless between runs — all state is in committed artefacts |

#### D.3.2 Manifest file format

```yaml
version: 1
schedule: "0 */6 * * *"
contracts:
  - id: "api-out-stripe"
    test_command: "npm test -- --grep 'stripe contract'"
    timeout_seconds: 120
    severity_on_failure: "breaking"
  - id: "data-out-postgres"
    test_command: "pytest tests/contracts/test_postgres.py"
    timeout_seconds: 60
    severity_on_failure: "additive"
issue_tracker:
  provider: "github"
  repository: "org/repo"
  labels: ["surveillance", "contract-break"]
```

#### D.3.3 Behavioural rules

1. Each run tests every contract listed in the manifest. A contract that was `compatible`
   and now fails transitions to `incompatible` — a new compatibility record is written
   and an issue is opened.
2. A contract that was `incompatible` and now passes transitions to `compatible` — the
   record is updated and the corresponding issue is closed (or commented on, if manual
   close is preferred).
3. The agent never modifies source code or tests — it only runs existing test commands
   and writes records.
4. The heartbeat (M1.4.1) is a timestamp file (`docs/compatibility/.heartbeat`) updated
   at the end of every run. If the heartbeat is older than the configured threshold
   (default: 6 hours), external monitoring should alert.
5. If a test command times out, the contract status is recorded as `timeout` and the
   issue is opened with a timeout label.
6. The agent produces a structured log of every run (contracts tested, results, issues
   opened/closed) for auditability (§12.6).

#### D.3.4 Compatibility record format

Each record follows the B.5 template. The agent writes one file per run per contract
that changed status:

```
docs/compatibility/YYYY-MM-DD-<contract-id>.md
```

Records for unchanged contracts are not duplicated — only transitions generate new files.

#### D.3.5 Integration points

| Playbook reference | Integration |
|--------------------|-------------|
| M1.1 Surveillance agents | The scaffold implements the agent described in M1.1 |
| M1.3 Compatibility records | Output format matches B.5 |
| M1.4.1 Heartbeat | The `.heartbeat` file implements the heartbeat mechanism |
| M1.4.2 Classifier retrospective | Run logs provide input for monthly retrospectives |
| §8 Boundary Contracts | The manifest references contract IDs from the contract map |
| D.1 AST Walker | The walker's output (`COMPATIBILITY.md`) is the agent's input |

#### D.3.6 Acceptance criteria

- [ ] Runs all contracts listed in the manifest and produces correct compatibility records
- [ ] Transitions (`compatible` → `incompatible` and vice versa) trigger issue creation/closure
- [ ] Heartbeat file is updated at the end of every run
- [ ] Timeout handling produces a `timeout` status and opens an issue
- [ ] Structured run log is produced for every execution
- [ ] Stateless between runs — deleting all local state except committed artefacts and re-running produces identical results
