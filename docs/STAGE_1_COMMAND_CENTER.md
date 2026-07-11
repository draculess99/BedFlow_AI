# Stage 1 — Hospital Command Center Dashboard

Stage 1 upgrades BedFlow AI from a single-patient demo into a hospital-style operations control tower.

## What changed

The original app flow was:

```text
Select one patient → Evaluate Patient Case → Review AI recommendation → Save human decision
```

Stage 1 keeps that workflow, but adds a hospital-wide operational layer before the patient-level review:

```text
Hospital capacity snapshot → Unit bed board → Multi-patient discharge queue → Select patient → Evaluate Patient Case
```

## New features

- Hospital capacity KPI cards.
- Unit-level bed board.
- Prioritized discharge queue.
- Primary blocker, owner role, and next-action columns.
- Bed-recovery priority score.
- Patient selection directly from the queue.

## New backend file

```text
backend/command_center.py
```

This file creates the command-center data without running full model inference for every patient.

## New API endpoints

```text
GET /api/hospital_capacity
GET /api/discharge_queue?limit=75
```

## Frontend changes

Updated file:

```text
frontend/dashboard.py
```

The Control Tower tab now shows:

1. Hospital-wide KPI row.
2. Unit bed board.
3. Prioritized discharge queue.
4. Patient case review panel.
5. Existing Evaluate Patient Case workflow.

## Important design note

The queue is an operational triage view. It uses existing fields such as:

- `expected_discharge_delay_hours`
- `primary_discharge_bottleneck`
- `current_bed_occupancy_percent`
- `ed_boarding_count`
- `readmitted_30_days`
- `prior_admissions_6mo`

It does not train or run XGBoost across every patient when the page loads. Full model prediction still happens on demand when the user clicks **Evaluate Patient Case**.

## Done when

Stage 1 is complete when the app opens into a hospital command-center experience and the user can choose a patient from a prioritized operational queue before running the original AI evaluation.
