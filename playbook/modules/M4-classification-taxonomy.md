## M4 Classification & Taxonomy

**Activation trigger.** The project owns, extends, or depends on a domain-specific ontological
framework (threat intelligence, biomedical coding, geospatial metadata, fraud signalling,
vulnerability cataloguing, …). If the project invents its own terminology, this module
activates on the first naming decision.

**In addition to Core.** This module is framework-agnostic: it ships no curated catalogue of
taxonomies. Instead, it defines the principles, governance, and scouting protocol the project
follows to discover, adopt, and maintain whatever domain-specific frameworks its problem space
requires. Illustrative examples (MITRE ATT&CK, STIX, FT3, CAPEC, TLP, F3EAD, SNOMED, ICD,
ISO 19115) appear only to show the *shape* of adoption, never as defaults.

### M4.1 Design principles

**MECE (Mutually Exclusive, Collectively Exhaustive).** Every taxonomy the project owns or
adopts must partition its domain without overlap and without gaps. When a real-world entity
could belong to two categories, the taxonomy has an overlap bug; when an entity belongs to
none, the taxonomy has a coverage bug. Both are tracked as defects (§9, bucket `data-model`).

**Parsimony.** Introduce the fewest categories that explain the observed data. A taxonomy that
is too fine-grained creates classification paralysis; one that is too coarse loses
discriminating power. Start small, split only when a category demonstrably contains entities
that require different treatment.

**Stable identifiers.** Every term in the taxonomy has a machine-readable identifier that
never changes once assigned, even if the human-readable label is renamed. Format:
`<namespace>-<monotonic-number>` (e.g. `THREAT-042`). Deleted terms are tombstoned, never
recycled.

**Semantic versioning of the taxonomy.** The taxonomy itself has a version (semver):

| Change | Version bump | Migration required |
|--------|--------------|--------------------|
| Add a new term | Minor | No |
| Rename a label (ID unchanged) | Patch | No |
| Split or merge terms | Major | Yes — all classified records must be re-mapped |
| Remove (tombstone) a term | Major | Yes |

### M4.2 Governance

**Ownership.** Every taxonomy has a single owner (person or team). The owner approves
additions, merges, splits, and deprecations. In a solo-developer project, the developer is
the owner; the governance protocol still applies to maintain audit trail.

**Proposal protocol.** Any change to the taxonomy follows this flow:

1. **RFC.** A short document (issue, PR description, or `docs/taxonomy/rfc-NNN.md`) stating:
   what changes, why, which classified records are affected, migration plan if major.
2. **Review.** The owner reviews; the AI agent may review for MECE and parsimony violations.
3. **Decision.** Approve, reject, or request revision. Decision recorded in the RFC.
4. **Execution.** Merge the change, bump the taxonomy version, run the migration if major.

**Deprecation.** A term is deprecated before removal. Deprecated terms carry a `deprecated`
flag, a `successor` pointer (the term that replaces them), and a sunset date. During the
deprecation window, both the old and new term are accepted; after sunset, only the new term
is valid. Classification attempts using a deprecated term after sunset emit a warning (or
error, if the project configures it so).

### M4.3 Scouting protocol

**Binding to §1.7 SOTA Scout.** When M4 is active, the State-of-the-Art Scout (§1.7.5,
M1.1.2.6) gains an additional responsibility: for every domain the project touches, the
scout researches whether an established, community-maintained taxonomy or ontology already
exists.

**Scouting steps (executed per domain, on first encounter and then at the §1.7.5 cadence):**

1. **Survey.** Search for published standards, open-source frameworks, and academic ontologies
   that classify entities in the project's domain. Sources: ISO/IEC standards bodies, OASIS,
   W3C, IETF, domain-specific registries, peer-reviewed literature, GitHub/GitLab topic
   searches.
2. **Evaluate.** For each candidate, assess:
   - Coverage: does it cover the project's problem space?
   - Adoption: is it used by other projects in the same domain?
   - Maintenance: is it actively maintained? Last update date? Governance model?
   - Licence: compatible with the project's licence?
   - Machine-readability: available in a structured format (M4.6)?
3. **Recommend.** Produce a short report in `docs/research/` (§1.7.4 format) classifying each
   candidate as `adopt` (use as-is), `adapt` (use with local extensions), `watch` (promising
   but immature), or `ignore` (irrelevant or abandoned). The recommendation is non-binding —
   the human decides.
4. **Record.** The chosen framework (if any) is recorded in the project's taxonomy registry
   (`docs/taxonomy/registry.md` or equivalent) with: framework name, version adopted, scope
   of adoption (full or partial), local extensions, and the scouting report that justified
   the choice.

### M4.4 Adoption patterns

When the scouting protocol (M4.3) identifies a framework worth adopting, the project follows
one of three patterns:

