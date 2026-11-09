# CRISC-MAP-002 — GRC Automation Lab Field-to-Canonical Mapping

**Version:** R0.1 | **Status:** Draft — Source Inspection Completed / Semantic Review Required  
**Parent:** CRISC-MAP-001 | **Related:** CRISC-DATA-001, CRISC-ARCH-001  
**Inspected baseline:** main @ `51234930d5305bb88835235d7ad3bf5610b0eedb`  
**Boundary:** Static source/CSV/schema inspection. No live database was supplied, executed or migrated.

## 1. CSV source mapping

### Controls — `projects/grc-automation-lab/data/controls.csv`

| Field | CRISC target | Mapping / limitation |
|---|---|---|
| control_id | Control.external_id | Source-scoped ID; no global ID |
| control_name | Control.name | Label, not unique identity |
| framework | Requirement/Control framework reference | Framework label only; no requirement ID, version or applicability |
| owner | Control.owner_reference | Free text; no owner registry |
| required_evidence | Control.expected_evidence_description | Description, not an evidence artifact |
| active | Control.lifecycle_status | Parse true/false; preserve raw value |

### Evidence — `evidence.csv`

| Field | CRISC target | Mapping / limitation |
|---|---|---|
| evidence_id | EvidenceRecord.external_id | Source-scoped ID |
| control_id | EvidenceRecord-to-Control relation | Resolve using source-scoped control ID |
| evidence_name | EvidenceRecord.name | Metadata label |
| status | EvidenceRecord.submission_status | Preserve raw value; version normalized vocabulary |
| submission_date | EvidenceRecord.submitted_at | Date precision; blank means unknown/not submitted |
| expiry_date | EvidenceRecord.valid_until | Date precision; blank means no expiry recorded |

**Boundary:** no artifact URI, content hash, storage location, media type, classification, collector, verifier or chain-of-custody data exists in this CSV. It tracks evidence metadata, not the evidence file itself.

### Tasks — `tasks.csv`

| Field | CRISC target | Mapping / limitation |
|---|---|---|
| task_id | RemediationTask.external_id (proposed) | Not equivalent to a RemediationCase ID |
| control_id | Task-to-Control relation | No finding key in source |
| task_name | RemediationTask.description | Text |
| owner | RemediationTask.owner_reference | Free text |
| due_date | RemediationTask.due_date | Date precision |
| status | RemediationTask.status | Distinct from finding/case status |

The evaluator uses overdue tasks to generate `SLA_OVERDUE` findings. This CSV alone does not persist tasks as canonical remediation cases.

### Risk register — `data/risk_register.csv`

| Field | CRISC target | Mapping / limitation |
|---|---|---|
| risk_id | Risk.external_id | Source-scoped |
| scenario | Risk.scenario | Preserve text |
| asset | Risk-to-Asset candidate relation | Free text; not a resolved Asset ID |
| probability | RiskAssessment.likelihood_raw | Ordinal 1–5; retain scale/method version |
| impact | RiskAssessment.impact_raw | Ordinal 1–5; retain scale/method version |
| owner | Risk.owner_reference | Free text |
| status | RiskAssessment.status (candidate) | Vocabulary requires approval |
| treatment | RiskTreatment.strategy (proposed) | No treatment plan/approval in row |

Current score = probability × impact with illustrative bands. It is not calibrated enterprise risk, and does not separately represent inherent/residual risk, confidence, appetite, acceptance or treatment effectiveness.

## 2. SQLite mapping

### Audit and finding lifecycle — `audit_store.py`

| Table | Observed fields | CRISC target / notes |
|---|---|---|
| audit_runs | run_id, executed_at, controls_evaluated, findings_count | AuditExecution / AssessmentRun; local integer PK and UTC ISO timestamp |
| audit_findings | finding_id, run_id, control_id, finding_type, severity, details | FindingOccurrence; run-scoped record |
| finding_entities | finding_key, control_id, finding_type, source_type, source_record_id, severity, first_seen_at, last_seen_at, created_at | Finding; SHA-256 key over control_id + finding_type + source_type + source_record_id |
| finding_occurrences | occurrence_id, finding_key, finding_id, run_id, details_snapshot, observed_at | FindingOccurrence; links entity to audit row/run; finding_id unique |

The current hash is an implementation contract, not yet a globally approved CRISC identity strategy. Changing its components requires compatibility design.

### Finding-linked remediation — `audit_store.py`

