## M3 Release & Distribution

**Activation trigger.** The project ships versioned artefacts to external consumers
(applies whenever D2, D3, D4, or D6 is active; may also apply to D1 when artefacts are
published to an internal registry).

**In addition to Core.** This module defines the universal release process that applies
across all domains. Domain appendices (D2.5 Package publishing, D3.6 Installation and
distribution, D4.4 Flash and OTA) add domain-specific details; M3 owns the cross-cutting
patterns that bind them together.

### M3.1 Release cadence

The project declares its release model in the agent configuration file (§2.4):

| Model | Description | When to use |
|-------|-------------|-------------|
| **Release-when-ready** | A release is cut whenever a meaningful set of changes is merged | Small teams, libraries, CLI tools with rapid iteration |
| **Release train** | Releases happen on a fixed schedule (e.g. every two weeks) regardless of content | Larger teams, products with external stakeholders expecting predictable delivery |
| **Event-driven** | Releases are tied to external events (hardware rev, conference, regulatory deadline) | Embedded/firmware, regulated industries |

**Freeze windows.** When the project adopts a release train, the last 20% of the cycle
is a freeze window: only bug fixes and documentation enter the release branch. New
features merge to the development branch and ride the next train.

**Multi-artefact coordination.** When a single project produces more than one artefact
(e.g. a backend service + a client SDK + a CLI), all artefacts follow the same release
cadence. Version numbers may differ (each artefact has its own SemVer), but releases are
cut in the same cycle. The release-coordination checklist lives in `docs/release-matrix.md`
or equivalent.

### M3.2 Changelog automation

The CHANGELOG (§6.3) is generated from Conventional Commits (§3.3) and refined by a
human editor before publication:

**Step 1 — Generate.** A CI step produces a draft CHANGELOG entry from commit messages
since the last release tag. Commits are grouped by type (`feat`, `fix`, `refactor`,
`docs`, `chore`) and filtered: `chore` commits are excluded from the public CHANGELOG
unless they affect consumer-visible behaviour.

**Step 2 — Edit.** A human (or lead agent with human approval) edits the draft to:

- Rewrite terse commit messages into consumer-facing language.
- Merge related entries (e.g. three `fix` commits for the same bug become one entry).
- Add a summary paragraph at the top for major releases.
- Flag breaking changes prominently at the start of the entry.

**Step 3 — Publish.** The final CHANGELOG entry is committed alongside the version bump.
The same text is used as the body of the GitHub Release (or equivalent platform release).

**Format.** Follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) with sections:
`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

### M3.3 Artefact signing and provenance

Every release artefact is accompanied by a verification mechanism appropriate to the
project's risk profile:

| Level | Mechanism | When required |
|-------|-----------|---------------|
| **Minimum** | SHA-256 checksum file published alongside artefacts | Always |
| **Standard** | GPG signature or Sigstore/cosign signature on each artefact | When M2 Security-sensitive is active, or when the artefact is distributed to untrusted channels |
| **Provenance** | SLSA Level 2+ provenance attestation (build platform, source commit, builder identity) | Regulated environments, supply-chain-critical libraries |

**Supply-chain attestation.** Where the registry supports it, use platform-native
provenance mechanisms:

- npm: `--provenance` flag (OIDC-based, ties the package to a specific CI build).
- PyPI: Trusted Publishers (OIDC from GitHub Actions, GitLab CI).
- Container images: `cosign` attestation attached to the image manifest.
- Go modules: `go.sum` provides content-based integrity; SLSA provenance adds builder
  attestation.

Signing keys or OIDC trust policies are documented in the project's `SECURITY.md` or
equivalent. Key rotation follows the schedule defined when M2 is active.

### M3.4 Release-notes protocol

Every release includes a release note structured for two audiences:

**Developer-facing** (in the CHANGELOG and GitHub Release body):

```
## [version] — YYYY-MM-DD

### Breaking changes
- [description + migration guide]

### Added
- [new feature]

### Fixed
- [bug fix]

### Deprecated
- [symbol, with replacement and removal version]
```

**End-user-facing** (when the project has non-developer consumers — e.g. a desktop app,
a CLI with a broad audience, a firmware update):

- One paragraph summarising what changed in plain language.
- A "What you need to do" section if the update requires action (migration, config
  change, hardware reset).
- Known issues, if any.

The developer-facing note is always produced. The end-user-facing note is produced when
the domain appendix requires it (D3 CLI, D4 Embedded, D6 Mobile) or when the analyst
judges it necessary.

### M3.5 Rollback of a published release

When a published release contains a critical defect:

| Step | Action |
|------|--------|
| **1. Assess** | Determine severity: data loss, security vulnerability, or functional regression. If security, follow M2 response SLA (M2.4) |
| **2. Decide** | Yank/unpublish the broken version, or publish a patch release. Prefer patch release when possible — yanking breaks consumers who pinned the version |
| **3. Yank (if necessary)** | Use the registry's yank mechanism (`npm deprecate`, `cargo yank`, PyPI yank). Do not delete — yank marks the version as unsuitable while preserving it for pinned consumers |
| **4. Patch** | Publish a new patch version with the fix. The CHANGELOG entry for the patch references the broken version explicitly |
| **5. Communicate** | Post a GitHub Advisory (if security), update the CHANGELOG, and notify consumers through the project's communication channel (GitHub Discussions, mailing list, Discord) |
| **6. Retrospective** | Record what allowed the defect to ship (missing test, insufficient review, CI gap) and add a mitigation to the release checklist |

A rollback is never silent. Every yanked or patched version is documented in the
CHANGELOG and in the GitHub Releases page.

