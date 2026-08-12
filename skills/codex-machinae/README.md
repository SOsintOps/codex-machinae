# codex-machinae — the playbook as an agent skill

This directory packages [Codex Machinae](../../README.md) as an agent skill:
a condensed, trigger-routed entry point plus the full playbook as disclosed
reference, so an agent session carries only what its triggers actually fire.

## Install

| Route | Command / location |
|---|---|
| **Subscribe** — Claude Code plugin (read-only, always current) | `claude plugin marketplace add SOsintOps/codex-machinae` then `claude plugin install codex-machinae@codex-machinae` |
| **Fork** — editable copy, any Agent-Skills harness | `npx skills add SOsintOps/codex-machinae` |
| Manual — this repo only | copy to `.claude/skills/codex-machinae/` |
| Manual — all your projects | copy to `~/.claude/skills/codex-machinae/` |

The skill is **model-invoked**: the agent activates it on its own when a
lifecycle event matches the description (new project, retrofit, dependency or
contract break, release, multi-agent coordination). You can also invoke it by
name.

## Layout

- [`SKILL.md`](SKILL.md) — hand-authored entry point: operating rules,
  route-by-situation table, condensed lifecycle, remediation ladder, trigger
  tables, reference index.
- [`reference/`](reference/) — **generated** byte-for-byte from the
  repository's [`playbook/`](../../playbook/) sources by
  [`tools/build.py`](../../tools/build.py). Edit the sources and rebuild;
  never edit these copies. `python tools/build.py --check` verifies sync.

## Companion skill

[`../setup-codex-machinae/`](../setup-codex-machinae/) seeds the per-repo
configuration this skill consumes (profile, tracker, autonomy posture,
module activation). Install both; run `/setup-codex-machinae` once per
repository.

## Licence

CC BY 4.0 — attribution: *"Codex Machinae —
https://github.com/SOsintOps/codex-machinae"*.
