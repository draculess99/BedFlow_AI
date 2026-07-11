# Modernization — Model-Scored Command Center

## Problem corrected

The original Stage 1 queue used proxy calculations and known demonstration outcome fields. That made the queue fast, but it could be mistaken for the actual XGBoost results and was not suitable as prospective scoring logic.

## Current design

The backend now:

1. loads the active published XGBoost artifacts;
2. aligns the complete demo patient table to `feature_columns.json`;
3. batch-generates delay, readmission, and delay-hours predictions;
4. caches the scored table by dataset modification time and model version;
5. builds the prioritized queue from those predictions and current operational blockers.

## Target-leakage protection

Inference is reindexed only to the saved feature-column artifact. These outcome columns are therefore excluded:

```text
delayed_discharge
readmitted_30_days
expected_discharge_delay_hours
```

An automated test changes those outcome values and confirms that the predictions remain unchanged.

## Fallback

If model scoring is unavailable, the queue uses a conservative prospective heuristic based on pending tasks, prior utilization, stability, support, length of stay, occupancy, and ED boarding. It does not use known outcomes.

## Safety

The queue is a review-prioritization tool. Low risk means eligible for routine or expedited review, not approved for discharge.
