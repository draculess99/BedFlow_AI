# Stage 9 — Capacity What-If Simulator

Stage 9 turns BedFlow AI from a prediction-and-workflow dashboard into an operational planning prototype.

## What it does

The simulator takes the current synthetic/proxy patient cohort and the active saved XGBoost predictions, changes selected operational inputs, and re-runs inference without retraining the models.

Supported levers:

- pharmacy medication-reconciliation clearance percentage;
- insurance-authorization clearance percentage;
- transport blocker clearance percentage;
- home-care setup clearance percentage;
- social-work clearance percentage;
- number of Rehab/SNF placements cleared;
- additional case-manager availability;
- beds released from cleaning;
- temporary staffed beds opened;
- unit scope and planning horizon.

## Protected safety fields

The scenario engine never automatically changes:

- `lab_stability_flag`;
- `vital_sign_stability_flag`;
- `doctor_signoff_pending`.

A patient can be counted only as a **potential expedited-review candidate** when clinical stability and physician-signoff conditions are already satisfied. This is not discharge approval.

## Method

```text
Current patient cohort
        ↓
Current saved-model inference
        ↓
Apply selected operational changes
        ↓
Recalculate the remaining primary blocker
        ↓
Re-run the same saved XGBoost artifacts
        ↓
Compare current versus simulated results
```

The simulator reports:

- patients changed and improved;
- potential expedited-review candidates;
- workflow-based potential beds recovered;
- delay hours removed;
- High/Critical delay cases reduced;
- operational blockers removed;
- potential ED boarding relief;
- unit-level impact;
- highest-impact patient cases;
- current versus simulated snapshots.

## Authentication and auditability

Only the **Bed Manager** and **Administrator** roles can run and save scenarios. Other authenticated operational roles may view saved scenario history. Saved runs include the signed-in user's identity, role, timestamp, model version, scenario assumptions, and results.

API endpoints:

```text
GET  /api/simulations/capability
POST /api/simulations/run
GET  /api/simulations
GET  /api/simulations/export.csv
```

## Persistence

Saved scenarios are written to:

```text
<BEDFLOW_DATA_DIR>/simulation_runs.json
```

This JSON store is for a local portfolio demo. A production system should use transactional database storage with immutable event history and retention controls.

## Limitations

- Results are counterfactual associations, not causal proof.
- Operational delay models use synthetic/proxy data.
- The unit bed board is simulated, not a live ADT feed.
- One potential available staffed bed is assumed to relieve at most one ED boarder.
- Additional case managers affect availability for a bounded number of high-priority cases; they do not automatically complete blockers.
- The simulator does not authorize discharge or replace clinical judgment.
