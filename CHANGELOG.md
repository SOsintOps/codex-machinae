# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) — Versioning: [SemVer](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `AI-AGENTS.md`: shared source of truth for all AI agents working on the project.
- `templates/`: full project scaffold (8 files) in English (UK) — ready for new projects.
- `scripts/new-project.sh`: bootstrap script that creates a new project structure from templates.
- `GEMINI.md` (template): Gemini-specific agent rules with dogfooding principle and file structure enforcement.
- `.claude/agents/proofreader.yaml`: multilingual proofreading agent v1.0.0 — MQM-based 3-stage pipeline
  (detect → correct → verify), British English, confidence-score filtering, rollback rule, compatible with
  Claude Code subagent and Gemini CLI.
- `.gitignore`: excludes Ruflo/Claude Flow orchestration artefacts (`.swarm/`, `.claude-flow/`, `ruvector.db`)
  and local Claude settings.

### Changed
- `CLAUDE.md`: refactored to reference `AI-AGENTS.md`; Claude-specific rules only.
- `GEMINI.md`: refactored, translated to English (UK), aligned with `AI-AGENTS.md`; added Proofreader Agent
  invocation instructions and validation checklist.
- `software-development-playbook.md`: translated from Italian to English (UK) via 4-agent parallel swarm;
  QA verified by 4 further agents; 7 style corrections applied by MQM proofreader pipeline.
- `PROJECT_STATUS.md`: translated to English (UK), updated to reflect current state.
- `CHANGELOG.md`: translated to English (UK).
- `DEPENDENCIES.md`: translated to English (UK).

## [2.0.0-draft] - 2026-04-15

### Added
- `GEMINI.md` with operative mandates for the repository.
- Repository structure initialised per playbook (§2.1).
- `PROJECT_STATUS.md`, `CLAUDE.md`, `CHANGELOG.md`, `DEPENDENCIES.md` initialised.
- `software-development-playbook.md` loaded as the main playbook document.

### Changed
- Repository configured for management and maintenance on GitHub.
