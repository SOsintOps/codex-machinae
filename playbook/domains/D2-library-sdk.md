## D2 Library / SDK

**Activation trigger.** The project is published as a reusable package to a registry
(npm, PyPI, Maven Central, crates.io, NuGet, RubyGems, Packagist, Go modules, …) or consumed
directly via VCS reference as a library.

**In addition to Core.** Core §6 required documents, code docs, and CHANGELOG apply. This
appendix adds the patterns specific to published packages.

### D2.1 API documentation

Every public SDK surface (exported modules, classes, functions, types) MUST have
documentation generated from the code:

| Type | Recommended tool | Output |
|------|------------------|--------|
| TypeScript SDK | TypeDoc | `docs/api/` |
| Python SDK | Sphinx + autodoc | `docs/api/` |

API documentation is generated in CI and published alongside the package. Manually
written API documentation that diverges from the code is an announced bug.

### D2.2 Semantic versioning

Published libraries follow [Semantic Versioning 2.0.0](https://semver.org/) strictly:

| Bump | When | Example |
|------|------|---------|
| **Major** | Breaking change to the public API | Removing an exported function, changing a return type, renaming a parameter |
| **Minor** | Additive change — new functionality, no existing contract broken | New exported function, new optional parameter with a default |
| **Patch** | Bug fix or internal change — no public API change | Fix incorrect return value, performance improvement, dependency update |

**What counts as public API.** Every symbol that is exported from the package's entry
point(s) and reachable by a consumer without bypassing access controls. Internal modules
(prefixed with `_` in Python, not re-exported in TypeScript `index.ts`) are not public
API — but if a consumer can import them, they are de facto public until the package
enforces module boundaries.

**Pre-release versions.** Use SemVer pre-release identifiers for unstable releases:
`1.0.0-alpha.1`, `1.0.0-beta.3`, `1.0.0-rc.1`. Pre-release versions carry no
backwards-compatibility guarantee. The CHANGELOG (§6.3) must note when a pre-release
is promoted to stable.

### D2.3 Deprecation policy

Removing or changing a public API symbol requires a deprecation cycle:

1. **Annotate.** Mark the symbol as deprecated in the code using the language's standard
   mechanism (`@deprecated` JSDoc tag, `warnings.warn(DeprecationWarning)` in Python,
   `@Deprecated` annotation in Java/Kotlin). The annotation includes the replacement
   and the version in which the symbol will be removed.
2. **Document.** Record the deprecation in the CHANGELOG under a `Deprecated` section.
3. **Minimum window.** The deprecated symbol remains functional for at least **one minor
   release** after the deprecation is published. For widely-used libraries (> 1 000
   weekly downloads or equivalent), extend to **two minor releases**.
4. **Remove.** The symbol is removed in the next major release after the window expires.
   The removal is recorded in the CHANGELOG under `Removed`.

Deprecation warnings MUST be visible at runtime (log or stderr) so consumers discover
them during testing, not after a version bump breaks their code.

### D2.4 Breaking-change detection

CI includes an automated step that compares the current public API surface against the
last published version and fails the build if:

- A public symbol was removed or renamed on a minor or patch bump.
- A function signature changed in an incompatible way (parameter removed, type narrowed,
  return type changed) on a minor or patch bump.
- A type was widened in a way that could break consumer type-checks on a patch bump.

| Language | Recommended tool | Mechanism |
|----------|------------------|-----------|
| TypeScript | `api-extractor` (Microsoft) | Generates `.d.ts` rollup; diff against baseline |
| Python | `griffe` | Extracts API from source; reports breaking changes |
| Java/Kotlin | `japicmp` | Compares JAR bytecode against previous version |
| Rust | `cargo-semver-checks` | Lint against SemVer violations |

The baseline is the API snapshot of the last published version, committed as a CI
artefact (e.g. `api-report.md` for `api-extractor`). The snapshot is updated on every
release, not on every commit.

### D2.5 Package publishing

**Pre-publish checklist (automated in CI where possible):**

1. All tests pass across all tiers (§5.5).
2. Coverage has not dropped below baseline (§5.3).
3. CHANGELOG updated with a release entry (§6.3).
4. Version bumped in the package manifest (`package.json`, `pyproject.toml`, `Cargo.toml`,
   `pom.xml`).
5. API documentation regenerated (D2.1).
6. Breaking-change detection passed (D2.4).
7. Git tag created matching the version (`v1.2.3`).

**CI publish pipeline.** Publishing is triggered by a version tag, never by a manual
`npm publish` or `twine upload`. The pipeline:

1. Checks out the tagged commit.
2. Runs the full test suite.
3. Builds the distributable artefact (tarball, wheel, JAR, crate).
4. Publishes to the registry using credentials stored in CI secrets.
5. Creates a GitHub Release (or equivalent) with the CHANGELOG entry as the body.

**Registry-specific notes:**

| Registry | Key concern |
|----------|------------|
| npm | Use `prepublishOnly` script to enforce build + test before pack. Publish with `--provenance` for supply-chain attestation where supported |
| PyPI | Build with `build`, publish with `twine`. Use Trusted Publishers (OIDC) over long-lived API tokens |
| Maven Central | Sign artefacts with GPG. Use staging repositories for validation before promotion |
| crates.io | Run `cargo publish --dry-run` in CI before the real publish |

### D2.6 Multi-language coordination

When the same SDK ships in more than one language (e.g. TypeScript + Python client for
the same API):

1. **Version parity.** All language variants share the same major.minor version. Patch
   versions may diverge for language-specific fixes but must be documented in a shared
   CHANGELOG or a per-language CHANGELOG with cross-references.
2. **Feature matrix.** Maintain a table listing every public capability and its
   implementation status per language (`implemented`, `planned`, `not applicable`).
   The matrix lives in `docs/sdk-feature-matrix.md` or equivalent.
3. **Release coordination.** All language variants are released within the same sprint
   or release cycle. A feature available in one language but not another for more than
   one release cycle is a backlog item, not an accepted divergence.
4. **Contract sharing.** Where possible, generate client SDKs from a shared contract
   definition (OpenAPI spec, gRPC `.proto` files, GraphQL schema). Manual implementations
   across languages are a maintenance liability — prefer code generation with thin
   hand-written wrappers for ergonomics.

