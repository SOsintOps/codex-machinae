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

