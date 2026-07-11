# BedFlow AI Professionalization Roadmap

BedFlow AI is being upgraded from a single-patient discharge demo into a hospital-style patient-flow control tower.

Current core workflow:

```text
Patient selection → readiness checklist → task workflow → model prediction → committee recommendation → human decision → audit log
```

---

# Stage 0 — Baseline Patient-Level AI Demo

## Achieved

- Demo patient selection
- Patient-level AI evaluation
- XGBoost predictions for:
  - Discharge delay risk
  - 30-day readmission risk
  - Expected discharge delay hours
- Operational modules for:
  - Safety
  - Pharmacy
  - Transport
  - Rehab/SNF
  - Insurance
  - Home care
  - Bed capacity
- Committee recommendation
- Human-in-the-loop review
- Audit log and memory history

## Limitation

The app worked, but it felt like a single-patient ML demo rather than a hospital operations system.

---

# Stage 1 — Hospital Command Center Dashboard

## Achieved

- Hospital-wide KPI cards
- Unit bed board
- Prioritized discharge queue
- Patient selection from the queue
- New command-center API helpers

## Added files

```text
backend/command_center.py
docs/STAGE_1_COMMAND_CENTER.md
```

## Added endpoints

```text
GET /api/hospital_capacity
GET /api/discharge_queue?limit=75
```

## Result

The app now opens like a bed-flow control room instead of jumping straight into one patient.

---

# Stage 2 — Discharge Readiness Checklist

## Achieved

- Hospital-style discharge readiness checklist
- Checklist completion percentage
- Active blocker count
- Critical/high/medium blocker classification
- Owner role per blocker
- Recommended action per blocker
- Checklist-aware committee logic
- Checklist stored in audit record

## Added files

```text
backend/discharge_checklist.py
docs/STAGE_2_DISCHARGE_READINESS_CHECKLIST.md
```

## Added endpoint

```text
POST /api/discharge_checklist
```

## Result

The app can now explain exactly why a patient is or is not ready for discharge.

---

# Stage 3 — Task Ownership and Escalation Workflow

## Achieved in this version

- Checklist blockers are converted into operational tasks.
- Each task has an owner role.
- Each task has a status.
- Each task has an SLA timer.
- The system identifies overdue tasks.
- The system raises escalation levels.
- Users can update task status from the UI.
- A new **Tasks & Escalations** tab shows hospital-wide workload.
- Audit records can include the task snapshot at the time of human decision.

## Added files

```text
backend/tasks.py
database/tasks.json
docs/STAGE_3_TASK_OWNERSHIP_AND_ESCALATION.md
```

## Added endpoints

```text
GET  /api/tasks
GET  /api/tasks/summary
GET  /api/tasks/overdue
GET  /api/tasks/<patient_id>
POST /api/tasks/sync
POST /api/tasks/sync_all
POST /api/tasks/update_status
```

## Result

The app now tracks the operational work needed to move a patient toward discharge. It is no longer just saying what the problem is; it is assigning the work.

---

# Stage 5 — Model Lifecycle and Governance ✅ Implemented

## Goal

Move from demo-style in-memory training toward a more professional ML lifecycle with visible governance metadata.

## Features added

- Offline training script
- Saved XGBoost model artifacts
- Model version number
- Feature-column artifact
- Metrics history
- Generated model card
- Training timestamp
- Dataset hash / data version
- Dashboard governance panel
- API endpoints for governance, metrics history, model card, and artifact loading

## Added files

```text
training/train_models.py
models/model_registry.json
models/feature_columns.json
models/model_card.md
models/discharge_delay_xgb.joblib
models/readmission_xgb.joblib
models/delay_hours_xgb.joblib
database/model_metrics_history.json
docs/STAGE_5_MODEL_LIFECYCLE_AND_GOVERNANCE.md
```

## How to train

```bash
python training/train_models.py
```

Or use the UI:

```text
Model Performance & Governance → Train & Publish Versioned Models
```

## Done when

- App can load saved model artifacts at backend startup.
- Model version is visible in the UI.
- Metrics history and model card are visible in the UI.
- Predictions no longer rely only on first-request training when artifacts are present.

