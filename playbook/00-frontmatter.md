<!--
  The monolithic codex-machinae.md at the repository root is assembled from
  the sources under playbook/ by tools/build.py. Edit the playbook/ sources,
  then run `python tools/build.py` to regenerate — never edit the monolith
  directly.
-->

# Codex Machinae

**Version:** 2.0.0 — Draft
**Last updated:** 2026-06-10
**Scope:** Framework for developing, testing, deploying, maintaining, and monitoring software projects.

This playbook defines the entire lifecycle of a software project: from requirements gathering through to deployment and continuous dependency monitoring. It is designed for independent developers and small teams operating with autonomous agents (Claude Code, GSD, or equivalents).

> **⚠ SECURITY NOTICE:** Ruflo (formerly used in this project) has been abandoned due to serious security concerns. Do not install or use ruflo or any of its components. Use Claude Code natively or GSD as orchestrator.

---

## Table of Contents

### Part I — Core (universal)

1. [Requirements and planning](#1-requirements-and-planning)
2. [Project structure](#2-project-structure)
3. [Code quality](#3-code-quality)
4. [Security requirements](#4-security-requirements)
5. [Testing strategy](#5-testing-strategy)
6. [Documentation](#6-documentation)
7. [CI/CD and deployment](#7-cicd-and-deployment)
8. [Boundary Contracts](#8-boundary-contracts)
9. [Change classification](#9-change-classification)
10. [Remediation workflow](#10-remediation-workflow)
11. [Project lifecycle](#11-project-lifecycle)
12. [Conventions for AI agents](#12-conventions-for-ai-agents)

### Part II — Domain Appendices (activate per project type)

- [D1 Web Service](#d1-web-service)
- [D2 Library / SDK](#d2-library--sdk)
- [D3 CLI Tool](#d3-cli-tool)
- [D4 Embedded / Firmware](#d4-embedded--firmware)
- [D5 ML / Data Pipeline](#d5-ml--data-pipeline)
- [D6 Mobile App](#d6-mobile-app)
- [D7 Static Site / Frontend-only](#d7-static-site--frontend-only)

### Part III — Cross-cutting Modules (activate by trigger)

- [M1 Surveillance](#m1-surveillance)
- [M2 Security-sensitive](#m2-security-sensitive)
- [M3 Release & Distribution](#m3-release--distribution)
- [M4 Classification & Taxonomy](#m4-classification--taxonomy)

### Meta

- [Known limitations and roadmap](#known-limitations-and-roadmap)

### Appendices

- [A — Per-phase checklists](#appendix-a--phase-checklists)
- [B — Templates](#appendix-b--templates)
- [C — Glossary](#appendix-c--glossary)
- [D — Tooling Specifications](#appendix-d--tooling-specifications)

---

