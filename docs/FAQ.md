# Frequently Asked Questions

---

## General

### What is Codex Machinae?

A universal, modular meta-framework that defines **how** to structure, develop, test,
and maintain software when one or more AI agents collaborate with human developers.
It is a process specification, not a template generator or a CLI tool.

### Who is it for?

Solo developers, small teams, and large organisations that use LLM-based agents
(Claude, Gemini, GPT, Copilot, local models, or any combination) as active
collaborators — not just autocomplete. The playbook scales via project-size
profiles (§2.5): Solo, Small, and Large.

### Do I need to adopt the entire playbook?

No. Only Part I (Core, §§1–12) is universal. Domain appendices (D1–D7) and
cross-cutting modules (M1–M4) activate only when their trigger fires (§2.2,
Emergent Expansion Protocol). You never carry weight you do not need.

### Can I use it on an existing project?

Yes. Phase R (§11.6) is a dedicated retrofit protocol. It guides you through a
debt-scoping audit, retroactive contract mapping, and prioritised adoption in
three tiers (T1 safety net, T2 structure, T3 process).

### Is it tied to a specific AI provider?

No. The playbook is LLM-agnostic. §12 defines conventions that apply to any agent.
§12.7 adds an optional multi-agent coordination protocol for teams using more than
one LLM simultaneously. Provider-specific rules live in separate config files
(e.g. `CLAUDE.md`, `GEMINI.md`) that are not part of the playbook itself.

### What language is the playbook written in?

British English (en-GB). All documentation, commits, and contributions must follow
this convention.

---

## Design and inspirations

### What standards and methodologies influenced the playbook?

The playbook draws from established industry practices. The main influences, grouped
by area:

**Version control and release**