---

# Stage 6 — Public / Realistic Readmission Data Upgrade ✅ Implemented

## Goal

Strengthen the data story by training the 30-day readmission model from a public hospital readmission dataset while keeping operational discharge-delay modeling on BedFlow synthetic/proxy operational data.

## Implemented features

- Public diabetes hospital readmission dataset transformed into BedFlow-compatible schema.
- New `database/readmission_training_data.csv` generated from `dataset_diabetes/diabetic_data.csv`.
- Readmission-risk model now trains from the transformed public readmission layer.
- Discharge-delay and expected-delay-hours models still train from `database/bedflow_patient_data.csv`.
- Data-source provenance visible in the Model Performance & Governance tab.
- Model card now documents the hybrid data strategy.
- Race and gender are intentionally excluded from transformed model features.

## Added files

```text
backend/data_sources.py
scripts/prepare_diabetes_readmission_data.py
database/readmission_training_data.csv
docs/STAGE_6_PUBLIC_READMISSION_DATA_UPGRADE.md
```

## Added endpoints

```text
GET  /api/data_sources
POST /api/prepare_readmission_data
```

## Done when

- The public readmission layer can be prepared from the included dataset.
- Training publishes hybrid Stage 6 model artifacts.
- The dashboard displays data-source provenance.
- README and model card explain which model uses which data source.

---

# Stage 7 — FHIR-Style Adapter ✅ Implemented

## Features added

- De-identified FHIR R4-shaped export bundle
- Patient resource
- Encounter resource
- Observation resources for model and capacity signals
- Task resources mapped from discharge blockers
- CarePlan resource mapped from the readiness checklist
- Location resource for the hospital unit
- Capability and bundle API endpoints
- Dashboard export/download workflow

## Added files

```text
backend/fhir_adapter.py
docs/STAGE_7_FHIR_STYLE_ADAPTER.md
```

## Added endpoints

```text
GET  /api/fhir/capability
POST /api/fhir/bundle
```

---

# Stage 8 — Role-Based Workflow and Audit

## Features to add

- Role selector or login
- Different views by role
- Required override reason
- Audit filters by user, role, patient, and decision type

---

# Stage 9 — Capacity What-If Simulator

## Features to add

- Estimate beds recovered if blockers are cleared.
- Simulate clearing pharmacy, transport, insurance, or SNF backlogs.
- Show before/after bed capacity.

---

# Stage 10 — Portfolio Polish

## Features to add

- Screenshots
- Architecture docs
- Data-flow docs
- Demo video/GIF
- GitHub Pages landing page
- Deployment notes

---

# Recommended next step after Stage 7

Build **Stage 8 — Role-Based Workflow and Audit**.

This is the next best upgrade because the app now has model governance, public-data provenance, and a FHIR-style export. The largest remaining product gap is role-based access, required override reasons, and stronger user-attributed audit controls.

---

# Stage 4 — Explainability and Risk Reasons

## Goal

Make BedFlow AI more trustworthy by explaining why each model produced its prediction.

## Implemented features

- Patient-level explanation endpoint.
- Global feature-importance endpoint.
- Risk reason panel in the Control Tower.
- Top drivers for discharge delay risk.
- Top drivers for 30-day readmission risk.
- Top drivers for expected delay hours.
- Plain-English risk summary.
- Global feature importance in the Model Performance tab.
- Explanation payload saved into the audit log.

## Files added or modified

```text
backend/models.py
backend/api.py
backend/audit.py
frontend/dashboard.py
docs/STAGE_4_EXPLAINABILITY_AND_RISK_REASONS.md
README.md
```

## Method

The current implementation uses native XGBoost feature importance combined with the selected patient's active feature values. It is a lightweight explanation and not formal SHAP.

## Done when

- After clicking Evaluate Patient Case, the user sees model risk reasons.
- The risk reason section explains discharge delay, readmission risk, and expected delay-hours outputs.
- Model Performance shows global feature-importance tables.
- Saved audit records include the explanation payload.

## Suggested commit

```bash
git add .
git commit -m "Add explainability and risk reasons"
git push
```
