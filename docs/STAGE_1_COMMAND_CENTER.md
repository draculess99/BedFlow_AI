# Stage 1 — Hospital Command Center Dashboard

Stage 1 upgraded BedFlow AI from a single-patient demonstration into a hospital-style operations control tower.

## Workflow

```text
Simulated capacity snapshot
        ↓
Unit bed board
        ↓
Model-scored discharge review queue
        ↓
Select patient
        ↓
Evaluate patient case
```

## Current implementation

- Hospital capacity KPI cards.
- Simulated unit-level bed board.
- Prioritized multi-patient discharge review queue.
- XGBoost delay-risk probability and risk band.
- XGBoost 30-day readmission probability and risk band.
- XGBoost expected delay-hours estimate.
- Primary blocker, owner role, and next action.
- Composite bed-recovery/review-priority score.
- Patient selection directly from the queue.
- Active model version, source, and prediction timestamp.

## Backend

```text
backend/command_center.py
backend/models.py
backend/api.py
```

## API endpoints

```text
GET /api/hospital_capacity
GET /api/discharge_queue?limit=75
```

## Scoring behavior

The queue now batch-scores the demo patient table using the active saved XGBoost artifacts. The predictions are cached so loading the dashboard does not retrain or repeatedly score every row.

Known target/outcome fields are not used during command-center inference:

```text
delayed_discharge
readmitted_30_days
expected_discharge_delay_hours
```

If the model artifacts are unavailable, a conservative operational fallback uses only prospective information such as pending tasks, prior utilization, clinical stability, home support, length of stay, occupancy, and ED boarding pressure.

## Capacity disclaimer

The unit bed board is simulated/proxy capacity. Unit assignment is inferred from diagnosis and acuity, and capacities are demonstration constants. It is not a live ADT or hospital bed-management feed.

## Safety boundary

The queue ranks patients for authorized review. It never authorizes discharge and must not be treated as a clinical order.
