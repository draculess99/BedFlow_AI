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
