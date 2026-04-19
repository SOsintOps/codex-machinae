# Contributing to Codex Machinae

Thank you for your interest in contributing to Codex Machinae. This document explains
how to contribute effectively.

---

## What this project is

Codex Machinae is a **design document** — a meta-framework specification for
LLM-assisted software development. It is not a software application. Contributions
are textual: improvements to the playbook's rules, new domain appendices, new modules,
or refinements to existing content.

## Language

All contributions must be in **British English** (en-GB). This includes documentation,
commit messages, comments, and PR descriptions.

## How to contribute

### Reporting issues

Open a [GitHub Issue](../../issues) for:

- **Errors** — incorrect cross-references, broken numbering, factual mistakes.
- **Gaps** — missing coverage for a scenario the playbook should address.
- **Suggestions** — improvements to existing rules or new content proposals.

Please include the relevant section reference (e.g. "§5.3 coverage ratchet") and
describe the problem or suggestion clearly.

### Proposing changes

1. **Fork** the repository.
2. **Create a branch** following the naming convention: `<type>/<description>`
   (e.g. `feat/d2-library-sdk`, `fix/xref-section-8`).
3. **Make your changes** in `codex-machinae.md` or the relevant file.
4. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/)
   (e.g. `feat(playbook): add D2 Library/SDK domain appendix`).
5. **Open a Pull Request** with a clear description of what changed and why.

### Content guidelines

- **Maximum line length:** 120 characters.
- **Cross-references:** use the `§X.Y` format for Core sections, `MX.Y` for modules,
  `DX.Y` for domain appendices. Every reference must resolve to an existing heading.
- **No scaffolding:** do not add templates, scripts, CI pipelines, or folder structures
  unless the playbook design explicitly calls for them.
- **Emergent Expansion:** new content must have a clear activation trigger (§2.2).
  Nothing is mandatory until the trigger fires.

### Filling domain stubs

The following domain appendices are stubs awaiting full content:

- **D2 Library / SDK** — published packages, semver, API surface management.
- **D3 CLI Tool** — argument parsing, man pages, shell completion.
- **D6 Mobile App** — app stores, device fragmentation, offline-first.
- **D7 Static Site / Frontend-only** — build pipelines, CDN, hydration.
- **M3 Release & Distribution** — release trains, changelogs, artefact signing.

If you have expertise in any of these domains, your contribution is especially welcome.
Follow the structure of existing full appendices (D1, D4, D5) as a model.

## Code of conduct

Be respectful, constructive, and focused on improving the playbook. This is a
collaborative project — assume good faith.

## Licence

By contributing, you agree that your contributions will be licensed under the
[CC BY 4.0 Licence](https://creativecommons.org/licenses/by/4.0/), the same licence
as the rest of the project.
