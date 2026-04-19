# Security Policy

## Scope

Codex Machinae is a **design document** — a process specification with no executable code,
running services, or stored credentials. A security issue in this context means a playbook
rule that, if followed, would lead to insecure software.

Examples of in-scope issues:

- A rule that recommends a deprecated or insecure cryptographic practice.
- A checklist that omits a critical security step (e.g. input validation, TLS enforcement).
- A template that encourages storing secrets in version control.
- A cross-reference that points to an outdated security standard.

## Out of scope

- Vulnerabilities in third-party tools mentioned by the playbook — report those to the
  respective maintainers.
- Typos, formatting, or non-security content gaps — use a standard
  [GitHub Issue](../../../issues) instead.

## Reporting a vulnerability

If you discover a security issue in the playbook's guidance, please report it privately:

1. **GitHub private vulnerability reporting** (preferred):
   go to the repository's **Security** tab → **Report a vulnerability**.
2. **Email:** contact the maintainer at the address listed in the repository profile.

Please include:

- The section reference (e.g. §4.2, M2.3, D1.4).
- A description of the insecure guidance and the risk it introduces.
- A suggested correction, if you have one.

## Response

- **Acknowledgement** within 7 days.
- **Resolution or public disclosure** within 30 days, depending on severity.
- Credit will be given in the CHANGELOG unless you prefer to remain anonymous.

## Supported versions

Only the latest version of `codex-machinae.md` on the `main` branch is supported.
Previous versions are not patched — fixes are applied to the current document.
