# Strategy Analysis & Transformation Roadmap

**Role:** Senior Software Analyst
**Goal:** Transform the `dev_playbook` repository from a collection of rigid documents into a **Universal Meta-Framework** for AI-assisted software development.

---

## 1. Current State

### Methodological Documentation
- `software-development-playbook.md`: A comprehensive document but too prescriptive about specific folders and tools (e.g. AST walker for REST API). It is in version `2.0.0 Draft`.
- `AI-AGENTS.md` & `GEMINI.md`: Operational rules for agents, currently heavily tied to text management and translation.
- `PROJECT_STATUS.md`: Correctly follows the format, documenting the development of the playbook itself.

### Examples and Templates
- `example/00-prd.md`: A high-quality application (Cortex) that contains lessons learned (snapshots, regression, L0-L2) not yet "promoted" to the general playbook.
- `templates/`: A series of blueprints reflecting the rigid structure of v2 of the playbook.

### Tooling and Agents
- `.claude/agents/`: Contains multiple versions of the `proofreader` (v1-v4), creating redundancy and confusion about the "official" version.
- `scripts/`: Utilities like `new-project.sh` that implement a fixed folder structure, contrary to the principle of "Emergent Architecture".

---

## 2. What should be Removed / Moved

To clean the repository and align it with the new vision, we must remove the "noise":

1.  **Agent Redundancy:** Remove `proofreader_v2.yaml` and `v3.yaml`. Keep only v4 as the official "Guest Agent" for quality control.
2.  **Rigid Prescriptiveness in the Playbook:** Remove the mandatory requirement for folders like `surveillance/` or `compat-data/` from §2.1. These should become optional modules to be activated only if necessary.
3.  **Hard-coded Examples:** Remove technology-specific references (e.g. "Synapse", "Cortex", "Stripe") from the theoretical sections of the playbook, moving them entirely to the examples section or making them abstract.
4.  **Static Templates:** Delete templates that do not provide for modularity (fixed DoD, PRD without dynamic checklist).

---

## 3. Action Plan

### Phase A: Playbook Refactoring (The Meta-Framework)
1.  **Generalisation of Surfaces:** Define the abstract concept of "Boundary Contract" (Hardware, UI, Data, API).
2.  **Emergent Expansion Protocol:** The LLM must be tasked with analysing the PRD and proposing: "I suggest adding folder `X` to manage risk `Y`".
3.  **Modular DoD:** Split the DoD into **Core** (process integrity: Status, Commits, Lint) and **Contextual** (project goals).
4.  **Abstract Remediation (L0-L2):** Integrate autonomy levels as risk management patterns, not as a requirement for every dependency.
5.  **Linguistic Standard:** Consolidate **British English** as the official working and output language for all projects in the framework.

### Phase B: Utility Agent Management
1.  **"Guest Agent" Standard:** Define how an agent (e.g. Proofreader) is "invited" into the project for a phase and how it is removed after production.
2.  **Portability:** Ensure each utility agent is self-contained.

### Phase C: The Lessons Learned Loop
1.  **Closure Protocol:** Create a template for the "Lessons Learned Report" at the end of each project.
2.  **Standard Promotion:** Define a process whereby if a v12 project discovers a useful new pattern, the analyst updates the Playbook (which might be at v3).

### Phase D: Independent Versioning
1.  **Decoupling:** Establish that the Playbook follows its own semantic versioning based on methodological maturity, while projects are free to evolve independently.

---

## Suggested Next Steps
1.  Begin refactoring `software-development-playbook.md` starting with the **"Emergent Architecture"** and **"Abstract Surface Definition"** sections.
2.  Consolidate the `.claude/agents/` folder.
3.  Update `scripts/new-project.sh` so that it creates only the "Minimum Core of Existence" (Status, Claude, README).