| Practice | Source | Used in |
|----------|--------|---------|
| Conventional Commits | [conventionalcommits.org](https://www.conventionalcommits.org/) | §3.3 — commit message format |
| Semantic Versioning (SemVer) | [semver.org](https://semver.org/) | D2.2 — library versioning, M3 cadence |
| Keep a Changelog | [keepachangelog.com](https://keepachangelog.com/) | §6.3 — changelog format |

**Security**

| Practice | Source | Used in |
|----------|--------|---------|
| OWASP Top 10 (Web, API, Mobile, LLM) | [owasp.org](https://owasp.org/) | M2.3 — security baseline |
| CVSS scoring | [first.org/cvss](https://www.first.org/cvss/) | M2.4 — dependency-vulnerability SLAs |
| SLSA provenance | [slsa.dev](https://slsa.dev/) | M3.3 — artefact signing and provenance |
| Sigstore / cosign | [sigstore.dev](https://sigstore.dev/) | M3.3 — keyless signing |
| NIST / CIS benchmarks | [nist.gov](https://www.nist.gov/) | §1.7, M2 — security landscape research |

**Architecture and documentation**

| Practice | Source | Used in |
|----------|--------|---------|
| Architecture Decision Records (ADR) | Michael Nygard's original proposal | §1.5 — decision documentation |
| OpenAPI / Swagger | [openapis.org](https://www.openapis.org/) | D1.1 — API documentation |
| C4 model (implied) | [c4model.com](https://c4model.com/) | §6 — layered documentation approach |

**Testing and quality**

| Practice | Source | Used in |
|----------|--------|---------|
| Testing pyramid (unit / integration / E2E) | Martin Fowler, Google Testing Blog | §5 — test strategy |
| Coverage ratchet (up-only baseline) | Industry practice (Google, Shopify) | §5.3 — coverage enforcement |
| DORA metrics (implied) | [dora.dev](https://dora.dev/) | §7 — CI/CD performance signals |

**Process and structure**

| Practice | Source | Used in |
|----------|--------|---------|
| Emergent Expansion (anti-scaffolding) | Original to Codex Machinae | §2.2 — trigger-based file creation |
| Boundary Contracts (4-axis taxonomy) | Inspired by contract testing (Pact) and DDD bounded contexts | §8 — integration-point catalogue |
| Risk-modulated remediation (L0/L1/L2) | Inspired by autonomous-vehicle levels and SRE practices | §10 — fix autonomy classification |
| MECE principle | McKinsey / structured problem-solving | M4 — taxonomy design |

### Is Emergent Expansion an established pattern?

No — it is original to Codex Machinae. It inverts the typical "scaffold first" approach:
no file, folder, or process exists until a defined trigger fires. This eliminates dead
scaffolding and ensures every artefact in the project earns its place.

### Why ADRs instead of design documents?

ADRs are lightweight, append-only, and version-controlled. They capture the **why**
behind a decision, including rejected alternatives. Traditional design documents tend
to grow stale; ADRs stay relevant because they are never edited — only superseded
by new ADRs that reference them (§1.5).

---

## Frameworks and taxonomies

### Where do I find information about classification frameworks?

Module M4 (Classification & Taxonomy) is framework-agnostic by design. It does not
ship a curated catalogue but defines the **protocol** for discovering, evaluating,
adopting, and maintaining domain-specific frameworks (M4.3 Scouting protocol).

The scouting protocol directs you to:

- **ISO/IEC standards bodies** — formal international standards.
- **OASIS** — open standards for security, IoT, and enterprise integration.
- **Domain-specific registries** — academic ontologies, government classifications,
  industry consortia.

### What are the illustrative framework examples in M4?

M4.7 provides a reference table of frameworks to show the *shape* of adoption.
These are examples, not defaults:

| Domain | Framework | Scope |
|--------|-----------|-------|
| Threat intelligence | MITRE ATT&CK | Adversary tactics, techniques, procedures |
| Threat intelligence | STIX / TAXII | Structured threat information exchange |
| Vulnerability | CAPEC | Common attack pattern enumeration |
| Vulnerability | CWE | Common weakness enumeration |
| Information sharing | TLP | Traffic Light Protocol for disclosure |
| Intelligence process | F3EAD | Find, Fix, Finish, Exploit, Analyse, Disseminate |
| Healthcare | SNOMED CT | Clinical terminology |
| Healthcare | ICD | International Classification of Diseases |
| Geospatial | ISO 19115 | Geographic metadata |

### How do I adopt an external framework?

Follow the adoption protocol in M4.4:

1. **Full adoption** — use the framework verbatim; its identifiers become yours.
2. **Partial adoption** — use a subset plus local extensions for domain-specific needs.
3. **Watch** — promising but immature; monitor without committing.

The decision is recorded in `docs/taxonomy/registry.md` with the scouting report
that justified the choice.

---

## Tooling

### Does the playbook include tools or scripts?

No. Codex Machinae is a design document. Appendix D contains **specifications**
(contracts) for three reference tools — AST Walker (D.1), Coverage Ratchet (D.2),
and Surveillance Agent (D.3) — but no implementations. Teams are free to build or
adopt tools that satisfy these contracts.

### What CLI frameworks does the playbook recommend?

D3.5 (Shell completion) mentions framework-native generation as the preferred
approach. Examples cited:

| Language | Framework |
|----------|-----------|
| Go | Cobra |
| Rust | Clap |
| Python | Click |
| Node.js | Commander, Yargs |

### What mobile frameworks are covered?

D6 is framework-agnostic. It covers native, cross-platform (Flutter, React Native,
.NET MAUI), and hybrid approaches. The rules apply regardless of the framework chosen.

### What static-site / frontend frameworks are mentioned?

D7 covers SPAs, SSG, and hybrid frameworks. Examples cited: Next.js (static export),
Astro, Nuxt, SvelteKit. The rules (bundle budgets, CDN, accessibility, Core Web
Vitals) are framework-independent.

---

## Contributing

### How do I report an error or suggest an improvement?

Open a [GitHub Issue](../../../issues). Include the section reference (e.g. §5.3,
M2.3, D1.4) and a clear description. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for
full guidelines.

### Can I contribute a new domain appendix?

Yes. Follow the Emergent Expansion principle: propose the trigger condition that
would activate the new appendix, then draft the content. Open a PR with a clear
description of what the appendix covers and why it is not already addressed by
existing appendices.
