## Appendix B — Templates

### B.1 PRD template

```markdown
# [Project Name] — Product Requirements Document

**Status:** Draft v1
**Owner:** [name]
**Last updated:** [date]

### Pre-implementation checklist

- [ ] [Decision 1 already confirmed]
- [ ] [Decision 2 already confirmed]

---

## 1. Purpose and scope

### 1.1 What this system guarantees
### 1.2 What this system does not cover

## 2. Users and stakeholders
## 3. Functional requirements
## 4. Non-functional requirements

### 4.1 Performance
### 4.2 Security
### 4.3 Accessibility
### 4.4 Scalability

## 5. Architectural constraints
## 6. Open questions

| # | Topic | Owner | Status |
|---|-------|-------|--------|

## 7. Later-phase work

| Item | Phase | Notes |
|------|-------|-------|

## Appendices
```

### B.2 User Story template

```markdown
# US-[AREA]-[NUMBER]: [Short title]

**Priority:** P0 | P1 | P2 | P3
**Estimate:** [hours/points]
**PRD ref:** §[section]
**Dependencies:** US-[xxx], US-[yyy]

## Story
As a [role]
I want [action]
So that [benefit]

## Acceptance Criteria

1. GIVEN [context]
   WHEN [action]
   THEN [result]

2. GIVEN [context]
   WHEN [action]
   THEN [result]

## Technical notes
[notes for the implementer]
```

### B.3 ADR template

```markdown
# ADR-[NUMBER]: [Title]

**Status:** proposed | accepted | deprecated | superseded by ADR-[n]
**Date:** YYYY-MM-DD

## Context
[Why this decision is necessary]

## Decision
[What was decided]

## Consequences
[Positive and negative impact]

## Alternatives rejected
[What was considered and discarded, with rationale]
```

### B.4 DEPENDENCIES.md template

```markdown
# Dependencies

## Critical dependencies

### [Dependency name]
- **Type:** REST API | SDK | Database | Service
- **Version:** [current version]
- **Contract:** [link to contract documentation]
- **Contract count:** [number of contracts in Boundary Contract Map, by axis]
- **Surveillance agent:** [agent id]
- **Last verified:** [date]
- **Notes:** [particular notes, known quirks, workarounds]

## Development dependencies

### [Name]
- **Purpose:** [what it is used for]
- **Version:** [version]
- **Pinned:** yes | no (range)
```

### B.5 Compatibility record template (M1)

```json
{
  "dependency": "[name]",
  "version": "[version that triggered the cycle]",
  "detected_at": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "[agent id: pkg-watch | api-probe | docs-watch | security-watch | container-watch]",
  "slots": {
    "latest": { "version": "[resolved]", "result": "pass | fail | error" },
    "recent": { "version": "[resolved]", "result": "pass | fail | error" },
    "baseline": { "version": "[resolved]", "result": "pass | fail | error" }
  },
  "rollup": "pass | fail | partial",
  "severity": "L0 | L1 | L2",
  "events": [
    { "type": "detected", "at": "...", "by": "..." },
    { "type": "classified", "at": "...", "severity": "..." },
    { "type": "remediated | adopted", "at": "...", "pr": "..." }
  ]
}
```

### B.6 OWASP review template (M2)

```markdown
# OWASP Top 10 Review — [Year]

**Reviewed by:** [name]
**Date:** YYYY-MM-DD
**OWASP version:** [e.g. 2021]

| # | Item | Covered by | Verified how | Status |
|---|------|-----------|-------------|--------|
| A01 | Broken Access Control | | | ✅ / ⚠️ / ❌ |
| A02 | Cryptographic Failures | | | |
| A03 | Injection | | | |
| A04 | Insecure Design | | | |
| A05 | Security Misconfiguration | | | |
| A06 | Vulnerable and Outdated Components | | | |
| A07 | Identification and Authentication Failures | | | |
| A08 | Software and Data Integrity Failures | | | |
| A09 | Security Logging and Monitoring Failures | | | |
| A10 | Server-Side Request Forgery (SSRF) | | | |

## Actions
[List any items that are not fully covered, with remediation plan]
```

### B.8 Boundary Contract Map example (§8)

> Complete `COMPATIBILITY.md` for a hypothetical web service that exposes a REST API,
> consumes Stripe and a PostgreSQL database, and renders a React SPA.

