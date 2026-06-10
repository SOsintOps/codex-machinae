## Appendix C — Glossary

| Term | Definition |
|------|------------|
| **PRD** | Product Requirements Document — specification of the what and the why |
| **ADR** | Architecture Decision Record — documented architectural decision |
| **User Story** | Functional requirement from the user's perspective |
| **Acceptance Criteria** | Binary conditions that define "done" |
| **Definition of Done** | Universal checklist applied to every work item |
| **Domain appendix** | A section of the playbook (D1–D7) that adds project-type-specific content on top of Core when its activation trigger fires |
| **Cross-cutting module** | A section of the playbook (M1–M4) that adds capability-specific content composable with any domain when its activation trigger fires |
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
| **HAL** | Hardware Abstraction Layer — thin interface isolating application code from peripheral access (D4.1) |
| **HIL** | Hardware-in-the-loop — test tier that exercises code on real hardware or a cycle-accurate simulator (D4.3) |
| **Data drift** | Divergence of incoming feature distributions from the training distribution (D5.5) |
| **Concept drift** | Change in the relationship between features and the target, degrading model quality (D5.5) |
| **Evaluation contract** | Versioned specification of how a model's quality is measured before promotion (D5.6) |
| **Taxonomy** | A structured classification of terms in a domain, following MECE and parsimony principles (M4.1) |
| **Scouting protocol** | The process by which the AI discovers domain-specific frameworks for adoption (M4.3) |
| **MECE** | Mutually Exclusive, Collectively Exhaustive — design constraint for taxonomies (M4.1) |
| **SOTA Scout** | Agent that researches the state of the art for project technologies and patterns |
| **Technology health check** | Periodic health verification of a technology (releases, community, trends) |
| **Alternative scanning** | Search for libraries or services alternative to those in use |
| **Pattern evolution** | Monitoring of the evolution of architectural best practices in the industry |
| **Back-pressure** | Load-shedding mechanism (circuit breaker, timeout, bulkhead) preventing cascading failure (D1.5) |
| **Semantic versioning (SemVer)** | Versioning scheme (major.minor.patch) encoding backwards-compatibility promises for published packages (D2.2) |
| **Deprecation window** | Minimum period during which a deprecated symbol remains functional before removal (D2.3) |
| **Breaking-change detection** | Automated CI step comparing current public API surface against the last published version (D2.4) |
| **Exit-code contract** | Documented mapping between CLI exit codes and their meaning, tested in CI (D3.3) |
| **Shell completion** | Auto-generated scripts enabling tab-completion of CLI subcommands and flags (D3.5) |
| **Release cadence** | The model governing when releases are cut: release-when-ready, release train, or event-driven (M3.1) |
| **Freeze window** | The final portion of a release-train cycle during which only fixes enter the release branch (M3.1) |
| **Artefact provenance** | Attestation tying a published artefact to its source commit, build platform, and builder identity (M3.3) |
| **Release yank** | Registry mechanism that marks a published version as unsuitable without deleting it (M3.5) |
| **Bundle budget** | Size threshold for production JS/CSS/image artefacts, enforced as a ratchet in CI (D7.1) |
| **Core Web Vitals** | Google's metrics for loading (LCP), responsiveness (INP), and visual stability (CLS) (D7.5) |
| **Cache-invalidation strategy** | The rules governing how CDN/browser caches are cleared on deployment (D7.2) |
| **Staged rollout** | Percentage-based release to mobile users, gated by crash-rate and quality metrics (D6.2) |
| **Crash-free rate** | Percentage of user sessions without an unhandled crash, monitored as a quality threshold (D6.4) |
| **OTA update (mobile)** | Code update delivered directly to the app, bypassing the store review cycle (D6.6) |
| **OTA** | Over-the-air — firmware update delivered via network (D4.4) |
| **A/B partitioning** | Firmware update strategy maintaining two slots for automatic rollback (D4.4) |
| **Phase R (Retrofit)** | One-time convergence protocol for adopting the playbook on an existing project (§11.6) |
| **Retrofit audit** | Structured gap assessment between a project's current state and the playbook's expectations (§11.6.1) |
| **Debt-scoping** | The process of measuring the distance between an existing project and playbook conformance (§11.6.1) |
| **Adoption tier** | Priority grouping (T1 safety net, T2 structure, T3 process) for ordering retrofit work (§11.6.3) |
| **Lead agent** | The agent designated as single writer for coordination artefacts in a multi-agent setup (§12.7.1) |
| **Scope partition** | Explicit assignment of non-overlapping work perimeters to agents in a multi-agent setup (§12.7.2) |
| **Inter-agent handover** | Structured note transferring context from one agent to another during shift change or scope transfer (§12.7.5) |
| **Project-size profile** | Declaration (Solo, Small, Large) that modulates checklist obligation levels in Appendix A (§2.5) |
| **AST Walker** | Static-analysis tool that generates the Boundary Contract Map by scanning source code (Appendix D.1) |
| **Coverage ratchet (tool)** | CI step that enforces the coverage-ratchet mechanism by comparing coverage reports against a committed baseline (Appendix D.2) |
| **Surveillance agent scaffold** | Minimal agent that runs contract tests on a schedule and produces compatibility records (Appendix D.3) |

---

