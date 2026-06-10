## Appendix A — Phase checklists

Each checklist is split into **Core** items (always apply) and **conditional** blocks that
activate only when the named module or domain appendix is active. Skip a conditional block
entirely when its trigger has not fired.

Items tagged with a profile downgrade (e.g. `[Solo: optional]`) follow the rules in §2.5.
Untagged items are mandatory for all profiles.

### A.1 Phase 0 checklist (Requirements)

**Core**

- [ ] PRD written with all mandatory sections (§1.2) `[Solo: recommended]`
- [ ] State-of-the-art research conducted for the project domain (§1.7)
- [ ] Pre-implementation checklist in the PRD completed and verified `[Solo: recommended]`
- [ ] User stories with acceptance criteria for the first sprint `[Solo: optional]`
- [ ] ADRs for fundamental architectural decisions (with "Alternatives rejected" from real research) `[Solo: recommended]`
- [ ] Backlog created and ordered by priority `[Solo: optional]`
- [ ] Definition of Done defined and shared
- [ ] Critical dependencies identified in `DEPENDENCIES.md` (with alternatives comparison §1.7.1)

**When M4 Classification & Taxonomy is active**

- [ ] Scouting protocol (M4.3) executed for every domain the project touches
- [ ] Taxonomy decisions recorded in `docs/taxonomy/registry.md`

### A.2 Phase 1 checklist (Bootstrap)

**Core**

- [ ] Directory structure created (§2.1)
- [ ] Linter + formatter configured and integrated into CI (§3.4)
- [ ] Base CI pipeline working (build + lint + unit) (§7) `[Solo: recommended]`
- [ ] Agent configuration written (§2.4)
- [ ] Contract map generated (even manually) (§8) `[Solo: recommended]`
- [ ] `.env.example` with all variables documented (§4.3)
- [ ] Initial coverage baseline committed (§5.3) `[Solo: recommended]`

**When M1 Surveillance is active**

- [ ] Surveillance agents configured (M1.1)
- [ ] First compatibility record created (`untested`)
- [ ] Heartbeat alert configured (threshold: 6 hours) (M1.4.1) `[Small: recommended]`

**When M2 Security-sensitive is active**

- [ ] Secret scan configured in CI (M2.2)

**When the project has persistent structured data**

- [ ] Seed script for development database (§5.4)

**When D4 Embedded / Firmware is active**

- [ ] Toolchain version locked (D4.2)
- [ ] Binary-size baseline committed (D4.2)
- [ ] Power budget document created (D4.5)

### A.3 Checklist for every PR

**Core**

- [ ] Code follows naming conventions (§3.2)
- [ ] Commit message in Conventional Commits format (§3.3)
- [ ] No lint warnings (§3.4)
- [ ] Input validated with schema at every boundary (§4.2)
- [ ] Tests written for new/modified code (§5)
- [ ] Coverage has not dropped below baseline (§5.3) `[Solo: recommended]`
- [ ] Documentation updated where necessary (§6)
- [ ] Contract map updated if dependencies added/removed (§8) `[Solo: recommended]`
- [ ] Errors handled explicitly, no empty catch blocks (§3.6)

**When M2 Security-sensitive is active**

- [ ] No secrets committed (verified by tools: `trufflehog`, `gitleaks`) (M2.2)
- [ ] Parameterised queries — no SQL concatenation (M2.2)
- [ ] Errors do not expose stack traces or internal details to the user (M2.2)
- [ ] Security headers present (CSP, X-Frame-Options, X-Content-Type-Options) (M2.2)
- [ ] Dependencies free of known vulnerabilities (M2.4)
- [ ] Logs do not contain PII or secrets (M2.2)

**When D1 Web Service is active**

- [ ] Rate limiting configured for public endpoints (D1.5)
- [ ] Negative-path tests cover the endpoint (D1.4)

**When D2 Library / SDK is active**

- [ ] Public API surface unchanged on minor/patch bump (D2.4)
- [ ] Deprecated symbols annotated with replacement and removal version (D2.3)

