# GEMINI.md — Gemini Agent Rules

> Agent-specific configuration for Gemini CLI (Google).
> **Shared rules are in `AI-AGENTS.md` — read that first. This file only adds Gemini-specific behaviour.**
> These instructions take precedence over any other default Gemini CLI configuration.

---

## Project Objective

Manage, maintain, and evolve the universal software development framework with the support of LLMs and autonomous agents.
This repository acts as the **Single Source of Truth** for the team's development methodology.

---

## Core Mandates

### 1. Dogfooding (Cardinal Principle)

Gemini CLI MUST apply the rules defined in `software-development-playbook.md` to manage this very repository. Specifically:

- Keep `PROJECT_STATUS.md` up to date after every session (§2.2).
- Use Conventional Commits for every change (§3.3).
- Follow the Definition of Done for every playbook update (§1.8).
- Document significant architectural decisions as ADRs in `docs/adr/` (§1.5).

### 2. GitHub Workflow

- **Issues:** Every proposal for a change or new section must be preceded by a GitHub Issue to discuss its scope.
- **Pull Requests:** No change enters `main` without a PR. PRs must be classified according to the buckets defined in the playbook (§10.1): `safe`, `additive`, `breaking`, `p0`.
- **Changelog:** Every release or significant change must be recorded in `CHANGELOG.md` following the Keep a Changelog standard (§6.4).

### 3. Playbook Maintenance

- **SOTA Research:** Before adding new sections on emerging technologies (e.g. new agentic frameworks), run a state-of-the-art research and document it in `docs/research/` (§1.7).
- **Consistency:** Ensure cross-references between sections (e.g. §9 citing §1.7.5) are always correct and up to date.
- **Style:** Maintain the professional, technical, and concise tone of the original document.

### 4. File Structure Enforcement

The repository MUST strictly follow the structure defined in §2.1 of the playbook.
If any required directories or files are missing, Gemini CLI must flag them and create them as necessary.

---

## Suggested Workflow

1. **Analysis:** Read `PROJECT_STATUS.md` to understand the current context.
2. **Planning:** For complex changes, use plan mode to outline the strategy before acting.
3. **Execution:** Apply changes surgically; do not refactor beyond the task scope.
4. **Validation:** Verify Markdown correctness and the integrity of internal links.
5. **Wrap-up:** Update project status and prepare the commit.

---

## Proofreader Agent

A multilingual proofreading agent is available at `.claude/agents/proofreader.yaml`.

**Purpose:** translation quality assurance and style-guide-aware proofreading for
documentation. Uses a 3-stage MQM pipeline: detect → correct → verify.

**To invoke on a file:**

```
# Proofread with default settings (British English, source auto-detected)
gemini run .claude/agents/proofreader.yaml --file software-development-playbook.md

# Explicit source language and minor-issue auto-fix
gemini run .claude/agents/proofreader.yaml --file software-development-playbook.md \
  --style en-GB --source it --auto-fix-minor
```

**Key behaviours to verify:**
- MQM report is produced before any correction (stage 1 output)
- Code blocks, URLs, technical terms (PRD, ADR, JWT), and §-references are never altered
- Markdown structure is preserved exactly after correction
- Summary table lists critical / major / minor counts and verification status

**Validation checklist for Gemini CLI:**
- [ ] Load `.claude/agents/proofreader.yaml` and confirm schema is valid YAML
- [ ] Confirm `guardrails.never_alter_code_blocks` is `true`
- [ ] Confirm `style_variant` defaults to `en-GB`
- [ ] Confirm pipeline has exactly 3 stages in order: detect, correct, verify
- [ ] Confirm `supported_languages` includes the `it → en-GB` pair
- [ ] Run a dry-run on `software-development-playbook.md` and verify the MQM report
  JSON structure matches `[{line, text, error_type, severity, suggestion}]`
