# Stage 6 — Public / Realistic Readmission Data Upgrade

## Goal

Strengthen the BedFlow data story by using a public clinical hospital dataset for the 30-day readmission model while keeping the operational bed-flow models on synthetic/proxy operational data.

## What changed

Before Stage 6, all three models were trained from the synthetic BedFlow dataset:

```text
bedflow_patient_data.csv
```

After Stage 6:

```text
Discharge-delay classifier        → synthetic/proxy BedFlow operations data
Expected-delay-hours regressor    → synthetic/proxy BedFlow operations data
30-day readmission classifier     → public diabetes hospital readmission data transformed into BedFlow schema
```

## Files added

```text
backend/data_sources.py
scripts/prepare_diabetes_readmission_data.py
database/readmission_training_data.csv
docs/STAGE_6_PUBLIC_READMISSION_DATA_UPGRADE.md
```

## Files modified

```text
backend/models.py
backend/api.py
frontend/dashboard.py
training/train_models.py
app.py
README.md
docs/BEDFLOW_PROFESSIONALIZATION_STAGES.md
```

## New API endpoints

```text
GET  /api/data_sources
POST /api/prepare_readmission_data
```

## How to prepare the public readmission layer

```bash
python scripts/prepare_diabetes_readmission_data.py
```

## How to train the Stage 6 hybrid model set

```bash
python training/train_models.py
```

Or in the UI:

```text
Model Performance & Governance
→ Prepare Public Readmission Data
→ Train & Publish Versioned Models
```

## Data transformation

The included public diabetes hospital dataset is transformed into the BedFlow feature schema.

The target is:

```text
readmitted_30_days = 1 if readmitted == "<30" else 0
```

The transformed rows are saved to:

```text
database/readmission_training_data.csv
```

The transformation maps public encounter fields into BedFlow-compatible proxy features such as:

```text
age
length_of_stay_days
prior_admissions_6mo
prior_ed_visits_6mo
prior_readmissions_12mo
medication_count
medication_complexity
diagnosis_group
acuity_level
discharge_destination
lab_stability_flag
vital_sign_stability_flag
```

Operational blocker fields such as pharmacy, transport, insurance, SNF/Rehab, home care, and bed pressure are still proxy fields. They are included for schema compatibility and demo workflow behavior, not as validated hospital operations measurements.

## Governance note

Race and gender are intentionally excluded from the transformed model features.

## UI change

The **Model Performance & Governance** tab now includes a **Stage 6 Data Sources** panel showing:

```text
BedFlow operational rows
Public raw dataset rows
Processed readmission training rows
Data paths
Readmission positive-label rate
Privacy note
Limitations
```

## Limitations

- The public dataset is diabetes-focused and not a full general-hospital discharge dataset.
- The operational bed-flow features remain synthetic/proxy.
- This is still not a clinically validated model.
- The system remains human-supervised decision support only.

## Done when

- `database/readmission_training_data.csv` exists.
- `/api/data_sources` shows the public readmission layer as ready.
- `/api/train_models` trains readmission risk from the transformed public dataset.
- The model card documents the hybrid data strategy.