**When D3 CLI Tool is active**

- [ ] Exit codes match documented contract (D3.3)
- [ ] `--json` output schema unchanged on minor/patch bump (D3.4)

**When D4 Embedded / Firmware is active**

- [ ] Binary size has not regressed beyond threshold (D4.2)
- [ ] Power budget updated if a component or duty cycle changed (D4.5)

**When D6 Mobile App is active**

- [ ] Minimum OS version policy respected (D6.3)
- [ ] Crash-reporting symbolication files included in build (D6.4)
- [ ] Offline behaviour tested for modified code paths (D6.5)

**When D7 Static Site / Frontend-only is active**

- [ ] Bundle size has not regressed beyond budget (D7.1)
- [ ] Automated accessibility audit passed (D7.4)
- [ ] No new accessibility violations from axe-core or equivalent (D7.4)

**When M4 Classification & Taxonomy is active**

- [ ] Taxonomy terms follow MECE and parsimony principles (M4.1)
- [ ] Machine-readable serialisation updated if taxonomy changed (M4.6)

### A.4 Checklist for release

**Core**

- [ ] All tests pass across all tiers (§5.5)
- [ ] CHANGELOG.md updated (§6.3)
- [ ] Version tag created (§3.8)
- [ ] Pre-production smoke tests green on promotion (§7.2) `[Solo: optional]`
- [ ] Rollback tested (§7.3) `[Solo: recommended]`

**When D1 Web Service is active**

- [ ] API documentation regenerated (D1.1)
- [ ] Health and readiness endpoints verified (D1.6)

**When D2 Library / SDK is active**

- [ ] API documentation regenerated (D2.1)
- [ ] Breaking-change detection passed (D2.4)
- [ ] Version bump matches SemVer rules (D2.2)
- [ ] Deprecation window respected for removed symbols (D2.3)
- [ ] Package published via CI pipeline, not manually (D2.5)

**When D3 CLI Tool is active**

- [ ] CLI documentation regenerated (D3.1)
- [ ] All exit codes tested (D3.3)
- [ ] Shell completions regenerated (D3.5)
- [ ] Installation channels built and checksummed (D3.6)

**When D4 Embedded / Firmware is active**

- [ ] Firmware image signed (D4.4)
- [ ] A/B partition rollback verified (D4.4)
- [ ] Bring-up checklist completed for new board revisions (D4.6)

**When D5 ML / Data Pipeline is active**

- [ ] Database migration tested (up AND down) (D5.2)
- [ ] Evaluation contract passed for any updated model (D5.6)

**When D6 Mobile App is active**

