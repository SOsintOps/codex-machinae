# Dependencies

Questo repository contiene documentazione e regole operative (playbook). Le sue "dipendenze" sono principalmente gli agenti che lo interpretano.

## Critical Dependencies

### Gemini CLI
- **Type:** LLM-based autonomous agent
- **Role:** Primary management and maintenance agent.
- **Contract:** Interprets `GEMINI.md` and `CLAUDE.md`.
- **Last verified:** 2026-04-15

### GitHub Actions
- **Type:** CI/CD Platform
- **Role:** Automation of PR checks, linting, and release management.
- **Contract:** Workflows in `.github/workflows/`.
- **Last verified:** 2026-04-15

## Development Dependencies

### Prettier / Markdownlint
- **Purpose:** Mantieni la consistenza del formato Markdown.
- **Version:** Latest
- **Pinned:** No
