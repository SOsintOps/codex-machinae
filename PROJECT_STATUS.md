# Project Status — Codex Machinae

## Objective
Evolve `codex-machinae.md` into a universal Meta-Framework for LLM-assisted software development.

All documentation and commits are in **British English**.

## Current Phase
All domain appendices (D1–D7) and all cross-cutting modules (M1–M4) fully populated.
No stubs remain. The playbook design is complete.

## Modified Files (cumulative, current state)
- `codex-machinae.md`: Core + Modules + Domains + Phase C hardening + Phase R (§11.6) +
  Multi-agent (§12.7) + Tooling specs (Appendix D) + Project-size profiles (§2.5).
- `MODULARISATION_PLAN.md`: All phases (0–10) closed.
- `README.md`: Minimal redesign (stable design badge).
- `LICENSE`: CC BY 4.0.
- `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: Agent configuration sync.

## Logical State
- Playbook structure: Stable, modular, retrofit-capable, multi-agent-ready,
  tooling-specified, profile-aware.
- All three Known Limitations now mitigated: mechanical barrier (Appendix D),
  incomplete domains (planned D2/D3 priority), checklist density (§2.5 profiles).

## Recent Changelog
- **Repository restructure** — service documents moved to `docs/` per §2.1:
  `CHANGELOG.md`, `CONTRIBUTING.md`, `MODULARISATION_PLAN.md`. New `docs/SECURITY.md`.
- **Gemini revision** — removed from tracking, kept locally via `.gitignore`.
- **Agent configs** — `AI-AGENTS.md`, `CLAUDE.md`, `GEMINI.md` excluded from version
  control (local only).
- *(Previous: D6 full content; D7 full content; M3 full content; D2/D3 full content;
  §2.5 profiles; Appendix D tooling specs; §12.7 multi-agent; §11.6 Phase R.)*

## Next Action
1. **First downstream retrofit** — apply the playbook to an existing project to validate
   Phase R and the tooling specs in practice.
2. **Build reference implementations** against Appendix D specifications.
