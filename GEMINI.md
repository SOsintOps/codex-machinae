# GEMINI.md — Gemini Agent Rules

> Agent-specific configuration for Gemini CLI (Google).
> **Shared rules are in `AI-AGENTS.md` — read that first. This file only adds Gemini-specific behaviour.**
> These instructions take precedence over any other default Gemini CLI configuration.

---

## Project Objective

Evolve `software-development-playbook.md` into a universal Meta-Framework for LLM-assisted software development, extracting general patterns from `example/00-prd.md` and promoting them into the playbook.

**Working Language:** British English for all documentation, commits, and agent outputs.

---

## Core Mandates

### 1. Dogfooding

Gemini CLI MUST apply the conventions defined in `software-development-playbook.md` to manage this very repository — to the extent those conventions are still valid under the current Meta-Framework direction (see `STRATEGY_TRANSFORMATION.md`). Specifically:

- Keep `PROJECT_STATUS.md` up to date after every session.
- Use Conventional Commits for every change.

### 2. Scope Discipline

- This repository is in the **design phase**. Only `software-development-playbook.md`, `example/00-prd.md`, and the agent configs are in scope.
- Do **not** reintroduce templates, bootstrap scripts, CI workflows, or release automation. Those are explicitly deferred until the playbook design stabilises.
- Do **not** create folders like `docs/adr/`, `docs/prd/`, `docs/research/`, `src/`, `tests/`, etc. in this repo. They belong to generated projects, not to the playbook repo itself.

### 3. Playbook Maintenance

- **Consistency:** Ensure cross-references between sections (e.g. §9 citing §1.7.5) remain correct as the playbook is refactored.
- **Style:** Maintain the professional, technical, and concise tone of the document.
- **Promotion rule:** When a pattern in `example/00-prd.md` is general enough, abstract it and promote it into the playbook; do not modify the example itself.

---

## Suggested Workflow

1. **Analysis:** Read `PROJECT_STATUS.md` to understand the current context.
2. **Planning:** For non-trivial changes, outline the strategy before acting.
3. **Execution:** Apply changes surgically; do not refactor beyond the task scope.
4. **Validation:** Verify Markdown correctness and internal link integrity.
5. **Wrap-up:** Update `PROJECT_STATUS.md` and prepare a Conventional Commit.
