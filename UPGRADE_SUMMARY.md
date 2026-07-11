# Upgrade Summary

## Implemented in this release

- Replaced command-center target/proxy risk labels with cached XGBoost batch inference.
- Added queue probabilities, expected delay hours, model version, source, and timestamp.
- Added a prospective fallback that excludes known outcome columns.
- Clarified that unit capacity is simulated/proxy data.
- Added reviewer name and role to new audit records.
- Made rationale mandatory for override, escalation, and hold.
- Added an audit role filter.
- Renamed and simplified the model tab to explain models and artifacts in plain English.
- Standardized FHIR wording as FHIR R4-shaped demonstration output.
- Added environment-driven API/port configuration and Waitress support.
- Added Dockerfile, Railway config, Procfile, and `.dockerignore`.
- Expanded automated tests and made the smoke test non-destructive.
- Modernized README, roadmap, Stage 1 documentation, and changelog.

## Next recommended work

1. Full authenticated role-based workflow with backend permission enforcement.
2. PostgreSQL persistence and append-only task events.
3. Capacity what-if simulator.
4. Readmission calibration, patient-group validation, and threshold analysis.
5. CI, screenshots, video, and public portfolio landing page.
