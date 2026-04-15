# Software Development Playbook

**Version:** 2.0.0 — Draft
**Last updated:** 2026-04-15
**Scope:** Framework universale per lo sviluppo, il testing, il deploy, la manutenzione e la sorveglianza attiva di progetti software.

Questo playbook definisce l'intero ciclo di vita di un progetto software: dalla raccolta dei requisiti fino al deploy e al monitoraggio continuo delle dipendenze. È pensato per sviluppatori indipendenti e piccoli team che operano con agenti autonomi (Claude Code, Ruflo, o equivalenti).

---

## Indice

### Parte I — Sviluppo

1. [Requisiti e pianificazione](#1-requisiti-e-pianificazione)
2. [Struttura del progetto](#2-struttura-del-progetto)
3. [Qualità del codice](#3-qualità-del-codice)
4. [Requisiti di sicurezza](#4-requisiti-di-sicurezza)
5. [Strategia di testing](#5-strategia-di-testing)
6. [Documentazione](#6-documentazione)
7. [CI/CD e deploy](#7-cicd-e-deploy)

### Parte II — Sorveglianza e manutenzione

8. [Dependency Surface Map](#8-dependency-surface-map)
9. [Agenti di sorveglianza](#9-agenti-di-sorveglianza)
10. [Classificazione dei cambiamenti](#10-classificazione-dei-cambiamenti)
11. [Matrice di test di compatibilità](#11-matrice-di-test-di-compatibilità)
12. [Remediation workflow](#12-remediation-workflow)
13. [Database di compatibilità](#13-database-di-compatibilità)
14. [Self-testing e osservabilità](#14-self-testing-e-osservabilità)

### Parte III — Gestione

15. [Ciclo di vita del progetto](#15-ciclo-di-vita-del-progetto)
16. [Convenzioni per agenti AI](#16-convenzioni-per-agenti-ai)

### Appendici

- [A — Checklist per fase](#appendice-a--checklist-per-fase)
- [B — Template](#appendice-b--template)
- [C — Glossario](#appendice-c--glossario)

---

# PARTE I — SVILUPPO

---

## 1. Requisiti e pianificazione

Ogni feature, bugfix o progetto parte da requisiti scritti. Codice senza requisiti documentati è debito tecnico dal primo commit.

### 1.1 Gerarchia dei documenti di requisiti

```
PRD (Product Requirements Document)
 └── Epic
      └── User Story
           └── Acceptance Criteria
                └── Task tecnico
```

Ogni livello è tracciabile al superiore. Un task tecnico senza user story di riferimento è un segnale d'allarme — potrebbe essere lavoro inutile o scope creep.

### 1.2 PRD (Product Requirements Document)

Il PRD è il documento di livello più alto. Definisce il **cosa** e il **perché**, mai il **come** (quello è architettura). Contenuto minimo:

| Sezione | Contenuto | Obbligatoria |
|---------|-----------|-------------|
| **Status e ownership** | Versione del draft, autore, data ultimo aggiornamento | Sì |
| **Purpose and scope** | Cosa il sistema garantisce e cosa NON copre | Sì |
| **Stakeholder e utenti** | Chi usa il sistema e in che contesto | Sì |
| **Requisiti funzionali** | Cosa il sistema deve fare, organizzato per area | Sì |
| **Requisiti non-funzionali** | Performance, sicurezza, accessibilità, scalabilità | Sì |
| **Vincoli architetturali** | Tecnologie obbligate, integrazioni, limitazioni | Sì |
| **Boundary con altri sistemi** | Cosa è responsabilità di altri repo/servizi/team | Sì |
| **Open questions** | Incognite note, con owner e strategia di risoluzione | Sì |
| **Decisioni architetturali** | ADR (Architecture Decision Records) referenziate | Raccomandata |
| **Later-phase work** | Lavoro esplicitamente rinviato, con motivazione | Raccomandata |
| **Appendici** | Documenti sorgente, riferimenti esterni | Raccomandata |

**Pre-implementation checklist.** Ogni PRD DEVE includere una checklist all'inizio del documento che elenca le decisioni già prese e confermate. L'implementatore la verifica prima di scrivere codice. Se una voce della checklist non corrisponde al codice nel repo, l'implementazione si ferma fino alla risoluzione.

### 1.3 User story

Formato standard:

```
Come [ruolo utente]
Voglio [azione]
In modo da [beneficio]
```

Ogni user story DEVE avere:

- **ID univoco** — formato `US-<area>-<numero>` (es. `US-AUTH-001`)
- **Priorità** — P0 (bloccante), P1 (must-have per release), P2 (should-have), P3 (nice-to-have)
- **Stima** — in ore o story point, aggiornata dopo la prima sessione di lavoro
- **Acceptance criteria** — lista di condizioni verificabili che definiscono "fatto"
- **Dipendenze** — riferimento ad altre user story che devono essere completate prima
- **Link al PRD** — sezione del PRD che questa story implementa

### 1.4 Acceptance criteria

Ogni criterio è una condizione binaria (passa o non passa). Formato:

```
DATO [contesto iniziale]
QUANDO [azione dell'utente o del sistema]
ALLORA [risultato atteso]
```

I criteri di accettazione diventano test. Se un criterio non è traducibile in un test automatizzato, va riscritto fino a quando non lo è.

### 1.5 Architecture Decision Records (ADR)

Ogni decisione architetturale significativa è documentata in un ADR. Formato minimo:

```markdown
# ADR-<numero>: <titolo>

**Status:** proposed | accepted | deprecated | superseded by ADR-<n>
**Date:** YYYY-MM-DD
**Context:** Perché questa decisione è necessaria.
**Decision:** Cosa è stato deciso.
**Consequences:** Impatto positivo e negativo della decisione.
**Alternatives rejected:** Cosa è stato considerato e scartato, con motivazione.
```

Gli ADR sono **append-only** — non si cancellano, si superano con nuovi ADR che li referenziano.

### 1.6 Gestione del backlog

Il backlog è una lista ordinata per priorità. Regole:

- Ogni item ha uno stato: `todo`, `in-progress`, `blocked`, `review`, `done`
- Nessun item resta `in-progress` per più di una settimana senza aggiornamento
- Item `blocked` devono avere un motivo e un owner per lo sblocco
- Item `done` devono avere tutti gli acceptance criteria soddisfatti e i test scritti
- Il backlog viene rivisto settimanalmente; item con priorità P3 più vecchi di 90 giorni vengono archiviati o cancellati

### 1.7 Ricerca sullo stato dell'arte

Prima di implementare una feature, un modulo, o un'integrazione, il sistema DEVE suggerire all'utente di condurre una ricerca sullo stato dell'arte. Questo vale sia per il progetto nel suo complesso sia per le singole parti.

#### 1.7.1 Quando la ricerca è obbligatoria

| Trigger | Cosa ricercare | Output atteso |
|---------|---------------|---------------|
| **Nuovo progetto** (Fase 0) | Progetti simili esistenti, framework consolidati, pattern architetturali dominanti nel dominio | Report con: soluzioni esistenti, pro/contro, decisione motivata su build vs adopt vs fork |
| **Nuova feature significativa** (P0 o P1) | Implementazioni di riferimento, librerie specializzate, pattern documentati | Sezione "State of the art" nella user story con link e valutazione |
| **Nuova dipendenza** | Alternative disponibili, confronto maturità/community/manutenzione, licenza | Tabella comparativa in `DEPENDENCIES.md` con motivazione della scelta |
| **Scelta tecnologica** (linguaggio, framework, database) | Benchmark recenti, trend di adozione, case study nel dominio | ADR con sezione "Alternatives rejected" compilata da ricerca reale |
| **Refactoring architetturale** | Pattern attuali nel settore, migrazioni documentate da altri progetti | ADR con riferimenti a esperienze simili |

#### 1.7.2 Cosa ricercare per ogni componente

Per ogni parte significativa del progetto, la ricerca dovrebbe coprire:

**Soluzioni esistenti.** Esiste già una libreria, un servizio, o un progetto open source che fa quello che sto per scrivere? Se sì, è più maturo, testato e mantenuto di quello che potrei produrre io? Regola: non reinventare la ruota a meno che le ruote esistenti non vadano bene per la mia strada — e documentare perché non vanno bene nell'ADR.

**Pattern e best practice.** Come risolvono questo problema i progetti maturi nello stesso dominio? Quali pattern architetturali sono emersi come dominanti? Quali anti-pattern sono stati documentati? Cercare: post di engineering blog di aziende rilevanti, conferenze recenti, RFC e proposal nei repository di riferimento.

**Evoluzione della tecnologia.** La tecnologia che sto usando è ancora la scelta migliore? Ci sono alternative più recenti che risolvono problemi noti della tecnologia attuale? La community è attiva o in declino? Cercare: GitHub star trend, frequenza di release, numero di contributor attivi, issue aperte vs chiuse.

**Esperienza di altri.** Chi altro ha fatto qualcosa di simile e cosa ha imparato? Quali errori posso evitare? Cercare: post-mortem pubblici, case study, thread su forum tecnici, talk da conferenze.

#### 1.7.3 Come l'agente AI supporta la ricerca

L'agente AI DEVE suggerire proattivamente la ricerca nei seguenti momenti:

**All'inizio di un nuovo progetto:** "Prima di iniziare l'implementazione, vuoi che faccia una ricerca sullo stato dell'arte per [dominio del progetto]? Posso cercare progetti simili, framework consolidati, e pattern architetturali usati nel settore."

**Quando viene aggiunta una nuova dipendenza:** "Stai per aggiungere [libreria]. Vuoi che verifichi se ci sono alternative più recenti o mature? Posso confrontare: maturità, frequenza di aggiornamento, dimensione della community, licenza, e eventuali problemi noti."

**Quando viene proposta una scelta architetturale:** "Questa decisione ha un impatto a lungo termine. Vuoi che cerchi come altri progetti nel dominio [X] hanno affrontato lo stesso problema? Posso trovare ADR pubblici, post di engineering blog, e case study."

**Quando il progetto entra in una nuova fase:** "Il progetto sta per affrontare [nuova area]. Vuoi che faccia un check sullo stato dell'arte per le tecnologie e i pattern usati in questa area?"

**Durante la revisione periodica:** "Sono passati [N] mesi dall'ultima ricerca sullo stato dell'arte per [componente]. Alcune delle tecnologie usate potrebbero avere alternative migliori o aggiornamenti significativi. Vuoi che faccia un check?"

#### 1.7.4 Registro delle ricerche

Ogni ricerca sullo stato dell'arte è documentata in `docs/research/`:

```
docs/research/
├── YYYY-MM-DD-<argomento>.md      # Report di ricerca
├── YYYY-MM-DD-<argomento>.md
└── index.md                        # Indice con data, argomento, esito
```

Formato del report:

```markdown
# Ricerca: [Argomento]

**Data:** YYYY-MM-DD
**Trigger:** nuovo progetto | nuova feature | nuova dipendenza | revisione periodica
**Autore:** umano | agente AI | entrambi

## Domanda di ricerca
[Cosa volevamo sapere]

## Soluzioni trovate
[Lista con pro/contro/maturità/licenza]

## Raccomandazione
[Cosa fare e perché]

## Fonti
[Link a documentazione, blog, repository, paper]

## Decisione presa
[Cosa abbiamo deciso e riferimento all'ADR se presente]
```

#### 1.7.5 Agente di ricerca stato dell'arte (State-of-the-Art Scout)

Oltre agli agenti di sorveglianza delle dipendenze (§9), il playbook prevede un agente dedicato alla ricerca dello stato dell'arte. Questo agente opera in modo diverso dagli altri: non monitora una singola dipendenza, ma scandaglia il panorama tecnologico intorno al progetto.

**Frequenza:** trimestrale per componenti stabili, mensile per componenti in fase attiva di sviluppo.

**Cosa fa:**

1. **Technology health check.** Per ogni tecnologia significativa nel progetto (linguaggio, framework, database, librerie chiave), verifica: ultima release, frequenza di release nell'ultimo anno, trend degli issue aperti, stato della documentazione, eventuali announcement di deprecation o end-of-life.

2. **Alternative scanning.** Cerca nuove librerie o servizi che risolvono lo stesso problema di una dipendenza esistente, ma con approccio diverso o migliore. Non suggerisce di cambiare — segnala che l'alternativa esiste e lascia la decisione all'umano.

3. **Pattern evolution.** Verifica se i pattern architetturali usati nel progetto sono ancora considerati best practice o se la community si è mossa verso approcci diversi. Cerca: aggiornamenti a styleguide ufficiali, nuovi RFC nei repository di riferimento, talk recenti da conferenze chiave.

4. **Security landscape.** Verifica se le practice di sicurezza del progetto sono allineate con le raccomandazioni correnti (OWASP, NIST, CIS benchmarks). Cerca: nuove vulnerability class, nuovi tool di scanning, aggiornamenti alle raccomandazioni.

5. **Ecosystem health.** Valuta la salute complessiva dell'ecosistema: la community è in crescita o in declino? Ci sono fork significativi? Ci sono controversie (licenza, governance, ownership) che potrebbero impattare il progetto?

**Output:** un report in `docs/research/` con segnalazioni classificate:

| Segnalazione | Significato | Azione |
|-------------|-------------|--------|
| `healthy` | La tecnologia è attiva, mantenuta, senza alternative superiori | Nessuna |
| `watch` | Esiste un'alternativa emergente o un trend da monitorare | Inserire nel prossimo ciclo di ricerca |
| `evaluate` | Un'alternativa è matura abbastanza da meritare una valutazione seria | Creare un ADR con confronto |
| `migrate` | La tecnologia è in declino, deprecata, o ha problemi significativi | Pianificare la migrazione nel backlog |
| `urgent` | End-of-life, vulnerability critica senza patch, fork ostile | Azione immediata |

### 1.8 Definition of Done

Un item è "fatto" quando TUTTE queste condizioni sono soddisfatte:

- [ ] La ricerca sullo stato dell'arte è stata condotta se applicabile (§1.7)
- [ ] Il codice è scritto e rispetta le convenzioni di stile (§3)
- [ ] Tutti gli acceptance criteria sono soddisfatti
- [ ] I test sono scritti e passano (§5)
- [ ] La coverage non è scesa sotto la soglia (§5.3)
- [ ] La documentazione è aggiornata (§6)
- [ ] Il codice è stato rivisto (self-review o peer review)
- [ ] Il CI è verde
- [ ] La surface map è aggiornata se sono state aggiunte/rimosse dipendenze esterne (§8)
- [ ] `PROJECT_STATUS.md` è aggiornato

---

## 2. Struttura del progetto

### 2.1 File obbligatori nella root

Ogni progetto DEVE contenere:

```
project-root/
├── CLAUDE.md                    # Regole per agenti AI
├── PROJECT_STATUS.md            # Stato corrente (4 sezioni fisse)
├── DEPENDENCIES.md              # Mappa dipendenze critiche e contratti
├── CHANGELOG.md                 # Storico dei cambiamenti per release
├── COMPATIBILITY.md             # Stato compatibilità con dipendenze esterne (generato)
├── docs/
│   ├── prd/                     # PRD e documenti di requisiti
│   │   └── 00-prd.md
│   ├── adr/                     # Architecture Decision Records
│   │   ├── 001-<titolo>.md
│   │   └── ...
│   ├── api/                     # Documentazione API (generata o manuale)
│   └── runbooks/                # Procedure operative (deploy, rollback, incident)
├── src/                         # Codice sorgente
├── tests/                       # Test (struttura specchiata a src/)
├── scripts/                     # Script di build, seed, utility
├── ci/                          # Configurazione CI/CD
│   └── adapters/                # Adapter per forge specifico (github/, gitlab/, ecc.)
├── compat-data/                 # Database di compatibilità
├── compatibility/               # Schema, surface map, cataloghi
├── surveillance/                # Configurazione agenti di sorveglianza
└── .config/                     # Configurazione linting, formatting, ecc.
    ├── eslint.config.js
    ├── prettier.config.js
    └── ...
```

### 2.2 PROJECT_STATUS.md

Aggiornato ad ogni sessione di lavoro. Quattro sezioni fisse:

```markdown
## Objective
Cosa il progetto deve raggiungere in questa fase.

## Modified Files
Lista dei file modificati nell'ultima sessione, con motivo.

## Logical State
Stato corrente: cosa funziona, cosa no, cosa è bloccato.

## Next Action
La prossima azione concreta da eseguire.
```

### 2.3 CLAUDE.md

Regole operative per agenti AI. Contenuto minimo:

- Lingua e stile di scrittura (es. British English, active voice, short sentences)
- Lista di parole vietate
- Scope delle modifiche consentite per livello di autonomia (L0/L1/L2)
- Convenzioni di naming per branch, commit, file
- Percorsi protetti (file che l'agente non può modificare senza conferma umana)
- Regole editoriali (no em dash, max lunghezza riga, ecc.)

---

## 3. Qualità del codice

### 3.1 Principi architetturali

Ogni progetto DEVE rispettare questi principi indipendentemente dal linguaggio:

**Separation of concerns.** Ogni modulo ha una responsabilità singola e ben definita. Il codice che parla con API esterne vive in un adapter/client layer separato dalla logica di business e dalla UI.

**Dependency inversion.** I moduli di alto livello non dipendono da moduli di basso livello — entrambi dipendono da astrazioni (interfacce, tipi, contratti). Questo rende il codice testabile e il client layer sostituibile.

**Fail fast.** Gli errori vengono rilevati e segnalati il prima possibile. Input non valido viene rifiutato al boundary, non propagato silenziosamente.

**Immutabilità per default.** Preferire strutture dati immutabili e funzioni pure. Lo stato mutabile è confinato in store/state manager espliciti.

**Explicit over implicit.** Nessuna magia nascosta: no global state non dichiarato, no side effect in getter, no import circolari.

### 3.2 Convenzioni di naming

| Elemento | Convenzione | Esempio |
|----------|------------|---------|
| File | kebab-case | `user-profile.ts`, `auth-client.py` |
| Classe/Componente | PascalCase | `UserProfile`, `AuthClient` |
| Funzione/metodo | camelCase (JS/TS), snake_case (Python) | `getUserById()`, `get_user_by_id()` |
| Costante | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT`, `API_BASE_URL` |
| Variabile d'ambiente | SCREAMING_SNAKE_CASE con prefisso progetto | `ARC_CORTEX_URL`, `APP_SECRET_KEY` |
| Branch | `<tipo>/<id>-<descrizione-breve>` | `feat/US-AUTH-001-login-flow` |
| Commit | Conventional Commits | `feat(auth): add login endpoint` |
| Test file | Stesso nome del file testato + `.test` o `.spec` | `auth-client.test.ts` |

### 3.3 Conventional Commits

Ogni commit message segue il formato:

```
<type>(<scope>): <description>

[body opzionale]

[footer opzionale]
```

Tipi consentiti:

| Tipo | Quando usarlo |
|------|--------------|
| `feat` | Nuova funzionalità |
| `fix` | Bugfix |
| `docs` | Solo documentazione |
| `style` | Formatting, semicolons, ecc. (nessun cambio di logica) |
| `refactor` | Cambio di codice che non aggiunge feature né fix bug |
| `test` | Aggiunta o modifica di test |
| `chore` | Build, CI, dipendenze, tool |
| `perf` | Miglioramento di performance |
| `ci` | Modifiche alla pipeline CI/CD |
| `revert` | Revert di un commit precedente |
| `compat` | Cambiamento legato alla compatibilità con dipendenze esterne |

Il footer `BREAKING CHANGE:` è obbligatorio per qualunque cambio che rompe backward compatibility.

### 3.4 Linting e formatting

Ogni progetto DEVE avere:

- **Linter** configurato e integrato nel CI. Il CI fallisce se ci sono errori di lint.
- **Formatter** configurato con regole identiche al linter. Nessun dibattito su stile: il formatter decide.
- **Pre-commit hook** (opzionale ma raccomandato) che esegue lint + format prima di ogni commit.

Configurazione raccomandata per linguaggio:

| Linguaggio | Linter | Formatter | Config file |
|-----------|--------|-----------|-------------|
| TypeScript/JavaScript | ESLint (flat config) | Prettier | `eslint.config.js`, `.prettierrc` |
| Python | Ruff (lint + format) | Ruff | `ruff.toml` o `pyproject.toml` |
| Rust | Clippy | rustfmt | `clippy.toml`, `rustfmt.toml` |
| Go | golangci-lint | gofmt | `.golangci.yml` |
| Bash | ShellCheck | shfmt | `.shellcheckrc` |

**Regola zero:** nessun commit entra nel repo con warning di lint. Warning è errore.

### 3.5 Complessità e metriche

Soglie che il CI DEVE applicare:

| Metrica | Soglia | Azione se superata |
|---------|--------|-------------------|
| Complessità ciclomatica per funzione | ≤ 15 | CI fail |
| Linee per funzione | ≤ 50 (indicativo) | Warning |
| Linee per file | ≤ 400 (indicativo) | Warning |
| Profondità di nesting | ≤ 4 livelli | CI fail |
| Parametri per funzione | ≤ 5 | Warning, suggerire oggetto opzioni |
| Import circolari | 0 | CI fail |
| `any` type (TypeScript) | 0 in produzione | CI fail (consentito in test con giustificazione) |
| `// @ts-ignore` o `# type: ignore` | 0 in produzione | CI fail (consentito con commento che spiega perché) |

### 3.6 Gestione degli errori

Regole universali:

- **Mai ingoiare errori silenziosamente.** Ogni `catch` deve loggare, rilanciare, o gestire esplicitamente. Un `catch` vuoto è un bug.
- **Errori tipizzati.** Definire classi/tipi di errore per ogni dominio dell'app. Non usare stringhe come errori.
- **Error boundary.** Ogni layer dell'architettura (UI, business logic, adapter, infra) ha il proprio error boundary che traduce errori del layer inferiore in errori significativi per il layer superiore.
- **Retry con backoff.** Le chiamate a servizi esterni devono avere retry con exponential backoff e limite massimo di tentativi. Mai retry infinito.
- **Timeout espliciti.** Ogni chiamata esterna ha un timeout configurato. Nessuna chiamata attende indefinitamente.

### 3.7 Gestione delle dipendenze

- **Lock file** sempre committato (`package-lock.json`, `Pipfile.lock`, `Cargo.lock`, `go.sum`).
- **Versioni esatte** per dipendenze dirette in produzione. Range (`^`, `~`) consentiti solo per dipendenze di sviluppo.
- **Audit regolare.** `npm audit`, `pip-audit`, `cargo audit` eseguiti nel CI su ogni PR.
- **Aggiornamento intenzionale.** Le dipendenze non si aggiornano "perché c'è una nuova versione" — si aggiornano quando c'è un motivo (bugfix, security patch, feature necessaria). L'aggiornamento è un task tracciato, non un effetto collaterale.
- **Dipendenze fantasma.** Il CI verifica che non ci siano import di pacchetti non dichiarati nelle dipendenze. Tool: `depcheck` (npm), `deptry` (Python).

### 3.8 Branching strategy

**Trunk-based development** per sviluppatori singoli e piccoli team:

- `main` è sempre deployabile
- Feature branch di breve durata (max 3-5 giorni)
- Nessun branch `develop` — è overhead inutile per team piccoli
- Branch naming: `<tipo>/<id>-<descrizione>` (es. `feat/US-AUTH-001-login`)
- Merge via squash (un commit per feature branch)
- Tag per release: `v<major>.<minor>.<patch>`

---

## 4. Requisiti di sicurezza

### 4.1 Principi fondamentali

**Defence in depth.** Nessun singolo controllo è sufficiente. Ogni layer valida i propri input indipendentemente.

**Least privilege.** Ogni componente ha solo i permessi minimi necessari. Token API, database user, file system access — tutto è ridotto al minimo.

**Zero trust on input.** Tutto l'input è ostile fino a prova contraria: query parameter, body di request, header, file upload, variabili d'ambiente, dati da API esterne.

### 4.2 Input validation

Ogni punto di ingresso dell'applicazione DEVE validare l'input:

| Layer | Cosa validare | Come |
|-------|--------------|------|
| **API endpoint** | Tipo, formato, range, lunghezza di ogni parametro | Schema validation (Zod, Pydantic, JSON Schema) |
| **Form UI** | Formato, lunghezza, caratteri consentiti | Validazione client-side + server-side (mai solo client) |
| **File upload** | Tipo MIME reale (non solo estensione), dimensione, contenuto | Magic bytes check, antivirus se disponibile |
| **Database query** | Parametri query, injection | Prepared statement / parametrised query (mai concatenazione di stringhe) |
| **Dati da API esterne** | Schema della risposta, campi obbligatori, tipi | Stessa validazione dell'input utente — un API esterna può essere compromessa |

**Regola:** la validazione è dichiarativa (schema), non imperativa (catena di `if`). Uno schema è testabile, documentabile, e riutilizzabile.

### 4.3 Autenticazione e autorizzazione

- **Password.** Mai in chiaro, mai in log, mai in URL. Hash con bcrypt/argon2, salt unico per utente.
- **Token.** JWT con scadenza breve (15 min access, 7 giorni refresh). Refresh token rotato ad ogni uso.
- **Session.** Cookie `HttpOnly`, `Secure`, `SameSite=Strict`. Session ID rigenerato dopo login.
- **API key.** Mai nel codice sorgente. Mai nel frontend. Sempre in variabile d'ambiente o secret manager.
- **Autorizzazione.** Controllata ad ogni request, non solo al login. RBAC o ABAC esplicito, mai hard-coded.

### 4.4 Secrets management

| Regola | Dettaglio |
|--------|----------|
| **Mai nel codice** | Nessun secret in file sorgente, commit, o log. `.gitignore` include `.env`, `*.key`, `*.pem` |
| **Variabili d'ambiente** | Metodo primario per secret in locale e CI |
| **Secret manager** | Per produzione: GitHub Secrets, Vault, AWS SSM, o equivalente |
| **Rotazione** | Ogni secret ha una data di scadenza. La rotazione è automatizzata o calendarizzata |
| **Audit** | Ogni accesso a secret è loggato. Se un secret è compromesso, va ruotato immediatamente |
| **`.env.example`** | Il repo contiene un `.env.example` con i nomi delle variabili (senza valori) e commenti esplicativi |

### 4.5 Checklist di sicurezza per ogni PR

- [ ] Nessun secret committato (verificato da tool: `trufflehog`, `gitleaks`)
- [ ] Input validato con schema a ogni boundary
- [ ] Query parametrizzate (nessuna concatenazione SQL)
- [ ] Errori non espongono stack trace o dettagli interni all'utente
- [ ] Header di sicurezza presenti (CSP, X-Frame-Options, X-Content-Type-Options)
- [ ] Dipendenze senza vulnerability note (`npm audit` / `pip-audit` clean)
- [ ] Rate limiting configurato per endpoint pubblici
- [ ] Log non contengono PII o secret

### 4.6 OWASP Top 10 come baseline

Ogni applicazione web DEVE essere protetta contro le OWASP Top 10 correnti. Il team rivede la lista annualmente e verifica che ogni voce sia coperta da test o configurazione.

---

## 5. Strategia di testing

### 5.1 Piramide dei test

```
          ┌─────────┐
          │   E2E   │  Pochi, lenti, costosi. Validano flussi utente completi.
         ┌┴─────────┴┐
         │Integration │  Medi. Verificano che i moduli funzionino insieme.
        ┌┴───────────┴┐
        │  Scenarios   │  Contract test contro servizi reali o emulati.
       ┌┴─────────────┴┐
       │     Unit       │  Molti, veloci, economici. Una funzione, un comportamento.
       └────────────────┘
```

| Tier | Cosa testa | Ambiente | Velocità | Quantità |
|------|-----------|----------|----------|----------|
| **Unit** | Funzione singola, logica pura | In-memory, mock completo | < 1s per test | Centinaia |
| **Scenario** | Contratto con servizio esterno | Emulatore o container reale | < 5s per test | Decine |
| **Integration** | Moduli che interagiscono | Container reale, database reale | < 30s per test | Decine |
| **E2E** | Flusso utente completo | Stack completo, browser reale | < 2min per test | Una manciata |

### 5.2 Regole per ogni tier

**Unit test:**
- Ogni funzione pubblica ha almeno un test
- Test il comportamento, non l'implementazione — se il refactor rompe il test ma non il comportamento, il test è sbagliato
- Nessuna dipendenza esterna (rete, file system, database) — tutto mockato
- Naming: `describe('functionName', () => { it('should <comportamento> when <condizione>') })`

**Scenario/Contract test:**
- Ogni superficie nella surface map ha almeno un contract test
- La validazione usa JSON Schema con `additionalProperties: true` (campi nuovi non rompono)
- I fixture sono generati da interazioni reali, non scritti a mano
- Set-based assertion per risposte con ordinamento non garantito

**Integration test:**
- Ogni flusso critico (login, CRUD principale, pagamento) ha almeno un integration test
- I test creano i propri dati e li puliscono — nessuna dipendenza da stato preesistente
- Dynamic port binding per container paralleli — nessuna porta hard-coded

**E2E test:**
- Copertura dei flussi utente critici (happy path + principali error path)
- Tool: Playwright (web), Detox (mobile), o equivalente
- Retry automatico per flaky test (max 2 retry), ma i test flaky vanno fixati, non ignorati
- Screenshot/video su failure per debug

### 5.3 Coverage

**Ratchet model:** la coverage può solo salire, mai scendere.

| Metrica | Soglia minima | Enforcement |
|---------|--------------|-------------|
| Line coverage | Definita nel baseline file, ratchet up-only | CI fail se scende |
| Branch coverage | Definita nel baseline file, ratchet up-only | CI fail se scende |
| Per-file coverage | Nessun file nuovo sotto il 70% | CI fail |
| Coverage delta su PR | ≥ 0% (la PR non può abbassare la coverage) | CI fail |

**Baseline file:** `coverage-baseline.json` nella root del progetto. Contiene la coverage per-file corrente. Il CI confronta e fallisce se una qualunque chiave scende.

**Escape valve:** una PR può abbassare la coverage solo con un footer nel commit message che spiega il motivo:

```
Low-Coverage-Reason: Refactor di auth-client.ts — test in follow-up PR #123
```

L'escape valve è tracciata e rivista settimanalmente. Nessun escape valve può restare aperto per più di 2 settimane.

### 5.4 Test data strategy

- **Inline creation.** I test creano i dati di cui hanno bisogno inline, non da file fixture condivisi. Questo rende ogni test auto-documentato e indipendente.
- **Factory pattern.** Per dati complessi, usare factory function che producono oggetti validi con default sensati e override puntuali.
- **Golden files.** Solo per snapshot testing (UI rendering, schema di risposta). Aggiornati esplicitamente con flag (`--update-snapshots`), mai silenziosamente.
- **Seed script.** Per database di sviluppo, uno script deterministico che popola dati realistici. Separato dai test.

### 5.5 Test nel CI

| Trigger | Tier eseguiti | Timeout | Parallelismo |
|---------|-------------|---------|-------------|
| Push su feature branch | Unit + lint | 5 min | Massimo |
| PR verso main | Unit + scenario + integration | 15 min | Per-tier |
| Merge su main | Unit + scenario + integration + E2E | 30 min | Per-tier |
| Scheduled (nightly) | Tutti + compat matrix completa | 60 min | Per-slot |
| Release tag | Tutti + smoke test su staging | 45 min | Sequenziale |

---

## 6. Documentazione

### 6.1 Documenti obbligatori

| Documento | Contenuto | Aggiornamento |
|-----------|----------|---------------|
| **README.md** | Scopo del progetto, quick start, architettura high-level, link ai doc | Ad ogni cambio significativo |
| **CHANGELOG.md** | Storico dei cambiamenti per release, formato Keep a Changelog | Ad ogni release |
| **DEPENDENCIES.md** | Dipendenze critiche, versioni, contratti, link a doc ufficiale | Quando cambia una dipendenza |
| **COMPATIBILITY.md** | Stato di compatibilità con dipendenze esterne (generato) | Automatico |
| **PROJECT_STATUS.md** | Stato corrente del progetto | Ad ogni sessione |
| **docs/prd/** | PRD e documenti di requisiti | Quando cambiano i requisiti |
| **docs/adr/** | Architecture Decision Records | Ad ogni decisione architetturale |
| **docs/runbooks/** | Procedure operative (deploy, rollback, incident response) | Ad ogni cambio di processo |

### 6.2 Documentazione del codice

**Commenti nel codice — quando e come:**

| Commenta | Non commentare |
|----------|---------------|
| Il **perché** di una decisione non ovvia | Il **cosa** (il codice lo dice già) |
| Workaround con link al bug/issue | Codice ovvio (`i++; // increment i`) |
| Assunzioni che potrebbero non essere vere in futuro | Codice che dovrebbe essere riscritto invece che commentato |
| Contratti e invarianti | TODO senza issue di riferimento |

**TODO/FIXME/HACK:** consentiti SOLO con riferimento a un issue:

```typescript
// TODO(US-AUTH-042): Replace with OAuth2 PKCE flow when Stripe supports it
// HACK(#issue-789): Workaround for upstream bug in synapse-client v2.237
```

TODO senza issue = il CI emette un warning. TODO più vecchi di 30 giorni senza issue = CI fail.

### 6.3 Documentazione API

Ogni API pubblica (REST, SDK, CLI) DEVE avere documentazione generata dal codice:

| Tipo | Tool raccomandato | Output |
|------|------------------|--------|
| REST API | OpenAPI/Swagger (da annotazioni) | `docs/api/openapi.yaml` |
| TypeScript SDK | TypeDoc | `docs/api/` |
| Python SDK | Sphinx + autodoc | `docs/api/` |
| CLI | `--help` + man page generata | `docs/cli/` |

La documentazione API è generata nel CI e pubblicata automaticamente. Documentazione API scritta a mano diverge dal codice — è un bug annunciato.

### 6.4 CHANGELOG.md

Formato Keep a Changelog (`keepachangelog.com`):

```markdown
## [Unreleased]

### Added
- Nuovo endpoint POST /api/v1/users (#123)

### Changed
- Migrato auth da session a JWT (#456)

### Deprecated
- Endpoint GET /api/v1/legacy-users — usare /api/v1/users

### Removed
- Supporto per Node.js 16

### Fixed
- Fix race condition nel WebSocket reconnect (#789)

### Security
- Aggiornato stripe-sdk per CVE-2026-1234
```

Il CHANGELOG è scritto dagli umani (o dall'agente AI), non generato dai commit. I commit sono troppo granulari; il CHANGELOG è per gli utenti del software.

---

## 7. CI/CD e deploy

### 7.1 Pipeline overview

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  COMMIT  │──▶│  BUILD   │──▶│  TEST    │──▶│  STAGE   │──▶│  DEPLOY  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
  lint +         compile       unit +         smoke +        health
  format +       bundle       scenario +      E2E su        check +
  secret         Docker       integration    staging        rollback
  scan           image                                       ready
```

### 7.2 Fasi della pipeline

#### 7.2.1 Build

- **Compilazione** del codice sorgente (TypeScript → JavaScript, ecc.)
- **Bundle** per produzione (tree shaking, minification, source map)
- **Build Docker image** con tag basato su commit SHA + versione semantica
- **Artefatti:** il build produce artefatti immutabili. Lo stesso artefatto testato in staging è quello deployato in produzione. Mai rebuilddare per produzione.

#### 7.2.2 Test

Esecuzione dei tier di test secondo la tabella in §5.5.

#### 7.2.3 Stage

- **Deploy automatico su staging** dopo test verdi su `main`
- **Smoke test** su staging: subset di E2E che verifica le funzionalità critiche
- **E2E completo** su staging per release candidate
- **Staging è una replica di produzione** (stessa infra, stessi secret [rotati], stesso database schema)

#### 7.2.4 Deploy

- **Deploy a produzione** triggerato da tag di release (`v*.*.*`)
- **Rolling update** o **blue-green** — mai deploy "big bang" senza rollback automatico
- **Health check** post-deploy: l'applicazione risponde su `/healthz` entro 60 secondi
- **Automatic rollback** se il health check fallisce dopo 3 tentativi
- **Feature flag** per feature rischiose: deploy il codice disabilitato, abilita gradualmente

### 7.3 Rollback

Ogni deploy DEVE essere reversibile. Il rollback è un'operazione di primo livello, non un'emergenza.

| Scenario | Azione | Tempo target |
|----------|--------|-------------|
| Health check fallisce post-deploy | Rollback automatico alla versione precedente | < 2 minuti |
| Bug critico scoperto in produzione | Rollback manuale via CI (un bottone/comando) | < 5 minuti |
| Data migration fallita | Restore da backup + rollback applicazione | < 30 minuti |
| Rollback non possibile (migration irreversibile) | Hotfix forward, deploy immediato | Dipende dalla fix |

**Regola:** se un deploy include una database migration irreversibile, deve essere taggato come `BREAKING` nel CHANGELOG e richiede approvazione esplicita prima del deploy.

### 7.4 Database migration

- **Migration forward-only.** Ogni migration ha un file `up` e un file `down`. Il `down` è testato — non è un placeholder vuoto.
- **Migration separata dal deploy dell'app.** La migration gira prima del deploy. Se la migration fallisce, il deploy non parte.
- **Backward compatibility.** La nuova versione del codice DEVE funzionare con la vecchia e la nuova versione del database per almeno un ciclo di deploy. Questo permette rollback senza rollback del database.
- **Data migration vs schema migration.** Le due sono separate. Schema prima, data dopo. Mai nella stessa migration.

### 7.5 Ambienti

| Ambiente | Scopo | Dati | Deploy |
|----------|-------|------|--------|
| **Local** | Sviluppo | Seed script | Manuale |
| **CI** | Test automatizzati | Generati dai test | Automatico su push |
| **Staging** | Validazione pre-produzione | Copia anonimizzata di produzione | Automatico su merge a main |
| **Production** | Utenti reali | Reali | Manuale/automatico su tag |

### 7.6 Configurazione come codice

- Tutta la configurazione CI/CD è nel repo (`.github/workflows/`, `.gitlab-ci.yml`, ecc.)
- Nessuna configurazione "a clic" nel forge — se non è nel repo, non esiste
- Configurazione specifica del forge in `ci/adapters/<forge>/`
- La logica di business del CI (script, classificatore, aggregatore) vive fuori dalla directory del forge — è portabile

### 7.7 Adapter pattern per CI

Tutta la logica CI che è specifica di GitHub Actions (o GitLab, o Forgejo) vive sotto `ci/adapters/<forge>/`. Il resto (script, classificatore, aggregatore, compat database) è portabile. Migrare a un nuovo forge è un single-directory swap + nuovo adapter.

---

# PARTE II — SORVEGLIANZA E MANUTENZIONE

---

## 8. Dependency Surface Map

La surface map è il cuore del sistema di sorveglianza. Risponde alla domanda: **dove esattamente nel codice consumo ogni dipendenza esterna?**

### 8.1 Definizione di superficie

Una "superficie" è qualunque punto di contatto tra il codice dell'app e una risorsa esterna:

| Tipo | Esempi |
|------|--------|
| REST endpoint | `GET /api/v1/users`, `POST /api/v2/auth/login` |
| WebSocket | `wss://service.example.com/events` |
| SDK method | `client.users.list()`, `db.query()` |
| Data model | Schema JSON, protobuf, modelli ORM |
| Config/env | Variabili d'ambiente, feature flag, chiavi API |
| File format | CSV ingest, JSON export, binary protocol |
| CLI tool | Comandi di build, linting, deploy |

### 8.2 Formato della surface map

```json
{
  "surfaces": [
    {
      "dependency": "stripe-api",
      "surface": "rest",
      "endpoint": "POST /v1/charges",
      "file": "src/payments/stripe-client.ts",
      "line": 42,
      "method": "POST",
      "context": "createCharge()",
      "risk_weight": "high",
      "test_coverage": true,
      "last_verified": "2026-04-15"
    }
  ],
  "generated_at": "2026-04-15T10:00:00Z",
  "generator": "manual|ast-walker|grep",
  "surface_count": 47
}
```

### 8.3 Generazione

Tre strategie, in ordine di affidabilità:

1. **AST walker** (migliore) — analisi statica del codice sorgente. Risolve template literal, import dinamici, type inference. Strumenti: `ts-morph` per TypeScript, `ast` per Python, `go/ast` per Go.
2. **Grep strutturato** — ricerca pattern con `ripgrep`. Veloce ma perde i percorsi dinamici.
3. **Manuale** — file curato a mano. Accettabile come stub iniziale, da sostituire appena possibile.

### 8.4 Guardia di cardinalità

Se il conteggio totale delle superfici cala di oltre il 10% tra una generazione e l'altra, il CI DEVE fallire. Cattura: refactor che spostano chiamate API fuori dal pattern riconosciuto, cambi di configurazione che escludono file, aggiornamenti del walker.

---

## 9. Agenti di sorveglianza

Gli agenti sono processi autonomi che monitorano le dipendenze esterne a intervalli regolari.

### 9.1 Architettura

```
┌─────────────────────────────────────────────────┐
│                  SCHEDULER                       │
│  (cron / CI schedule / workflow_dispatch)         │
└──────┬──────┬──────┬──────┬──────┬───────────────┘
       │      │      │      │      │
       ▼      ▼      ▼      ▼      ▼
   ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
   │Agent ││Agent ││Agent ││Agent ││Agent │
   │Pkg   ││Docker││GitHub││API   ││Docs  │
   │Watch ││Watch ││Watch ││Probe ││Watch │
   └──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘
      │       │       │       │       │
      ▼       ▼       ▼       ▼       ▼
   ┌─────────────────────────────────────┐
   │         CHANGE CLASSIFIER           │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │         IMPACT ANALYSER             │
   │    (cross-ref con surface map)      │
   └──────────────┬──────────────────────┘
                  │
          ┌───────┴────────┐
          ▼                ▼
   ┌────────────┐   ┌────────────┐
   │ REMEDIATION│   │  ADOPTION  │
   │   (fix)    │   │  (improve) │
   └────────────┘   └────────────┘
```

### 9.2 Tipi di agente

**9.2.1 Package Watch** — rileva nuove versioni delle dipendenze. Frequenza: 5 min (RSS) o 1h (JSON API). Filtro: solo release stabili.

**9.2.2 API Probe** — esegue contract test contro ogni endpoint nella surface map. Frequenza: 6h per endpoint critici, 24h per gli altri. Verifica: raggiungibilità, schema, semantica, campi nuovi/mancanti, deprecation header, rate limit, versioning.

**9.2.3 Docs Watch** — monitora changelog e documentazione ufficiale. Frequenza: 24h. Metodo: fetch + diff testuale.

**9.2.4 Security Watch** — rileva advisory di sicurezza. Frequenza: 15 min. Sorgente: GHSA, NVD, audit tool nativi. Qualunque advisory forza L2.

**9.2.5 Container/Image Watch** — rileva nuove immagini Docker. Frequenza: 15 min. Timeout: 90 min con backoff.

**9.2.6 State-of-the-Art Scout** — agente dedicato alla ricerca dello stato dell'arte. Diverso dagli altri agenti: non monitora una singola dipendenza, ma scandaglia il panorama tecnologico intorno al progetto. Frequenza: trimestrale per componenti stabili, mensile per componenti in sviluppo attivo.

Cosa fa ad ogni ciclo:

1. **Technology health check.** Per ogni tecnologia significativa del progetto, verifica: ultima release, frequenza di release nell'ultimo anno, trend issue aperti, stato documentazione, annunci di deprecation o end-of-life.

2. **Alternative scanning.** Cerca nuove librerie o servizi che risolvono lo stesso problema di una dipendenza esistente con approccio diverso o migliore. Non suggerisce di cambiare — segnala che l'alternativa esiste e lascia la decisione all'umano.

3. **Pattern evolution.** Verifica se i pattern architetturali usati nel progetto sono ancora best practice o se la community si è mossa verso approcci diversi. Cerca: aggiornamenti a styleguide ufficiali, nuovi RFC, talk da conferenze chiave.

4. **Security landscape.** Verifica se le practice di sicurezza sono allineate con le raccomandazioni correnti (OWASP, NIST, CIS).

5. **Ecosystem health.** Valuta la salute dell'ecosistema: community in crescita o declino, fork significativi, controversie (licenza, governance, ownership).

Output: report in `docs/research/` con segnalazioni classificate in 5 livelli: `healthy` (nessuna azione), `watch` (monitorare nel prossimo ciclo), `evaluate` (creare ADR con confronto), `migrate` (pianificare migrazione nel backlog), `urgent` (azione immediata — end-of-life, vulnerability critica, fork ostile).

L'agente suggerisce proattivamente la ricerca quando: si inizia un nuovo progetto, si aggiunge una dipendenza, si propone una scelta architetturale, il progetto entra in una nuova fase, o sono passati N mesi dall'ultima ricerca su un componente. Dettagli completi in §1.7.

### 9.3 Heartbeat

Ogni agente, ad ogni ciclo — anche quando non rileva nulla — emette un heartbeat. Alert se il più recente è più vecchio di 6 ore.

### 9.4 Configurazione multi-sorgente

Per ogni dipendenza critica, almeno due sorgenti con ruoli diversi: primaria (trigger rapido) e backstop (recovery). Il backstop riconcilia le versioni mancate quando la primaria torna attiva.

---

## 10. Classificazione dei cambiamenti

### 10.1 Bucket

| Bucket | Descrizione |
|--------|-------------|
| `data-model` | Cambiamenti a schemi, modelli, tipi |
| `api-endpoint` | Endpoint aggiunti, rimossi, modificati |
| `sdk-method` | Metodi di libreria cambiati |
| `auth` | Autenticazione, permessi, policy |
| `config` | Variabili d'ambiente, feature flag |
| `docs-only` | Solo documentazione |
| `internal` | Refactoring interni, nessun impatto sulla superficie |
| `security` | Patch di sicurezza |
| `deprecation` | Deprecazione di superfici esistenti |
| `migration` | Migrazioni che modificano dati esistenti |

### 10.2 Severità

| Severità | Definizione | Azione |
|----------|-------------|--------|
| `safe` | Solo `internal` o `docs-only` | Auto-merge dopo CI verde |
| `additive` | Nuovi endpoint, nuovi campi, nuove librerie | PR con report |
| `breaking` | Superfici rimosse, rinominate, firma cambiata | Draft PR + revisione umana |
| `p0` | Security advisory, cambio protocollo | Draft PR + notifica immediata |

### 10.3 Never-auto-merge list

Condizioni che forzano sempre la revisione umana: rimozione/rinomina endpoint, cambio formato risposta, cambio protocollo auth, riduzione rate limit, rimozione metodo SDK, migration che riscrive dati, security advisory critical/high, cambio campo richiesto, cambio WebSocket handshake, regressione test funzionali.

---

## 11. Matrice di test di compatibilità

### 11.1 Slot

| Slot | Definizione | Scopo |
|------|-------------|-------|
| `latest` | Versione che ha triggerato il ciclo | Compatibilità con la novità |
| `recent` | Versione stabile più recente (finestra 21 giorni) | Regressioni mascherate |
| `baseline` | Versione pinnata, rivista trimestralmente | Contratto dichiarato |

### 11.2 Run manifest

All'inizio di ogni ciclo, prima di qualunque test, il sistema congela le versioni in un manifest JSON. Elimina ambiguità se la matrice si risolve diversamente tra step.

### 11.3 Test data

1. **Seed workload** — crea dati che esercitano ogni superficie consumata
2. **Golden queries** — query con risultati attesi per verificare integrità post-migrazione
3. **Snapshot regression** — carica snapshot di versioni precedenti e verifica accessibilità dati

---

## 12. Remediation workflow

### 12.1 Livelli di autonomia

| Livello | Trigger | Azione | Approvazione |
|---------|---------|--------|-------------|
| **L0** | `safe`, test verdi | Auto-merge | Nessuna |
| **L1** | `additive`, fix agentiva supera correctness gate | PR con fix-claim | Revisione umana |
| **L2** | `breaking`, `p0`, never-auto-merge match | Draft PR + notifica | Intervento umano |

### 12.2 Correctness gate (L1)

CI verde non basta. L'agente DEVE: validare contro lo schema specifico che ha triggerato il failure, includere fix-claim strutturato, aggiungere regression test, limitare le modifiche al client/adapter layer.

### 12.3 Circuit breaker

3 PR L1 aperte OPPURE 5 tentativi in 14 giorni → loop agentivo in pausa, tutto degrada a L2, ack umano richiesto.

### 12.4 Adoption workflow

Quando il classificatore rileva capacità nuove: cross-reference con surface map, aggiungere wrapper nel client, scrivere contract test, aprire PR di adoption + issue di tracking per le modifiche UI.

### 12.5 Deprecation tracking

Registrare la deprecazione, cross-reference con surface map, aprire issue `deprecation-watch`. La migrazione è sempre umana.

### 12.6 Major version protocol

L1 disabilitato, coverage baseline resettabile, surface map rigenerata obbligatoriamente, test harness verificato, issue come tracking epic.

### 12.7 Report all'umano

Per ogni cambiamento: cosa è cambiato, classificazione, dove impatta (file e righe), cosa va modificato per mantenere operatività, cosa si può adottare, risultati test, azione raccomandata.

---

## 13. Database di compatibilità

### 13.1 Formato

JSON flat in repo, un file per versione per dipendenza. Nessun database esterno.

### 13.2 Eventi (append-only)

L'array `events` è l'audit trail completo. Mai modificare o rimuovere eventi.

### 13.3 Aggregazione

Ogni slot produce il suo payload, un job di aggregazione li fonde. `pass` solo se tutti gli slot sono `pass`. Se un qualunque slot è `fail`, il rollup è `fail`. Se uno slot è `error`, il rollup è `partial`.

### 13.4 Portabilità

Plain JSON nel repo. Migrare a un altro forge = copia directory + nuovo adapter CI.

---

## 14. Self-testing e osservabilità

### 14.1 Detection heartbeat

Ogni ciclo di polling emette un heartbeat. Alert se il più recente è più vecchio di 6 ore.

### 14.2 Classifier retrospective

Job mensile: rivede tutti i record `safe` auto-merged negli ultimi 30 giorni. Tasso falsi negativi > 10% → alert per ricalibrare.

### 14.3 End-to-end canary

Job settimanale: inietta record sintetico per verificare l'intero percorso detection → classification → issue → surface-map cross-ref → event emission. Pulisce dopo la verifica.

### 14.4 Surface map cardinality guard

Se il conteggio superfici cala > 10%, il CI fallisce.

---

# PARTE III — GESTIONE

---

## 15. Ciclo di vita del progetto

### 15.1 Fase 0 — Ideazione e requisiti

1. Scrivere il PRD (§1.2)
2. Definire user story con acceptance criteria (§1.3, §1.4)
3. Documentare le decisioni architetturali in ADR (§1.5)
4. Creare il backlog ordinato per priorità (§1.6)
5. Definire la Definition of Done (§1.7)
6. Identificare le dipendenze critiche e documentarle in `DEPENDENCIES.md`

### 15.2 Fase 1 — Bootstrap tecnico

1. Creare la struttura di directory (§2.1)
2. Configurare linting, formatting, pre-commit hook (§3.4)
3. Configurare la pipeline CI base (build + lint + unit test) (§7)
4. Scrivere `CLAUDE.md` con le regole operative (§2.3)
5. Generare la surface map iniziale (§8)
6. Configurare gli agenti di sorveglianza (§9)
7. Creare il primo record di compatibilità (`untested`)
8. Scrivere `.env.example` con tutte le variabili documentate (§4.4)
9. Scrivere il seed script per il database di sviluppo (§5.4)

### 15.3 Fase 2 — Sviluppo attivo

1. Lavorare per user story, rispettando la Definition of Done (§1.7)
2. Aggiornare `PROJECT_STATUS.md` ad ogni sessione (§2.2)
3. Scrivere test per ogni tier appropriato (§5)
4. Mantenere la coverage ratchet (§5.3)
5. Aggiornare documentazione API e CHANGELOG (§6)
6. Gli agenti girano in background e producono record di compatibilità
7. Le PR di fix e adoption vengono revisionate e merged
8. Mantenere la surface map aggiornata dopo refactor significativi

### 15.4 Fase 3 — Maturità e manutenzione

1. Gli agenti continuano la sorveglianza
2. Le fix sono principalmente L0/L1
3. Revisione trimestrale della baseline e delle soglie
4. Retrospective mensile del classificatore
5. Aggiornamento della never-auto-merge list
6. Revisione annuale della OWASP Top 10 e delle security practice

### 15.5 Fase 4 — Major upgrade di dipendenza

1. Il major-version protocol si attiva (§12.6)
2. L1 disabilitato, tutto è L2
3. Surface map rigenerata
4. Coverage baseline resettata
5. Test harness verificato
6. Ritorno a fase 3 dopo la migrazione

---

## 16. Convenzioni per agenti AI

### 16.1 Regole generali

- L'agente legge `CLAUDE.md` prima di qualunque azione
- L'agente aggiorna `PROJECT_STATUS.md` dopo ogni sessione
- L'agente non modifica mai file nella never-auto-merge list senza conferma umana
- L'agente non modifica mai la logica di business — solo client/adapter layer e test
- L'agente include sempre un regression test per ogni fix
- L'agente non finge di eseguire operazioni — se non può fare qualcosa, lo dice

### 16.2 Grounding su dati live

Il primo step di qualunque fix loop DEVE essere: recuperare i dati live dalla dipendenza e pinnarli nel contesto. Previene l'allucinazione di firme, endpoint, o comportamenti inesistenti.

### 16.3 Fix-claim obbligatorio

Ogni PR prodotta dall'agente DEVE includere un fix-claim strutturato (§12.2).

### 16.4 Scope limitato

L'agente L1 può SOLO aggiungere nuovi file, nuove export, modificare file nel client/adapter layer, aggiungere test.

L'agente L1 NON può modificare metodi esistenti, cambiare call site esistenti, alterare comportamento UI, modificare configurazione di deploy, cancellare file o codice.

### 16.5 Proposta prima del codice

Per feature complesse, l'agente DEVE proporre l'approccio in forma scritta (document o commento) e attendere l'approvazione dell'umano prima di scrivere codice. Nessun codice "a sorpresa".

### 16.6 Logging strutturato

Ogni azione dell'agente è loggata come evento nel database di compatibilità. Tutto è tracciabile, riproducibile, e auditabile.

---

## Appendice A — Checklist per fase

### A.1 Checklist Fase 0 (Requisiti)

- [ ] PRD scritto con tutte le sezioni obbligatorie (§1.2)
- [ ] Ricerca stato dell'arte condotta per il dominio del progetto (§1.7)
- [ ] Pre-implementation checklist nel PRD compilata e verificata
- [ ] User story con acceptance criteria per il primo sprint
- [ ] ADR per le decisioni architetturali fondamentali (con "Alternatives rejected" da ricerca reale)
- [ ] Backlog creato e ordinato per priorità
- [ ] Definition of Done definita e condivisa
- [ ] Dipendenze critiche identificate in `DEPENDENCIES.md` (con confronto alternative §1.7.1)

### A.2 Checklist Fase 1 (Bootstrap)

- [ ] Struttura directory creata (§2.1)
- [ ] Linter + formatter configurati e integrati nel CI (§3.4)
- [ ] Pipeline CI base funzionante (build + lint + unit) (§7)
- [ ] `CLAUDE.md` scritto (§2.3)
- [ ] Surface map generata (anche manuale) (§8)
- [ ] Agenti di sorveglianza configurati (§9)
- [ ] Primo record di compatibilità creato (`untested`)
- [ ] `.env.example` con tutte le variabili documentate (§4.4)
- [ ] Secret scan configurato nel CI (§4.5)
- [ ] Seed script per database di sviluppo (§5.4)
- [ ] Coverage baseline iniziale committata (§5.3)
- [ ] Heartbeat alert configurato (soglia: 6 ore) (§14.1)

### A.3 Checklist per ogni PR

- [ ] Il codice rispetta le convenzioni di naming (§3.2)
- [ ] Commit message in formato Conventional Commits (§3.3)
- [ ] Nessun warning di lint (§3.4)
- [ ] Nessun secret committato (§4.5)
- [ ] Input validato con schema a ogni boundary (§4.2)
- [ ] Test scritti per il codice nuovo/modificato (§5)
- [ ] Coverage non scesa sotto il baseline (§5.3)
- [ ] Documentazione aggiornata se necessario (§6)
- [ ] Surface map aggiornata se aggiunte/rimosse dipendenze (§8)
- [ ] Errori gestiti esplicitamente, nessun catch vuoto (§3.6)

### A.4 Checklist per release

- [ ] Tutti i test passano su tutti i tier (§5.5)
- [ ] CHANGELOG.md aggiornato (§6.4)
- [ ] Tag di versione creato (§3.8)
- [ ] Deploy su staging riuscito con smoke test verde (§7.2.3)
- [ ] Rollback testato (§7.3)
- [ ] Database migration testata (up E down) (§7.4)
- [ ] Documentazione API aggiornata (§6.3)
- [ ] Compat database aggiornato con lo stato corrente (§13)

### A.5 Checklist per sorveglianza

- [ ] Agenti attivi con heartbeat recente (< 6 ore) (§14.1)
- [ ] Canary settimanale superato (§14.3)
- [ ] Retrospective mensile eseguita (§14.2)
- [ ] Never-auto-merge list rivista (§10.3)
- [ ] Coverage baseline aggiornata (§5.3)
- [ ] Surface map rigenerata dopo refactor (§8)
- [ ] Thresholds riviste trimestralmente (§14)
- [ ] State-of-the-Art Scout eseguito nel trimestre corrente (§1.7.5, §9.2.6)
- [ ] Report SOTA rivisti e azioni pianificate per segnalazioni `evaluate` o `migrate`

---

## Appendice B — Template

### B.1 Template PRD

```markdown
# [Nome Progetto] — Product Requirements Document

**Status:** Draft v1
**Owner:** [nome]
**Last updated:** [data]

### Pre-implementation checklist

- [ ] [Decisione 1 già confermata]
- [ ] [Decisione 2 già confermata]

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

### B.2 Template User Story

```markdown
# US-[AREA]-[NUMERO]: [Titolo breve]

**Priorità:** P0 | P1 | P2 | P3
**Stima:** [ore/punti]
**PRD ref:** §[sezione]
**Dipendenze:** US-[xxx], US-[yyy]

## Story
Come [ruolo]
Voglio [azione]
In modo da [beneficio]

## Acceptance Criteria

1. DATO [contesto]
   QUANDO [azione]
   ALLORA [risultato]

2. DATO [contesto]
   QUANDO [azione]
   ALLORA [risultato]

## Note tecniche
[appunti per l'implementatore]
```

### B.3 Template ADR

```markdown
# ADR-[NUMERO]: [Titolo]

**Status:** proposed | accepted | deprecated | superseded by ADR-[n]
**Date:** YYYY-MM-DD

## Context
[Perché questa decisione è necessaria]

## Decision
[Cosa è stato deciso]

## Consequences
[Impatto positivo e negativo]

## Alternatives rejected
[Cosa è stato considerato e scartato, con motivazione]
```

### B.4 Template DEPENDENCIES.md

```markdown
# Dependencies

## Critical dependencies

### [Nome dipendenza]
- **Type:** REST API | SDK | Database | Service
- **Version:** [versione corrente]
- **Contract:** [link a documentazione del contratto]
- **Surface count:** [numero superfici nella surface map]
- **Surveillance agent:** [id agente]
- **Last verified:** [data]
- **Notes:** [note particolari, quirk noti, workaround]

## Development dependencies

### [Nome]
- **Purpose:** [a cosa serve]
- **Version:** [versione]
- **Pinned:** yes | no (range)
```

---

## Appendice C — Glossario

| Termine | Definizione |
|---------|-------------|
| **PRD** | Product Requirements Document — specifica del cosa e del perché |
| **ADR** | Architecture Decision Record — decisione architetturale documentata |
| **User Story** | Requisito funzionale dal punto di vista dell'utente |
| **Acceptance Criteria** | Condizioni binarie che definiscono "fatto" |
| **Definition of Done** | Checklist universale applicata a ogni item di lavoro |
| **Superficie** | Punto di contatto tra il codice dell'app e una risorsa esterna |
| **Surface map** | Inventario strutturato di tutte le superfici |
| **Bucket** | Categoria di cambiamento (api-endpoint, data-model, ecc.) |
| **Severità** | Livello di impatto del cambiamento (safe, additive, breaking, p0) |
| **Slot** | Una versione nella matrice di test (latest, recent, baseline) |
| **L0/L1/L2** | Livelli di autonomia nella remediation |
| **Heartbeat** | Segnale periodico che conferma che un agente è attivo |
| **Canary** | Test sintetico end-to-end del sistema di sorveglianza |
| **Golden query** | Query con risultato atteso per verificare integrità dati |
| **Fix-claim** | Dichiarazione strutturata che accompagna ogni fix agentiva |
| **Circuit breaker** | Meccanismo che disabilita l'automazione dopo troppi fallimenti |
| **Never-auto-merge** | Condizioni che forzano sempre la revisione umana |
| **Ratchet** | Meccanismo che impedisce alla coverage di scendere |
| **Escape valve** | Eccezione temporanea tracciata a una regola del ratchet |
| **Conventional Commits** | Standard per messaggi di commit strutturati |
| **Blue-green deploy** | Strategia di deploy con due ambienti alternati |
| **Rolling update** | Deploy graduale che sostituisce le istanze una alla volta |
| **Feature flag** | Toggle che abilita/disabilita una feature senza deploy |
| **SOTA Scout** | Agente che ricerca lo stato dell'arte per tecnologie e pattern del progetto |
| **Technology health check** | Verifica periodica della salute di una tecnologia (release, community, trend) |
| **Alternative scanning** | Ricerca di librerie o servizi alternativi a quelli in uso |
| **Pattern evolution** | Monitoraggio dell'evoluzione delle best practice architetturali nel settore |
