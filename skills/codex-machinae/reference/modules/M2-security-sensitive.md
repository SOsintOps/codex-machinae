## M2 Security-sensitive

**Activation trigger.** The project handles authentication, authorisation, or personally
identifiable information; OR serves untrusted clients over a network; OR processes
attacker-controlled input. When in doubt: if the project has a login flow, stores user data,
accepts file uploads, or exposes an API without a trusted-network assumption in the contract
map (§8), the trigger has fired.

**In addition to Core.** Core §4 (Fundamental principles, Input validation, Secrets management)
applies to every project. This module adds the patterns that make sense only when the trigger
above fires: identity handling, a per-PR security checklist, OWASP coverage, and
dependency-vulnerability management.

**Relationship to domain appendices.** M2 composes with any domain. When D1 (Web Service) is
active, M2 is almost always active as well. When D4 (Embedded) is active, M2 fires if the
device handles credentials, communicates over an untrusted channel, or processes
attacker-influenced input (OTA payloads, sensor data from an adversarial environment).

### M2.1 Authentication and authorisation

- **Passwords.** Never in plain text, never in logs, never in URLs. Hashed with bcrypt/argon2, unique salt per user.
- **Tokens.** JWT with short expiry (15 min access, 7 days refresh). Refresh token rotated on every use.
- **Session.** `HttpOnly`, `Secure`, `SameSite=Strict` cookies. Session ID regenerated after login.
- **API keys.** Never in source code. Never in the frontend. Always in an environment variable or secret manager.
- **Authorisation.** Checked on every request, not only at login. Explicit RBAC or ABAC, never hard-coded.

### M2.2 Security checklist for every PR

- [ ] No secrets committed (verified by tools: `trufflehog`, `gitleaks`)
- [ ] Input validated with schema at every boundary
- [ ] Parameterised queries (no SQL concatenation)
- [ ] Errors do not expose stack traces or internal details to the user
- [ ] Security headers present (CSP, X-Frame-Options, X-Content-Type-Options)
- [ ] Dependencies free of known vulnerabilities (`npm audit` / `pip-audit` clean)
- [ ] Rate limiting configured for public endpoints
- [ ] Logs do not contain PII or secrets

### M2.3 OWASP Top 10 as baseline

Every networked application MUST be protected against the current OWASP Top 10 (Web) or the
relevant OWASP vertical (API Security, Mobile, LLM, …) when one exists for the project's
domain.

**Annual review.** Once per year the team walks through each OWASP item and records, for each:

| Item | Covered by | Verified how | Last reviewed |
|------|-----------|-------------|---------------|
| A01 Broken Access Control | RBAC middleware + integration tests | CI + manual pentest | YYYY-MM-DD |
| A02 Cryptographic Failures | TLS termination + hashing policy (M2.1) | Config audit | YYYY-MM-DD |
| … | | | |

The table lives in `docs/security/owasp-review.md` (or equivalent). An empty or stale table
(last reviewed > 12 months ago) is flagged by the M2.2 checklist.

### M2.4 Dependency-vulnerability management

When M1 Surveillance is also active, its Security Watch agent (M1.1.2.4) detects advisories
automatically. This section defines the response policy regardless of how the advisory is
discovered.

| Advisory severity | Response SLA | Action |
|-------------------|-------------|--------|
| Critical (CVSS ≥ 9.0) | 24 hours | Patch, upgrade, or mitigate. If no fix exists, disable the affected feature and document the workaround |
| High (CVSS 7.0–8.9) | 72 hours | Patch or upgrade. Workaround acceptable only if the patch introduces a breaking change requiring D5.2-style migration |
| Medium (CVSS 4.0–6.9) | Next sprint | Schedule the upgrade; track in the backlog |
| Low (CVSS < 4.0) | Best effort | Upgrade when convenient; do not block releases |

**Transitive dependencies.** The policy applies to transitive (indirect) dependencies as well.
When a transitive dependency has a critical advisory and the direct dependency has not released
a fix, the project pins a patched fork or applies a lockfile override — and opens an upstream
issue. The override is recorded in the contract map (§8) so it is not forgotten.

