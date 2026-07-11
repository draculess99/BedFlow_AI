# Changelog

## 2026-07-11 — Model-Scored Command Center & Modernization

### Added

- Batch XGBoost scoring for the complete prioritized discharge queue.
- Cached queue predictions tied to the active model version.
- Delay/readmission probabilities, expected delay hours, model source, version, and prediction timestamps in queue records.
- Leakage-safety tests confirming known outcome columns do not affect inference.
- Reviewer name, role, model version, and UTC timestamp in new audit records.
- Mandatory rationale for override, escalation, and hold decisions.
- Environment-driven API/dashboard configuration.
- Waitress backend launcher support.
- Dockerfile, Railway configuration, Procfile, and `.dockerignore`.
- Expanded unit tests and package `__init__.py` files.

### Changed

- Replaced target-based command-center proxy scoring with saved XGBoost inference.
- Reworked fallback scoring to use only prospective operational inputs.
- Clarified that the unit bed board is simulated/proxy capacity.
- Renamed the dashboard model tab to **Model Quality & Transparency**.
- Added plain-English descriptions of models and saved artifacts.
- Standardized FHIR wording to **FHIR R4-shaped** rather than claiming formal compliance.
- Modernized the README and deployment instructions.

### Security

- Release packages should exclude `.env`, `.git`, caches, and local secrets.

## Stage 8 — Authenticated Role-Based Workflow

- Added local demo users with hashed passwords and signed bearer tokens.
- Added backend permission enforcement for model operations, task ownership, human decisions, audit export, and access-log viewing.
- Bound reviewer identity to the authenticated token instead of trusting UI fields.
- Added role-specific decision options.
- Added immutable task lifecycle events.
- Added administrator CSV audit export and access-event logging.
- Added Streamlit sign-in/sign-out controls and permission-aware actions.
- Added Stage 8 documentation and expanded automated tests to 10 passing tests.
