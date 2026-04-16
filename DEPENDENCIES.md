# Dependencies — dev_playbook

This repository contains documentation and operative rules (a playbook). Its "dependencies" are primarily the agents that interpret it and the tooling that enforces its conventions.

## Critical Dependencies

### Claude (Anthropic)
- **Type:** LLM-based autonomous agent
- **Role:** Primary development and maintenance agent.
- **Contract:** Interprets `AI-AGENTS.md` and `CLAUDE.md`.
- **Last verified:** 2026-04-16

### Gemini CLI (Google)
- **Type:** LLM-based autonomous agent
- **Role:** Secondary management and maintenance agent.
- **Contract:** Interprets `AI-AGENTS.md` and `GEMINI.md`.
- **Last verified:** 2026-04-15

### GitHub Actions
- **Type:** CI/CD Platform
- **Role:** Automation of PR checks, linting, and release management.
- **Contract:** Workflows in `.github/workflows/`.
- **Last verified:** 2026-04-15

## Development Dependencies

### Prettier / Markdownlint
- **Purpose:** Enforce consistent Markdown formatting across the playbook.
- **Version:** Latest
- **Pinned:** No

## Notes
- No runtime dependencies — this is a meta-documentation project.
- Agent contracts (CLAUDE.md, GEMINI.md) derive from `AI-AGENTS.md` as the single source of truth.
