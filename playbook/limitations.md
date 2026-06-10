## Known limitations and roadmap

This section records structural limitations identified during the post-modularisation review
(April 2026) and the planned mitigations. It is a living section: entries are removed when
the limitation is resolved, not when work begins.

### Mechanical barrier to adoption

Many Core processes (coverage ratchet, contract-map generation, surveillance agents) assume
CI/CD tooling and automation infrastructure that a new adopter does not have on day one.
Without reference implementations, the compliance cost is high.

**Mitigation — Tooling specifications (Appendix D).** The playbook now defines the
contracts that reference implementations must satisfy for three tools:
- **D.1 AST Walker** — contract-map generator (§8 automation).
- **D.2 Coverage Ratchet** — CI step enforcing §5.3.
- **D.3 Surveillance Agent Scaffold** — M1.1 implementation.

Implementations are built in dedicated repositories and validated against Appendix D.

### ~~Incomplete domain coverage~~ — Resolved

All seven domain appendices (D1–D7) and all four cross-cutting modules (M1–M4) are
fully populated. No stubs remain.

### Checklist density

Appendix A is comprehensive but dense. For small projects, unfiltered application of the full
checklist can slow velocity disproportionately.

**Mitigation — Project-size profiles (§2.5).** The project declares a size profile (Solo,
Small, Large) that modulates checklist items as mandatory, recommended, or optional.
Checklist items in Appendix A are tagged inline where the profile changes their obligation
level. Untagged items remain mandatory for all profiles.

---