**Full adoption.** The project uses the framework's taxonomy verbatim, without local
extensions. The framework's identifiers become the project's identifiers. Updates to the
framework are tracked by M1 Surveillance (if active) as an outbound contract.

**Partial adoption with local extensions.** The project adopts a subset of the framework and
adds local terms for concepts the framework does not cover. Local extensions use a distinct
namespace prefix (e.g. `LOCAL-`) so they are visually and programmatically distinguishable
from upstream terms. Local extensions follow the same governance (M4.2) as the rest of the
taxonomy.

**Inspiration only.** The project designs its own taxonomy, informed by the framework's
structure but not bound by its identifiers. The scouting report (M4.3) documents what was
borrowed and why the project diverged.

### M4.5 Audits

The taxonomy is audited periodically (suggested: quarterly, aligned with the §1.7.5 SOTA
Scout cadence). The audit checks:

| Check | Method | Failure threshold |
|-------|--------|-------------------|
| **Coverage** | Sample N records from the past quarter; classify each. Unclassifiable records = coverage gap | > 5% unclassifiable |
| **Ambiguity** | Two independent classifiers (human or AI) classify the same N records; measure inter-rater agreement (Cohen's κ or equivalent) | κ < 0.8 |
| **False positives** | Review records classified in the past quarter; count misclassifications | > 5% misclassified |
| **Drift** | Compare the distribution of classifications this quarter vs. last. A new cluster of records in a single category may signal a missing split | PSI > 0.2 on any category |
| **Staleness** | Check for terms with zero classifications in the past 6 months | Any stale term triggers a deprecation review |

Audit results are recorded in `docs/taxonomy/audit-YYYY-QN.md`. Failures trigger an RFC
(M4.2) for corrective action.

### M4.6 Machine-readable formats

Every taxonomy the project owns MUST have a machine-readable serialisation alongside the
human-readable documentation. Supported formats (choose at least one):

| Format | When to use |
|--------|-------------|
| JSON Schema | When the taxonomy is used for input validation or API contracts |
| JSON-LD / RDF | When the taxonomy participates in a linked-data ecosystem |
| OWL | When formal reasoning over the taxonomy is required |
| CSV / TSV | When the taxonomy is consumed by data pipelines or spreadsheets |
| Custom YAML | Acceptable for internal tooling; must be convertible to at least one of the above |

The machine-readable file is version-controlled alongside the taxonomy documentation. A CI
step validates that the human-readable and machine-readable representations are in sync (e.g.
every term in the Markdown table has a corresponding entry in the JSON Schema, and vice
versa).

### M4.7 Upstream contribution protocol

When a project's local extension (M4.4) proves broadly useful, the owner considers
contributing it back to the upstream framework. The protocol:

1. **Maturity gate.** The local term has been in use for at least two audit cycles (M4.5)
   with no MECE violations.
2. **Proposal.** Open an issue or RFC in the upstream framework's repository, following its
   contribution guidelines. Reference the project's usage data (classification count,
   coverage improvement).
3. **Tracking.** Record the proposal in `docs/taxonomy/upstream-contributions.md` with
   status (`proposed`, `accepted`, `rejected`, `withdrawn`).
4. **Adoption of upstream version.** If accepted, the project migrates from its local term
   to the upstream term (major version bump per M4.1). If rejected, the local term remains
   with a note explaining the divergence.

### M4.8 Illustrative examples

The following examples show the *shape* of taxonomy adoption across diverse domains. They are
not defaults — a project activates M4 because of its own domain, not because these examples
exist.

| Domain | Framework | What it classifies | Adoption shape |
|--------|-----------|-------------------|----------------|
| Threat intelligence | MITRE ATT&CK | Adversary tactics, techniques, procedures | Full or partial adoption; local techniques for niche attack surfaces |
| Threat intelligence | STIX / TAXII | Structured threat information exchange | Full adoption as a transport format |
| Fraud signalling | FT3 (Stripe) | Fraud tactics and techniques | Partial adoption; local extensions for domain-specific fraud vectors |
| Vulnerability | CVE / CWE / CAPEC | Vulnerabilities, weaknesses, attack patterns | Full adoption as identifiers; local severity overlay |
| Sharing policy | TLP (Traffic Light Protocol) | Information-sharing boundaries | Full adoption; no local extensions expected |
| Intelligence cycle | F3EAD | Find, Fix, Finish, Exploit, Analyse, Disseminate | Inspiration; adapted to the project's operational rhythm |
| Biomedicine | SNOMED CT / ICD | Clinical terms, diagnoses | Full or partial adoption; local extensions for research-specific phenotypes |
| Geospatial | ISO 19115 | Geographic metadata | Full adoption for metadata; local extensions for domain-specific layers |

---