```json
{
  "contracts": [
    {
      "id": "rest.orders.create",
      "axis": "api",
      "direction": "inbound",
      "counterparty": "mobile-app",
      "shape": "POST /v1/orders",
      "file": "src/routes/orders.ts",
      "line": 28,
      "context": "createOrder()",
      "risk_weight": "high",
      "test_coverage": true,
      "last_verified": "2026-04-18"
    },
    {
      "id": "rest.orders.list",
      "axis": "api",
      "direction": "inbound",
      "counterparty": "mobile-app",
      "shape": "GET /v1/orders?status={status}",
      "file": "src/routes/orders.ts",
      "line": 55,
      "context": "listOrders()",
      "risk_weight": "medium",
      "test_coverage": true,
      "last_verified": "2026-04-18"
    },
    {
      "id": "stripe.charges.create",
      "axis": "api",
      "direction": "outbound",
      "counterparty": "stripe-api",
      "shape": "POST /v1/charges",
      "file": "src/payments/stripe-client.ts",
      "line": 42,
      "context": "createCharge()",
      "risk_weight": "high",
      "test_coverage": true,
      "last_verified": "2026-04-15"
    },
    {
      "id": "stripe.webhooks.charge.succeeded",
      "axis": "api",
      "direction": "inbound",
      "counterparty": "stripe-api",
      "shape": "POST /webhooks/stripe (event: charge.succeeded)",
      "file": "src/webhooks/stripe-handler.ts",
      "line": 17,
      "context": "handleChargeSucceeded()",
      "risk_weight": "high",
      "test_coverage": true,
      "last_verified": "2026-04-15"
    },
    {
      "id": "db.orders",
      "axis": "data",
      "direction": "outbound",
      "counterparty": "postgresql",
      "shape": "public.orders (id, user_id, status, total, created_at)",
      "file": "src/db/schema/orders.ts",
      "line": 8,
      "context": "OrderModel",
      "risk_weight": "high",
      "test_coverage": true,
      "last_verified": "2026-04-18"
    },
    {
      "id": "db.users",
      "axis": "data",
      "direction": "outbound",
      "counterparty": "postgresql",
      "shape": "public.users (id, email, hashed_password, role, created_at)",
      "file": "src/db/schema/users.ts",
      "line": 5,
      "context": "UserModel",
      "risk_weight": "high",
      "test_coverage": true,
      "last_verified": "2026-04-18"
    },
    {
      "id": "ui.orders.dashboard",
      "axis": "ui",
      "direction": "inbound",
      "counterparty": "end-user",
      "shape": "screen:orders-dashboard",
      "file": "src/ui/pages/OrdersDashboard.tsx",
      "line": 1,
      "context": "OrdersDashboard",
      "risk_weight": "medium",
      "test_coverage": false,
      "last_verified": "2026-04-10"
    },
    {
      "id": "env.stripe_secret_key",
      "axis": "data",
      "direction": "outbound",
      "counterparty": "runtime-environment",
      "shape": "env:STRIPE_SECRET_KEY",
      "file": "src/config/env.ts",
      "line": 12,
      "context": "loadEnv()",
      "risk_weight": "high",
      "test_coverage": true,
      "last_verified": "2026-04-18"
    }
  ],
  "generated_at": "2026-04-18T14:30:00Z",
  "generator": "ast-walker",
  "contract_count": 8,
  "axis_counts": {
    "api": 4,
    "data": 3,
    "ui": 1,
    "hardware": 0
  }
}
```

> **Reading guide.** The map covers all four axes. Two `api` contracts are inbound
> (the REST endpoints the mobile app calls), two are outbound (Stripe). The `data`
> axis includes both database schemas and an environment variable — the latter is a
> contract because changing the variable name breaks the deployment. The single `ui`
> entry has `test_coverage: false`, which the Surveillance module (M1) would flag as
> a gap. The `axis_counts` block feeds the cardinality guard (§8.4).

---

### B.7 Taxonomy term template (M4)

```yaml
id: "[NAMESPACE]-[NUMBER]"
label: "[Human-readable name]"
description: "[One-sentence definition]"
parent: "[parent term ID, or null if top-level]"
status: "active | deprecated"
deprecated_successor: "[successor term ID, if deprecated]"
deprecated_sunset: "YYYY-MM-DD"
introduced_in: "[taxonomy version, e.g. 1.2.0]"
source: "upstream:[framework-name] | local"
```

### B.9 Retrofit Audit template (§11.6)

```markdown
# Retrofit Audit — [Project Name]

**Date:** [YYYY-MM-DD]
**Analyst:** [name or agent ID]
**Repository:** [URL or path]
**Current state:** [brief description — e.g. "active development, no CI, partial tests"]

## Gap assessment

| Area | Playbook expectation | Current state | Gap severity | Effort estimate |
|------|---------------------|---------------|--------------|-----------------|
| Requirements artefacts (§1) | PRD, stories, ADRs, backlog | | | |
| Project structure (§2) | Standard layout, agent config | | | |
| Code quality (§3) | Linting, formatting, commits | | | |
| Security (§4) | Secrets management, input validation | | | |
| Testing (§5) | Coverage ratchet, tier distribution | | | |
| Documentation (§6) | README, CHANGELOG, code comments | | | |
| CI/CD (§7) | Pipeline with build/lint/test/deploy | | | |
| Boundary contracts (§8) | Contract map generated | | | |

## Contract map summary

| Axis | Direction | Count | Documented | Undocumented |
|------|-----------|-------|------------|--------------|
| api | inbound | | | |
| api | outbound | | | |
| data | inbound | | | |
| data | outbound | | | |
| ui | outbound | | | |
| hardware | inbound | | | |

## Activated modules and domains

| Module/Domain | Trigger met? | Rationale |
|---------------|-------------|-----------|
| D1 Web Service | | |
| D4 Embedded | | |
| D5 ML / Data | | |
| M1 Surveillance | | |
| M2 Security-sensitive | | |
| M4 Classification | | |

## Adoption plan

### T1 — Safety net (mandatory first)
1. [item]

### T2 — Structure
1. [item]

### T3 — Process
1. [item]

## Target lifecycle phase

**Recommended entry point:** Phase [2|3]
**Rationale:** [why this phase]
```

---

