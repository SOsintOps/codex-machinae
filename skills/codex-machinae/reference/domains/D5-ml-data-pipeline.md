## D5 ML / Data Pipeline

**Activation trigger.** The project trains or fine-tunes models, transforms datasets at scale,
or persists structured data subject to schema evolution (relational or otherwise).

**In addition to Core.** Core §5 testing fundamentals apply. This appendix adds the testing
patterns that only arise when data is being reshaped, and will grow to cover pipeline-
reproducibility, dataset versioning, drift monitoring, and evaluation contracts.

### D5.1 Golden queries for data migrations

For any migration that alters schema or rewrites data, maintain a small curated set of **golden queries** — canonical read queries whose results must match before and after the migration (modulo an explicit, documented allow-list of intentional differences).

Rules:

- Golden queries live alongside the migration script, version-controlled with it
- They are executed automatically against a pre-migration snapshot and the post-migration state; any unexplained divergence blocks promotion of the migration
- Each query has a short rationale explaining which invariant it protects (row counts per tenant, aggregate totals, referential integrity across renamed tables, …)
- "Intentional difference" entries are not free-form prose: they are a structured list referenced from the migration's remediation record (§10)

Golden queries are complementary to schema migrations' own tests; they catch semantic drift that schema-level checks miss (e.g. a column renamed correctly but backfilled with the wrong default).

### D5.2 Database migration

- **Forward-only migration.** Every migration has an `up` file and a `down` file. The `down` is tested — it is not an empty placeholder.
- **Migration separate from the application deploy.** The migration runs before the deploy. If the migration fails, the deploy does not start.
- **Backward compatibility.** The new version of the code MUST work with both the old and the new version of the database for at least one deploy cycle. This allows rollback without rolling back the database.
- **Data migration vs schema migration.** The two are separate. Schema first, data after. Never in the same migration.

**Irreversible-migration rule.** If a deploy includes an irreversible database migration, it must be tagged as `BREAKING` in the CHANGELOG and requires explicit approval before deploying. Because rolling back the application does not undo the migration, the rollback scenario for this class of change is "hotfix forward" — see Core §7.3.

### D5.3 Training-pipeline reproducibility

Every training run MUST be reproducible from its recorded inputs. The minimum record per run:

| Artefact | Content | Storage |
|----------|---------|---------|
| **Run manifest** | Dataset version, code commit, dependency lock, hyperparameters, random seeds, hardware spec (GPU model, driver version) | Version-controlled or experiment tracker |
| **Trained model** | Serialised weights + architecture definition | Model registry (MLflow, W&B, DVC, or equivalent) |
| **Evaluation report** | Metrics on the held-out evaluation set (D5.6) | Stored alongside the model in the registry |
| **Training log** | Loss curves, resource utilisation, wall-clock time | Experiment tracker |

**Determinism.** When the framework supports it, pin every source of non-determinism
(random seeds, CUDA deterministic mode, data-loader shuffle seed). Document any remaining
non-deterministic operations (e.g. certain GPU kernels) in the run manifest so that "same
inputs → same outputs" failures are explained, not mysterious.

**Pipeline-as-code.** The training pipeline is defined in version-controlled code, not in
notebook cells or manual shell commands. A single entry-point command (e.g. `make train`,
`dvc repro`, `python -m train`) reproduces the entire pipeline from raw data to evaluated
model. Interactive notebooks are permitted for exploration but are never the canonical
training path.

### D5.4 Dataset versioning

Datasets are versioned artefacts with the same rigour as code:

- Every dataset has a unique version identifier (content hash, tag, or monotonic version
  number). The identifier is recorded in the run manifest (D5.3).
- Dataset transformations (filtering, labelling, augmentation, splitting) are defined in
  code, not applied manually. The transformation pipeline is version-controlled alongside
  the data schema.
- Large datasets that cannot live in the Git repository are tracked via DVC, Git-LFS, or a
  dedicated registry. The pointer file (`.dvc`, `.gitattributes`, manifest) is committed;
  the data itself is stored externally.
- Schema changes to the dataset (new columns, changed types, dropped features) follow the
  same classification (§9) and remediation (§10) workflow as any other data-model change.

### D5.5 Drift monitoring

Once a model is serving predictions, the project monitors two kinds of drift:

**Data drift.** The distribution of incoming features diverges from the distribution the
model was trained on. Detection methods (choose at least one):

| Method | What it measures | Suggested threshold |
|--------|-----------------|---------------------|
| Population Stability Index (PSI) | Distribution shift per feature | PSI > 0.2 → alert |
| Kolmogorov–Smirnov test | Maximum CDF distance | p < 0.01 → alert |
| Jensen–Shannon divergence | Symmetric distribution divergence | JSD > 0.1 → alert |

**Concept drift.** The relationship between features and the target changes — the model's
predictions degrade even though the input distribution looks stable. Detected by monitoring
live performance metrics (accuracy, precision, recall, or the domain-specific metric defined
in D5.6) against the evaluation baseline. A sustained drop beyond a declared threshold
triggers a retraining investigation.

**Alert flow.** Drift alerts flow through Core classification (§9, bucket `data-model`) and
remediation (§10). Severity mapping:

| Signal | Severity | Action |
|--------|----------|--------|
| Data drift above threshold, no performance drop | L1 — `safe` | Log, monitor next window |
| Data drift + performance drop within tolerance | L2 — `review` | Schedule retraining evaluation |
| Performance drop beyond tolerance | L3 — `breaking` | Retrain or roll back to previous model |

### D5.6 Evaluation contracts

Every model has an **evaluation contract** — a versioned specification of how the model's
quality is measured before promotion to production.

| Element | Content |
|---------|---------|
| **Evaluation dataset** | A held-out set, versioned alongside training data (D5.4), never used during training |
| **Primary metric** | The single metric that gates promotion (e.g. F1, AUROC, RMSE) |
| **Threshold** | The minimum acceptable value of the primary metric; updated via ratchet (§5.3) |
| **Secondary metrics** | Additional metrics reported for context but not gating |
| **Slice analysis** | Performance broken down by critical subgroups (demographic, geographic, temporal) to surface hidden regressions |
| **Comparison baseline** | The currently deployed model's evaluation report; the new model must meet or exceed the primary metric |

The evaluation contract is executed automatically in CI. A model that fails the contract is
not promoted — it is sent back for investigation, not manually overridden.

