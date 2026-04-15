# CLAUDE.md - Regole Operative per Agenti AI

Queste regole sono ottimizzate per agenti che operano sul "Software Development Playbook".

## Lingua e Stile
- **Lingua principale:** Italiano.
- **Tono:** Professionale, tecnico, asciutto.
- **Termini tecnici:** Usa l'inglese per i termini tecnici consolidati (es. "fail fast", "dependency inversion", "mock", "stub").

## Convenzioni di Naming (§3.2 del Playbook)
- **File:** kebab-case (es. `new-section.md`).
- **Commit:** Conventional Commits (es. `feat(docs): add section on agentic loops`).
- **Branch:** `<tipo>/<id>-<descrizione>` (es. `feat/US-DOC-001-setup`).

## Percorsi Protetti
- Non modificare le sezioni fondamentali del playbook (§1, §8, §9) senza previa conferma umana o via Issue/PR.
- Non alterare i parametri di severità e autonomia (§10, §12) a meno che non sia esplicitamente richiesto per evolvere il sistema.

## Regole Editoriali
- Massima lunghezza riga: 120 caratteri.
- Usa sempre intestazioni di primo livello per ogni documento principale.
- Mantieni i riferimenti incrociati (§...) aggiornati.
