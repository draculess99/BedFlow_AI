# Stage 7 — FHIR-Style Interoperability Adapter

## Goal

Show how BedFlow AI can exchange a de-identified patient-flow case using familiar FHIR R4 resource shapes without claiming to be a certified EHR integration.

## Implemented

- Export-only FHIR-style adapter.
- Patient, Encounter, Observation, Task, CarePlan, Location, and Bundle resources.
- Deterministic demo identifiers and references.
- No names, addresses, dates of birth, or other PHI.
- API capability description and patient bundle endpoint.
- Streamlit tab with resource summary, JSON preview, and download.

## Endpoints

```text
GET  /api/fhir/capability
POST /api/fhir/bundle
```

## Bundle request

```json
{
  "patient_data": {},
  "model_outputs": {},
  "discharge_checklist": {},
  "tasks": []
}
```

## Important limitation

The adapter produces FHIR R4-shaped demonstration JSON. It is not a certified FHIR server, does not implement SMART on FHIR/OAuth, terminology validation, profiles, subscriptions, persistence, or EHR write-back.
