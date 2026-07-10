# BedFlow AI Professionalization Roadmap

BedFlow AI currently works as a single-patient discharge decision-support demo:

Patient selection → Evaluate patient case → AI prediction → operational blocker analysis → committee recommendation → human decision → audit log

The goal of this roadmap is to evolve BedFlow AI into a more professional hospital-style patient-flow control tower.

---

# Stage 0 — Current Baseline

## Goal

Document what the app already does before adding new features.

## Current functionality

- User selects a patient from the demo patient list.
- User clicks **Evaluate Patient Case**.
- Flask backend runs prediction logic.
- XGBoost models predict:
  - Discharge delay risk
  - 30-day readmission risk
  - Expected discharge delay hours
- Operational modules check:
  - Patient safety
  - Pharmacy
  - Transport
  - Rehab/SNF placement
  - Insurance authorization
  - Home care
  - Bed capacity pressure
- Committee logic produces a recommendation.
- Human supervisor reviews the recommendation.
- Decision is saved to audit log and memory history.

## Current limitation

The app works, but it feels like a patient-level AI demo rather than a real hospital operations system.

## Done when

- README explains the current workflow.
- README includes architecture and training/inference diagrams.
- GitHub repo can be cloned and run.

---

# Stage 1 — Hospital Command Center Dashboard

## Goal

Make the app feel like a hospital operations control tower instead of a single-patient demo.

## Features to add

- Hospital capacity KPI cards
- Multi-patient discharge queue
- Unit-level bed pressure table
- High-risk patient list
- Primary blocker column
- Next best action column

## New dashboard sections

### Hospital Capacity Overview

Show:

- Total beds
- Occupied beds
- Available beds
- Beds pending cleaning
- ED boarders
- Expected discharges today
- Delayed discharges
- Critical delay cases

### Unit Bed Board

Example:

| Unit | Beds | Occupied | Available | Pending Discharges | ED Boarders |
|---|---:|---:|---:|---:|---:|
| ED | 40 | 39 | 1 | 0 | 12 |
| ICU | 20 | 19 | 1 | 2 | 3 |
| Med/Surg | 80 | 76 | 4 | 11 | 7 |
| Telemetry | 35 | 34 | 1 | 5 | 4 |

### Discharge Queue

Example columns:

- Patient ID
- Unit
- Diagnosis group
- Delay risk
- Readmission risk
- Predicted delay hours
- Primary blocker
- Owner role
- Status
- Next action

## Files likely to modify

```text
frontend/streamlit_app.py
backend/api.py
backend/research_modules.py
database/bedflow_patient_data.csv