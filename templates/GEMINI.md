# GEMINI.md — Gemini Agent Rules

> Agent-specific configuration for Gemini CLI (Google).
> **Shared rules are in `AI-AGENTS.md` — read that first. This file only adds Gemini-specific behaviour.**
> These instructions take precedence over any other default Gemini CLI configuration.

---

## Project Objective

<!-- One sentence: what this project does and for whom. -->
This repository acts as the **Single Source of Truth** for the team's development methodology on **{{PROJECT_NAME}}**.

---

## Core Mandates

### 1. Dogfooding (Cardinal Principle)

Gemini CLI MUST apply the rules defined in the project playbook to manage this very repository. Specifically:

- Keep `PROJECT_STATUS.md` up to date after every session.
- Use Conventional Commits for every change.
- Follow the Definition of Done for every update.
- Document significant architectural decisions as ADRs in `docs/adr/`.

### 2. GitHub Workflow

- **Issues:** Every non-trivial proposal must be preceded by a GitHub Issue to discuss its scope.
- **Pull Requests:** No change enters `main` without a PR.
- **Changelog:** Every significant change must be recorded in `CHANGELOG.md` following the Keep a Changelog standard.

### 3. Maintenance Rules

- **SOTA Research:** Before adopting emerging technologies, run a state-of-the-art research and document it in `docs/research/`.
- **Consistency:** Ensure cross-references between sections are always correct and up to date.
- **Style:** Maintain a professional, technical, and concise tone throughout all documentation.

### 4. File Structure Enforcement

The repository MUST strictly follow the structure defined in the project playbook (§2.1).
If any required directories or files are missing, Gemini CLI must flag them and create them as necessary.

---

## Suggested Workflow

1. **Analysis:** Read `PROJECT_STATUS.md` to understand the current context.
2. **Planning:** For complex changes, use plan mode to outline the strategy before acting.
3. **Execution:** Apply changes surgically; do not refactor beyond the task scope.
4. **Validation:** Verify Markdown correctness and the integrity of internal links.
5. **Wrap-up:** Update project status and prepare the commit.
