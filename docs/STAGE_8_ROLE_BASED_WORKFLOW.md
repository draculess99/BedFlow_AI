# Stage 8 — Authenticated Role-Based Workflow

Stage 8 converts BedFlow AI from a free-form reviewer demo into a role-aware operational workflow.

## What was implemented

### Local authenticated demo identities

The backend creates local demonstration users on first startup. Passwords are stored as Werkzeug hashes and successful login returns a signed, time-limited bearer token.

Default local password:

```text
BedFlowDemo!
```

Override it before first startup with:

```text
BEDFLOW_DEMO_PASSWORD=<your-local-demo-password>
```

Available roles:

- Administrator
- Bed Manager
- Physician
- Nurse
- Pharmacist
- Case Manager
- Utilization Manager
- Social Worker
- Transport Coordinator

### Backend-enforced permissions

The backend—not the Streamlit interface—checks permissions for protected actions.

Examples:

- only an Administrator can retrain or reload model artifacts;
- a Bed Manager or Administrator can update any task;
- specialist roles can update only tasks owned by their operational role;
- final committee actions are restricted by role;
- only an Administrator can export the audit log or view the access log.

### Identity-bound human decisions

The reviewer name, user ID, and role are taken from the signed bearer token. Values supplied by the browser are not trusted as the source of identity.

Every new decision includes:

- immutable audit ID;
- authenticated user ID;
- reviewer name and role;
- authentication source;
- patient ID;
- AI recommendation;
- human action and rationale;
- model version;
- UTC timestamp;
- checklist, task, model, and explanation snapshots.

### Immutable task event history

Every task status change now appends a separate event containing:

- event ID;
- old and new status;
- patient and task IDs;
- authenticated actor;
- actor role;
- timestamp;
- optional note.

Historical events are not overwritten when the current task record changes.

### Administrator controls

Administrators can:

- download the decision audit as CSV;
- inspect the access log;
- retrain and reload models;
- update any operational task.

## New API endpoints

```text
GET  /api/auth/demo_users
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout
GET  /api/auth/role_matrix
GET  /api/tasks/events
GET  /api/audit/export.csv
GET  /api/access_log
```

Protected endpoints require:

```http
Authorization: Bearer <signed-token>
```

## Security boundary

This is a portfolio-grade local authentication layer. It demonstrates identity binding and backend authorization, but it is not a hospital production identity system.

A production deployment still requires:

- enterprise SSO/OIDC or SAML;
- MFA;
- HTTPS everywhere;
- managed secret rotation;
- database-backed users and sessions;
- account lifecycle and lockout policy;
- centralized immutable audit storage;
- formal privacy and security review.
