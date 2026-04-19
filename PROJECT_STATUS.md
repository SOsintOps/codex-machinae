# Project Status — Codex Machinae

## Objective
Evolve `codex-machinae.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` (Cortex project) and promoting them into the playbook.

All documentation and commits are in **British English**.

## Current Phase
Project-size profiles added. §2.5 defines Solo/Small/Large profiles that modulate
checklist obligation levels in Appendix A. All three Known Limitations now have
concrete mitigations in place.

## Modified Files (cumulative, current state)
- `codex-machinae.md`: Core + Modules + Domains + Phase C hardening + Phase R (§11.6) +
  Multi-agent (§12.7) + Tooling specs (Appendix D) + Project-size profiles (§2.5).
- `gemini_revision_260419.md`: Comprehensive senior analyst review + strategic synthesis.
- `MODULARISATION_PLAN.md`: All phases (0–10) closed.
- `README.md`: Minimal redesign (stable design badge).
- `LICENSE`: CC BY 4.0.
- `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: Agent configuration sync.

## Logical State
- Playbook structure: Stable, modular, retrofit-capable, multi-agent-ready,
  tooling-specified, profile-aware.
- All three Known Limitations now mitigated: mechanical barrier (Appendix D),
  incomplete domains (planned D2/D3 priority), checklist density (§2.5 profiles).
- Reference example: `example/00-prd.md` (Cortex) — unchanged; quality benchmark.

## Recent Changelog
- **§2.5 Project-size profile** — Solo/Small/Large declaration that modulates Appendix A
  items as mandatory/recommended/optional. Conservative tagging: most items stay
  mandatory; only ceremony-heavy items are downgraded for smaller profiles.
- **Appendix A tagged** — items in A.1–A.5 carry inline profile tags where applicable.
- **Known Limitations updated** — checklist density mitigation now points to §2.5.
- **Glossary** — one new entry: Project-size profile.
- *(Previous: Appendix D tooling specs; §12.7 multi-agent; §11.6 Phase R.)*

## Next Action
All items from the post-modularisation roadmap are now addressed:
- Phase R (Retrofit) — §11.6 ✓
- Multi-Agent Protocol — §12.7 ✓
- Tooling Specifications — Appendix D ✓
- Project-size Profiles — §2.5 ✓

Remaining work:
1. **Fill remaining stubs** — prioritise D2 (Library/SDK) and D3 (CLI Tool).
2. **Build reference implementations** against Appendix D specifications.
3. **First downstream retrofit** — apply the playbook to an existing project to validate
   Phase R and the tooling specs in practice.
