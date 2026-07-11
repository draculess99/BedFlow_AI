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

## Stage 9 — Capacity What-If Simulator ✅

Implemented:

- authenticated Bed Manager/Administrator scenario execution;
- pharmacy, insurance, transport, home-care, and social-work clearance levers;
- Rehab/SNF placement clearance counts;
- additional case-manager availability;
- cleaning-bed release and temporary staffed-bed capacity;
- unit scope and planning horizon;
- current-versus-counterfactual XGBoost inference without retraining;
- potential review candidates, workflow bed recovery, delay-hours removed, and ED boarding relief;
- unit and patient impact tables;
- protected clinical stability and physician-signoff fields;
- identity-bound saved scenarios and CSV export;
- Stage 9 API, dashboard tab, documentation, smoke checks, and tests.

The output is a synthetic/proxy counterfactual estimate, not causal proof, a live ADT forecast, or discharge authorization.

## Stage 10A — Production Readiness and Observability ✅

Implemented:

- structured JSON request logging;
- request IDs and response-time headers;
- security headers on API responses;
- separate liveness, deep readiness, version, and administrator metrics endpoints;
- System Operations dashboard tab;
- GitHub Actions CI for secret scanning, compilation, tests, smoke checks, and release packaging;
- clean packaging scripts that exclude `.env`, Git history, password hashes, logs, and caches;
- Stage 10A documentation and six additional automated tests.

Important limitation:

- request metrics are process-local and reset on restart;
- JSON stores remain single-instance demonstration persistence; mount `/data` to preserve them across redeployments.

## Persistent JSON Volume Support ✅

Implemented:

- `BEDFLOW_DATA_DIR` separates mutable JSON records from static datasets and model artifacts;
- Railway and Docker deployments can mount `/data` for restart-safe persistence;
- missing runtime files are seeded once and existing mounted data is never overwritten;
- users, access events, tasks, task events, audit records, simulations, and memory use the configured directory;
- readiness and version endpoints report the active storage mode;
- atomic memory writes and clean release exclusions protect runtime files;
- PostgreSQL is intentionally deferred for this single-instance portfolio deployment.

JSON storage remains unsuitable for multiple replicas or high-concurrency production use.

## Stage 10C — Model Validation and Explainability ⏳

Remaining analytical hardening:

- patient-group train/test splitting for readmission data;
- probability calibration and precision-recall AUC;
- threshold and uncertainty analysis;
- subgroup evaluation and documented fairness limitations;
- formal SHAP explanations;
- data-quality and model-drift monitoring.

## Portfolio Finish ⏳

Remaining presentation work:

- screenshots and short demonstration video;
- GitHub Pages landing page;
- static architecture images as Mermaid fallbacks;
- recruiter-facing project summary.

Enterprise SSO/OIDC, MFA, HTTPS, and SMART on FHIR should only be added for a genuine multi-user or hospital integration.

## Recommended next implementation

Focus next on **model validation and explainability**: patient-group splitting, probability calibration, threshold analysis, precision-recall evaluation, and formal SHAP. The application feature set is already complete for a JSON-backed portfolio demonstration.