- [ ] Signed build artefact produced by CI (D6.1)
- [ ] Internal and external testing completed (D6.1)
- [ ] Staged rollout configured — not releasing to 100% immediately (D6.2)
- [ ] Symbolication files uploaded to crash-reporting service (D6.4)
- [ ] Store metadata updated (screenshots, description, what's new) (D6.1)

**When D7 Static Site / Frontend-only is active**

- [ ] Bundle budgets met (D7.1)
- [ ] Source maps uploaded to error-reporting service (D7.3)
- [ ] Manual accessibility audit completed for significant UI changes (D7.4)
- [ ] Core Web Vitals within "good" thresholds in Lighthouse CI (D7.5)
- [ ] Cache-invalidation strategy verified (content-hashed assets, short HTML TTL) (D7.2)

**When M1 Surveillance is active**

- [ ] Compat database updated with current state (M1.3)

**When M3 Release & Distribution is active**

- [ ] CHANGELOG entry generated and human-edited (M3.2)
- [ ] Artefact checksum file published (M3.3)
- [ ] Artefact signed or provenance attested where required (M3.3)
- [ ] Release notes published (developer-facing; end-user-facing where applicable) (M3.4)
- [ ] Release cadence respected — no freeze-window violations (M3.1)

### A.5 Surveillance checklist (M1 — periodic)

This checklist applies only when M1 Surveillance is active.

- [ ] Agents active with recent heartbeat (< 6 hours) (M1.4.1) `[Small: recommended]`
- [ ] Weekly canary passed (M1.4.3) `[Small: recommended]`
- [ ] Monthly retrospective executed (M1.4.2) `[Small: recommended]`
- [ ] Never-auto-merge list reviewed (§9.3)
- [ ] Coverage baseline updated (§5.3)
- [ ] Contract map regenerated after refactor (§8)
- [ ] Thresholds reviewed quarterly (M1.4) `[Small: recommended]`
- [ ] State-of-the-Art Scout run in the current quarter (§1.7.5, M1.1.2.6)
- [ ] SOTA reports reviewed and actions planned for `evaluate` or `migrate` signals

### A.6 Security review checklist (M2 — periodic)

This checklist applies only when M2 Security-sensitive is active.

- [ ] OWASP Top 10 review table updated within the past 12 months (M2.3)
- [ ] Dependency-vulnerability backlog triaged — no critical/high advisories past SLA (M2.4)
- [ ] Secret-scanning tool coverage verified (no new file patterns excluded) (M2.2)

### A.7 Taxonomy audit checklist (M4 — quarterly)

This checklist applies only when M4 Classification & Taxonomy is active.

- [ ] Coverage audit completed (M4.5)
- [ ] Ambiguity audit completed (M4.5)
- [ ] False-positive audit completed (M4.5)
- [ ] Drift audit completed (M4.5)
- [ ] Staleness audit completed — stale terms sent to deprecation review (M4.5)
- [ ] Machine-readable serialisation in sync with human-readable docs (M4.6)
- [ ] Upstream contributions tracked and statuses updated (M4.7)

### A.8 Phase R checklist (Retrofit)

This checklist applies when adopting Codex Machinae on an existing project (§11.6).

**Debt-scoping audit (§11.6.1)**

- [ ] `RETROFIT_AUDIT.md` produced and committed
- [ ] Requirements artefacts gap assessed (PRD, stories, ADRs)
- [ ] Code quality gap assessed (linting, formatting, commits)
- [ ] Security posture reviewed (secrets, input validation)
- [ ] Test coverage measured and ratchet starting point set (§5.3)
- [ ] Documentation gaps identified (README, CHANGELOG, code comments)
- [ ] CI/CD pipeline gap analysed against §7

**Contract mapping (§11.6.2)**

- [ ] Boundary Contract Map generated from existing codebase (§8)
- [ ] All integration points classified by axis and direction
- [ ] Undocumented or implicit contracts flagged as high-risk

**Adoption tiers (§11.6.3)**

- [ ] T1 (Safety net) completed — coverage ratchet, secrets audit, CI baseline
- [ ] T2 (Structure) completed — directory layout, agent config, CHANGELOG, contract map
- [ ] T3 (Process) completed — module activation, checklist adoption, Definition of Done

**Module activation (§11.6.4)**

- [ ] All module triggers evaluated against existing codebase
- [ ] Active modules' artefacts populated retroactively

**Lifecycle entry (§11.6.5)**

- [ ] Target phase determined (Phase 2 or Phase 3)
- [ ] `PROJECT_STATUS.md` created or updated to reflect current phase

### A.9 Multi-agent setup checklist (§12.7 — when activated)

This checklist applies only when the analyst has chosen to employ multiple agents.

**Designation and partitioning**

- [ ] Lead agent nominated and recorded in agent-configuration file (§12.7.1)
- [ ] Scope partition defined and documented (§12.7.2)
- [ ] Each agent's perimeter confirmed as non-overlapping
- [ ] Write-access categories assigned to shared artefacts (§12.7.4)

**Mixed-LLM (if applicable)**

- [ ] Provider-specific config files consistent with shared `AI-AGENTS.md` (§12.7.6)
- [ ] No contradictions between provider-specific instructions and scope partition

**Operational**

- [ ] Handover note format agreed (§12.7.5)
- [ ] Conflict-prevention protocol understood by all participating agents (§12.7.3)

---

