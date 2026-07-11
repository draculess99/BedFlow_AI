# Stage 2 — Discharge Readiness Checklist

Stage 2 converts BedFlow AI from a queue-and-prediction demo into a more realistic hospital discharge workflow.

The app already had raw fields such as `doctor_signoff_pending`, `pharmacy_med_rec_pending`, `transport_pending`, and `insurance_authorization_pending`. Stage 2 turns those fields into a structured checklist with completion status, blocker severity, owner role, and recommended action.

---

## What changed

### New backend module

```text
backend/discharge_checklist.py
```

This module builds a discharge readiness package for one patient:

- Checklist items
- Completion percentage
- Active blockers
- Critical/high/medium blocker counts
- Owner summary
- Readiness status
- Recommended actions

### New API endpoint

```text
POST /api/discharge_checklist
```

The endpoint accepts either a raw patient record or a payload with `patient_data` and optional `model_outputs`.

Example response shape:

```json
{
  "readiness_status": "Blocked",
  "completion_percent": 67,
  "completed_count": 8,
  "total_count": 12,
  "active_blocker_count": 4,
  "blocker_names": ["Insurance authorization", "Medication reconciliation"],
  "owner_summary": [
    {"owner": "Case Manager", "active_blockers": 2},
    {"owner": "Pharmacy", "active_blockers": 1}
  ]
}
```

### Dashboard UI

The Control Tower now shows a **Discharge Readiness Checklist** after a patient is selected and before the user clicks **Evaluate Patient Case**.

The UI shows:

- Readiness status
- Checklist completion percentage
- Active blocker count
- Critical/high blocker count
- Active blocker table
- Full checklist expander
- Owner workload summary

### Committee integration

The committee now uses the checklist in addition to model predictions and operational modules.

The priority order is:

1. Clinical readiness and safety
2. Critical checklist blockers under high bed pressure
3. High-severity blockers by owner role
4. Model delay/readmission risk
5. Operational module recommendations
6. Human review and audit logging

---

## Readiness statuses

| Status | Meaning |
|---|---|
| Ready for Discharge | All required items are complete or not required |
| Almost Ready | Only medium-priority blockers remain |
| Blocked | One or more high or critical operational blockers remain |
| Escalate Now | Critical blocker exists while bed pressure is high |
| Not Clinically Ready | Lab or vital-sign stability is incomplete |

---

## Checklist owners

| Owner | Typical blockers |
|---|---|
| Physician | Clinical stability, discharge order/signoff |
| Pharmacy | Medication reconciliation, discharge prescriptions |
| Utilization Management | Insurance authorization |
| Case Manager | Rehab/SNF placement, home care, case coverage |
| Transport | Transport ETA, facility transfer |
| Social Worker | Social barriers |
| Family / Case Manager | Pickup or caregiver support |

---

## Why this matters

Hospitals do not discharge patients just because a model says risk is low. They need the discharge process to be operationally complete.

Stage 2 makes BedFlow feel more like a hospital patient-flow product because it answers:

```text
What exactly is blocking discharge?
Who owns the blocker?
How severe is it?
What should happen next?
```

---

## Files changed

```text
backend/discharge_checklist.py
backend/api.py
backend/audit.py
backend/committee.py
frontend/dashboard.py
README.md
docs/STAGE_2_DISCHARGE_READINESS_CHECKLIST.md
```

---

## Next recommended stage

Stage 3 should add task ownership and escalation timers.

The checklist tells us what is blocked. Stage 3 should turn those blockers into tasks with owners, statuses, SLAs, and overdue escalation.
