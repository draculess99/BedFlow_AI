# BedFlow AI Professionalization Roadmap

This document tracks what is implemented and what remains for BedFlow AI.

## Stage 1 — Hospital Command Center ✅

Implemented:

- simulated hospital capacity snapshot;
- unit bed board;
- model-scored prioritized discharge review queue;
- cached XGBoost batch inference;
- blocker owner, next action, and review-priority score;
- patient selection from the queue.

Modernization update:

- queue scoring no longer uses known outcome/target columns;
- queue rows now expose probability, model version, source, and prediction timestamp;
- fallback scoring uses only prospective operational inputs.

## Stage 2 — Discharge Readiness Checklist ✅

Implemented:

- clinical readiness checks;
- medication, prescription, transport, insurance, placement, home-care, and social-work blockers;
- blocker severity, owner, reason, and recommended action;
- readiness status and completion percentage.

## Stage 3 — Task Ownership and Escalation ✅

Implemented:

- checklist blockers converted into tasks;
- owner roles;
- status workflow;
- SLA timers;
- overdue and escalation indicators;
- hospital task queue.

## Stage 4 — Explainability and Risk Reasons ✅

Implemented:

- patient-level model explanations;
- active feature values;
- global XGBoost feature importance;
- plain-English explanations;
- explanation payload stored with audit records.

Current method is feature importance plus active patient signals, not formal SHAP.

## Stage 5 — Model Lifecycle and Governance ✅

Implemented:

- saved `.joblib` model artifacts;
- feature-column artifact;
- model registry;
- model metrics snapshot and history;
- generated model card;
- explicit training and artifact publishing;
- load-latest-artifacts endpoint and dashboard controls.

## Stage 6 — Public Readmission Data Upgrade ✅

Implemented:

- public diabetes hospital encounter dataset included;
- transformation into the BedFlow feature schema;
- 30-day readmission target preparation;
- hybrid training strategy;
- data-source provenance dashboard.

Operational delay models remain synthetic/proxy models.

## Stage 7 — FHIR-Style Interoperability ✅

Implemented:

- de-identified FHIR R4-shaped `Patient`;
- `Encounter`;
- prediction `Observation` resources;
- discharge `Task` resources;
- `CarePlan`;
- `Location`;
- collection `Bundle`;
- capability endpoint;
- dashboard preview and JSON download.

This is an export-only demonstration adapter, not a certified FHIR server.

## Modernization increment ✅

Implemented after Stage 7:

- active-model XGBoost scoring across the prioritized queue;
- leakage-safe operational fallback;
- clearer simulated-capacity labels;
- reviewer name and role in new audit records;
- mandatory rationale for override, escalation, and hold;
- role filtering in the audit viewer;
- environment-driven API configuration;
- Waitress launcher support;
- Docker, Railway, and Procfile packaging;
- expanded tests;
- modernized README and model terminology.

## Stage 8 — Authenticated Role-Based Workflow ✅

Implemented:

- local demo users with password hashes;
- signed, time-limited bearer tokens;
- backend-enforced role permissions;
- Administrator-only model operations;
- role-owned task updates;
- Bed Manager/Administrator cross-role task supervision;
- role-specific final decision actions;
- identity-bound audit records;
- immutable task event history;
- Administrator audit CSV export;
- access-event logging;
- Streamlit sign-in, sign-out, identity, and permission display.

Production hardening still required outside the portfolio stage:

- enterprise SSO/OIDC or SAML;
- MFA and account lifecycle controls;
- HTTPS and managed secret rotation;
- database-backed identities and sessions;
- centralized immutable audit storage.

## Stage 9 — Capacity What-If Simulator ⏳

Recommended features:

- simulate clearing pharmacy blockers;
- increase transport capacity;
- add case-management availability;
- resolve insurance or placement backlogs;
- compare current and simulated beds recovered;
- estimate delay-hours removed;
- estimate ED boarding relief;
- save simulation scenarios.

## Stage 10 — Portfolio and Production Polish ⏳

Recommended features:

- screenshots and demo video;
- GitHub Pages landing page;
- CI workflow;
- PostgreSQL persistence;
- structured logging and monitoring;
- model calibration and threshold analysis;
- patient-group validation split;
- subgroup/fairness evaluation;
- formal SHAP explanations;
- SMART on FHIR and OAuth only for real integration.

## Recommended next implementation

Build the **Stage 9 capacity what-if simulator** next. Stage 8 now supplies the authenticated identity and permission layer needed to attribute saved simulations and operational actions.
