## D3 CLI Tool

**Activation trigger.** The project's primary interface is a command-line executable invoked
by humans or by scripts.

**In addition to Core.** Core §6 required documents, code docs, and CHANGELOG apply. This
appendix adds the patterns specific to command-line interfaces.

### D3.1 CLI documentation

The CLI's contract surface (flags, subcommands, exit codes, output modes) MUST be
documented and kept in sync with the code:

| Type | Recommended tool | Output |
|------|------------------|--------|
| CLI | `--help` + generated man page | `docs/cli/` |

Documentation is generated from the code (help strings, argument metadata) in CI.
Manually written documentation that diverges from `--help` is an announced bug.

### D3.2 Argument and subcommand design

CLI interfaces follow POSIX and GNU conventions unless the target platform has a
dominant alternative (e.g. PowerShell verb-noun on Windows):

| Rule | Example |
|------|---------|
| Short flags are single dash + single letter | `-v`, `-f` |
| Long flags are double dash + kebab-case word | `--verbose`, `--output-format` |
| Boolean flags do not take a value | `--dry-run` (not `--dry-run=true`) |
| Value flags use `=` or space | `--output=json` or `--output json` |
| `--` terminates flag parsing | `mytool -- -not-a-flag` |
| Subcommands precede flags | `mytool deploy --env staging` |
| No ambiguity between positional args and flags | Positional args come after all flags, or are unambiguous by position |

**Help hierarchy.** Every level of the command tree has a `--help` output:

- `mytool --help` — lists subcommands and global flags.
- `mytool <subcommand> --help` — lists subcommand-specific flags and arguments.

Help text includes at least: one-line description, usage synopsis, flag table with
defaults, and one example invocation.

**Global flags.** The following flags are reserved across all subcommands:

| Flag | Short | Meaning |
|------|-------|---------|
| `--help` | `-h` | Show help and exit |
| `--version` | `-V` | Show version and exit |
| `--verbose` | `-v` | Increase output verbosity (stackable: `-vvv`) |
| `--quiet` | `-q` | Suppress non-error output |

### D3.3 Exit-code contracts

Every CLI tool defines and documents a set of exit codes. The minimum set:

| Code | Meaning | When |
|------|---------|------|
| `0` | Success | The command completed its intended operation |
| `1` | User error | Invalid input, missing required argument, file not found |
| `2` | Internal error | Unexpected failure, unhandled exception, bug |

Domain-specific codes (`3`–`125`) are permitted but must be documented in the help text
and in `docs/cli/exit-codes.md`. Codes `126`–`255` are reserved by the shell and must
not be used.

**Testing.** Every documented exit code has at least one test that triggers it and
asserts on the exact code. Exit-code tests are part of the integration tier (§5).

### D3.4 Machine-readable output

Every command that produces structured output supports at least one machine-readable
format alongside the human-readable default:

| Flag | Format | When to use |
|------|--------|-------------|
| `--json` | JSON (one object or array per invocation) | Scripting, piping to `jq`, programmatic consumption |
| `--csv` | CSV with header row | Tabular data, spreadsheet import |

**Rules:**

1. Human-readable output is the default. Machine-readable is opt-in via flag.
2. The JSON schema is stable within a major version. Breaking changes follow D2.2
   SemVer rules (machine-readable output is public API).
3. JSON output goes to stdout. Errors and warnings go to stderr regardless of output
   mode, so piping works correctly: `mytool list --json | jq '.[] | .name'`.
4. When `--json` is active, the exit code still reflects success/failure — the caller
   should not need to parse JSON to detect errors.

### D3.5 Shell completion

The CLI ships or generates completion scripts for at least two shells:

| Shell | Generation mechanism | Installation |
|-------|---------------------|-------------|
| Bash | `mytool completion bash` | Source in `.bashrc` or install to `/etc/bash_completion.d/` |
| Zsh | `mytool completion zsh` | Install to `$fpath` or source in `.zshrc` |
| Fish | `mytool completion fish` (optional) | Install to `~/.config/fish/completions/` |

Completion covers subcommands, flags (including value suggestions where feasible), and
file-path arguments. Completion scripts are regenerated in CI when the command tree
changes and included in the release artefact.

Most CLI frameworks generate completions automatically (Cobra for Go, Clap for Rust,
Click for Python, Commander/Yargs for Node.js). Prefer framework-native generation
over hand-written scripts.

### D3.6 Installation and distribution

The CLI is distributed through multiple channels appropriate to the target audience:

| Channel | When to support | Artefact |
|---------|----------------|----------|
| **Standalone binary** | Always (if compiled language) | Pre-built binaries per OS/arch in GitHub Releases |
| **Homebrew** | macOS/Linux audience | Tap formula or core formula |
| **apt / deb** | Debian/Ubuntu server audience | `.deb` package |
| **Scoop / Chocolatey** | Windows audience | Manifest in a bucket/repo |
| **npm / pip / cargo install** | Developer audience using the language's ecosystem | Published to the language registry |
| **Container image** | CI/CD and ephemeral usage | Minimal image with the binary as entrypoint |

**Rules:**

1. Every supported channel has a CI step that builds and publishes the artefact on
   release tag.
2. The installation matrix (channels × OS × architecture) is documented in the README
   and tested in CI for at least the primary channel.
3. Standalone binaries are checksummed (SHA-256) and the checksums file is published
   alongside the binaries. Signed binaries are preferred where feasible (GPG or
   Sigstore/cosign).
4. Reproducible builds are a goal: given the same source and toolchain version, the
   output binary should be byte-identical. Record the toolchain version in CI and in
   the release notes.

