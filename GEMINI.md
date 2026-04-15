# GEMINI.md - Istruzioni Operative per il Playbook LLM

Questo file contiene i mandati fondamentali per Gemini CLI nella gestione del repository "Software Development Playbook". Queste istruzioni hanno la precedenza su ogni altra configurazione predefinita.

## Obiettivo del Progetto
Gestire, mantenere ed evolvere il framework universale per lo sviluppo di progetti software con l'ausilio di LLM e agenti autonomi. Il repository funge da "Single Source of Truth" per le metodologie di sviluppo del team.

## Mandati Fondamentali

### 1. Dogfooding (Principio Cardine)
Gemini CLI DEVE applicare le regole definite nel `software-development-playbook.md` per la gestione di questo stesso repository. In particolare:
- Mantenere aggiornato `PROJECT_STATUS.md` ad ogni sessione (§2.2).
- Usare Conventional Commits per ogni modifica (§3.3).
- Seguire la Definition of Done per ogni aggiornamento del playbook (§1.8).
- Documentare decisioni architetturali significative tramite ADR nella cartella `docs/adr/` (§1.5).

### 2. Gestione GitHub
- **Issue:** Ogni proposta di modifica o nuova sezione deve essere preceduta da un'Issue su GitHub per discuterne lo scope.
- **Pull Requests:** Nessuna modifica entra in `main` senza una PR. Le PR devono essere classificate secondo i bucket definiti nel playbook (§10.1): `safe`, `additive`, `breaking`, `p0`.
- **Changelog:** Ogni release o modifica significativa deve essere registrata in `CHANGELOG.md` seguendo lo standard Keep a Changelog (§6.4).

### 3. Manutenzione del Playbook
- **Ricerca SOTA:** Prima di aggiungere nuove sezioni su tecnologie emergenti (es. nuovi framework di agenzia), esegui una ricerca sullo stato dell'arte e documentala in `docs/research/` (§1.7).
- **Consistenza:** Assicurati che i riferimenti incrociati tra le sezioni (es. §9 che cita §1.7.5) siano sempre corretti e aggiornati.
- **Stile:** Mantieni il tono professionale, tecnico e asciutto del documento originale. Usa l'italiano come lingua principale per il contenuto del playbook, ma mantieni i termini tecnici standard in inglese dove appropriato (es. "fail fast", "dependency inversion").

### 4. Struttura dei File
Il repository deve rispettare rigorosamente la struttura definita nel §2.1 del playbook. Qualora mancassero directory o file obbligatori, Gemini CLI deve segnalarlo o crearli secondo necessità.

## Flusso di Lavoro Suggerito
1. **Analisi:** Leggi `PROJECT_STATUS.md` per capire il contesto attuale.
2. **Pianificazione:** Se la modifica è complessa, usa `enter_plan_mode` per delineare la strategia.
3. **Esecuzione:** Applica le modifiche in modo chirurgico.
4. **Validazione:** Verifica la correttezza formale del Markdown e l'integrità dei link interni.
5. **Conclusione:** Aggiorna lo stato del progetto e prepara il commit.