| Table | Observed fields | CRISC target / notes |
|---|---|---|
| remediation_cases | case_id, finding_key, case_status, owner, corrective_action, evidence_reference, validated_at, verification_result, created_at, updated_at | RemediationCase; one per finding_key; statuses OPEN, IN_REMEDIATION, PENDING_VALIDATION, RESOLVED, REOPENED |
| remediation_events | event_id, case_id, event_type, actor, reason, before_snapshot, after_snapshot, occurred_at, source_history_id | RemediationEvent/AuditEvent; event snapshots; case FK; source_history_id nullable unique |

A new finding can automatically create a case. A finding recurring after RESOLVED reopens the case and records a system event.

### Separate remediation register — `remediation_store.py`

| Table | Observed fields | CRISC target / notes |
|---|---|---|
| remediation_records | control_id, finding_type, owner, corrective_action, evidence_reference, validated_at, verification_result, updated_at, recorded_by, validated_by, change_reason | RemediationCase candidate; composite PK (control_id, finding_type); current-state upsert |
| remediation_history | history_id, control_id, finding_type, owner, corrective_action, evidence_reference, validated_at, verification_result, recorded_at, recorded_by, validated_by, change_reason, event_type, before_snapshot, after_snapshot | RemediationEvent/AuditEvent; append history |

## 3. Material reconciliation findings

1. **Two remediation models coexist.** `remediation_cases/events` and `remediation_records/history` have different keys, schemas and consumers. They are not interchangeable. `grc_analytics.py` reads the latter through `remediation_store`; it does not consolidate the former.
2. **Evidence is metadata-first.** CSV and remediation references do not prove artifact storage, integrity, retention or custody.
3. **Control and requirement are not separated fully.** `framework` is a label; there is no requirement ID, version or applicability record.
4. **Task and remediation are distinct.** `tasks.csv` drives SLA finding generation; it is not either SQLite remediation model.
5. **Finding identity is local.** Hash contract and source identity need versioning before cross-domain integration.
6. **Owners are free text.** No stable owner ID or organizational directory is present.
7. **Risk register is a starter.** Ordinal product score is illustrative.

## 4. Non-destructive canonical reconciliation design

Do not merge/drop/rename tables now. Define a logical RemediationCase with source adapters and a deterministic crosswalk that preserves legacy keys, both event streams, source table/key, event semantics and migration provenance. Specify precedence/conflict rules, dual-read comparison, idempotency, rollback and backup/restore before any write-path cutover.

Model evidence separately as EvidenceRecord (submission/status/validity metadata) and EvidenceArtifactReference (controlled URI, digest, media type, classification, retention and custody). The latter is target design, not current implementation.

## 5. Validation gates

- [ ] Obtain sanitized representative SQLite DB or generate a reproducible synthetic DB.
- [ ] Inspect actual table definitions, indexes, foreign keys, migration history and row counts.
- [ ] Inventory all read/write paths for both remediation models.
- [ ] Produce read-only crosswalk and conflict/orphan report.
- [ ] Define status precedence, duplicate handling and source lineage.
- [ ] Test idempotency, rollback, backup/restore and backward compatibility.
- [ ] Prove dashboards, reports and existing tests remain unchanged.
- [ ] Obtain explicit approval for a separate implementation PR.

## 6. Read-only profiler implementation

Added `tools/grc_sqlite_profiler.py` and `tests/test_grc_sqlite_profiler.py`. The tool opens SQLite using URI `mode=ro`, enables `PRAGMA query_only`, and reports object names, columns, indexes, foreign keys, row counts and migration version/name metadata. It does not export business row values or write to the inspected database.

Tests cover schema/count reporting, non-export of sensitive row values, unchanged database bytes and missing-file failure. The profiler tests passed in GitHub Actions run [42670487137](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/actions/runs/42670487137). The latest expanded test run is also executing against the subsequent documentation/CI commit.

Example (use a sanitized copy, not a production database):

```powershell
python tools/grc_sqlite_profiler.py --database .\\projects\\grc-automation-lab\\runtime\\grc_audit.db --output .\\runtime\\grc_schema_profile.json
```

The report path is separate from the inspected database. Do not commit real database files or reports containing sensitive metadata.

## 7. Next increment

Run the profiler against a sanitized copy or reproducible synthetic database. Review actual migration/index/FK metadata and produce a read-only crosswalk for both remediation models. No schema consolidation, write-path change or production data modification is included.

**Change log:** R0.1 maps inspected CSV/SQLite fields, documents the two remediation models, identifies evidence and identity limitations, and defines safe validation gates.
