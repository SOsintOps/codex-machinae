---
name: setup-codex-machinae
description: Configure a repository for the Codex Machinae playbook — project-size profile, issue tracker, autonomy posture, module activation.
disable-model-invocation: true
---

# Setup — Codex Machinae

Seeds the per-repo configuration the playbook's skill depends on. Run once
per repository, and again whenever the posture changes. The sibling
`codex-machinae` skill consumes what this writes; without it, tracker-bound
work (decision maps, tracking issues) has nowhere to publish and
profile-aware checklists cannot be graded.

## What it seeds

| Key | Consumed by |
|---|---|
| Project-size profile (Solo / Small / Large) | Every checklist obligation (§2.5, Appendix A) |
| Issue-tracker binding | Decision maps (§1.9), tracking epics and deprecation watches (§10), retrofit audit issues (§11.6) |
| Autonomy posture (L0/L1 enablement) | The remediation ladder (§10.1) and its preconditions |
| Never-auto-merge additions | Classification guardrails (§9.3) |
| Active domains and modules | Which reference files sessions load (§2.2, §11.6.4) |

## Steps

1. **Locate the agent-configuration file** (§2.4): `CLAUDE.md`,
   `AGENTS.md`, `AI-AGENTS.md`, or the harness's equivalent, at the repo
   root. If none exists, creating one is part of this setup. If a
   `## Codex Machinae configuration` block already exists, switch to
   **update mode**: show the current values and change only what the human
   asks changed.

2. **Gather the facts yourself** — never ask the human for anything the
   environment can answer. Read: git remotes (GitHub? GitLab? none?),
   whether code and history already exist (greenfield vs retrofit),
   CI configuration, package manifests that imply publishing, source-tree
   hints of domains (mobile project files, firmware toolchains, ML
   pipelines) and modules (auth code, payment SDKs, release tooling).

3. **Put the decisions to the human, one question per round, each with a
   recommended answer** grounded in the facts from step 2:
   - **Profile** — Solo, Small, or Large (§2.5). Recommend from team size
     and repo history.
   - **Tracker** — `github` | `gitlab` | `local` (markdown fallback:
     decision maps at `docs/decisions/MAP.md`, tickets as sibling files).
     Recommend the forge the remote already points at.
   - **Autonomy posture** — default is everything L2; enable L1 only when
     CI, the correctness gate, and regression tests exist (§10.1); enable
     L0 only on top of L1 for `safe`-classified changes. Recommend the
     highest level the repo's machinery actually supports, not more.
   - **Never-auto-merge additions** — paths or patterns beyond the §9.3
     defaults (deploy config, migrations, secrets-adjacent files).

4. **Retrofit only** (the repo has pre-existing code): walk the trigger
   lists of D1–D7 and M1–M4 against the codebase (§11.6.4) and propose each
   activation in the §2.2 form — *"I suggest activating `<D/M>` because
   `<trigger evidence>`. Cost of omission: `<what goes unwatched>`"* — one
   proposal per round, accepted, rejected, or deferred.

5. **Write the block, with approval.** The agent-configuration file is
   **human-only** (§12.7.4): compose the full block (template below), show
   it, and write it **only after the human explicitly approves**. Never
   overwrite unrelated content in the file.

6. **Verify and report.** Re-read the file, confirm the block parses,
   then report: what is configured, which lifecycle entry point applies
   (Phase 0 for greenfield, Phase R for retrofit — the main skill takes it
   from here), and whether the `codex-machinae` skill itself is installed
   (if not, say where to copy it from).

## Config block template

```markdown
## Codex Machinae configuration

<!-- Seeded by setup-codex-machinae on YYYY-MM-DD. Human-only file (§12.7.4). -->

- **Profile:** Solo | Small | Large (§2.5)
- **Tracker:** github | gitlab | local — decision maps (§1.9) and tracking
  issues (§10) publish here
- **Autonomy:** L0: off | on (classes: …) · L1: off | on · everything else L2 (§10.1)
- **Never-auto-merge additions:** <paths/patterns, or "none"> (§9.3)
- **Active domains:** <D1…D7, or "none yet">
- **Active modules:** <M1…M4, or "none yet">
- **Playbook source:** skill | playbook/ directory | codex-machinae.md monolith
```

## Done when

Every key in the block holds a value the human chose (none defaulted
silently), the block is written into the agent-configuration file with the
human's approval, and the closing report names the lifecycle entry point.
The one legitimate partial outcome: the human defers a decision — record
the key as `deferred: <reason>` rather than inventing a value.

---

*Part of [Codex Machinae](https://github.com/SOsintOps/codex-machinae),
CC BY 4.0.*
