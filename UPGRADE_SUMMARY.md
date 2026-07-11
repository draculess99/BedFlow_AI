# BedFlow AI Upgrade Summary

## Implemented in this package

This package completes **Stage 8 — Authenticated Role-Based Workflow**.

Key additions:

- signed local demo authentication;
- nine operational roles;
- backend-enforced permissions;
- role-owned task updates;
- immutable task event history;
- identity-bound human decisions;
- role-specific allowed decisions;
- administrator audit CSV export;
- administrator access-event viewer;
- updated README, roadmap, environment settings, and tests.

## Local demo login

Default password:

```text
BedFlowDemo!
```

Override before first startup:

```text
BEDFLOW_DEMO_PASSWORD=<new-password>
BEDFLOW_AUTH_SECRET=<long-random-secret>
```

## Next implementation

**Stage 9 — Capacity What-If Simulator** is next. It should simulate removing discharge blockers and estimate beds recovered, delay-hours removed, patients moved toward readiness, and potential ED boarding relief.

## Remaining production work

- PostgreSQL persistence;
- enterprise SSO/OIDC and MFA;
- structured monitoring;
- model calibration and patient-group validation;
- subgroup/fairness evaluation;
- formal SHAP;
- portfolio screenshots, video, CI, and public landing page.
