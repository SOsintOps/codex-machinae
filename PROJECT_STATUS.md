# Project Status — dev_playbook

## Objective
Manage and evolve the universal software development playbook — the Single Source of Truth for development methodology, conventions, and tooling for LLM-assisted projects.

## Modified Files
- `AI-AGENTS.md`: Created as shared source of truth for all AI agents.
- `CLAUDE.md`: Refactored — now references `AI-AGENTS.md` for shared rules; Claude-specific rules only.
- `GEMINI.md`: Refactored — translated to English (UK) and aligned with `AI-AGENTS.md` structure.
- `templates/`: Created full scaffold (AI-AGENTS.md, CLAUDE.md, GEMINI.md, PROJECT_STATUS.md, DEPENDENCIES.md, CHANGELOG.md, COMPATIBILITY.md, docs/prd, docs/adr, docs/runbooks).
- `scripts/new-project.sh`: Created bootstrap script for new projects.

## Logical State
Repository structure is now in place. Multi-agent alignment protocol established via `AI-AGENTS.md`.
Remaining gap: `software-development-playbook.md` (1,347 lines) is still in Italian — needs translation.

## Next Action
Translate `software-development-playbook.md` to English (UK). Commit all current changes.
