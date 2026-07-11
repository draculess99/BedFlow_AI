# Stage 4 — Explainability and Risk Reasons

Stage 4 adds a professional explainability layer to BedFlow AI. The goal is to make every model prediction easier to review, defend, and audit.

Before this stage, the app showed model outputs such as discharge delay risk, readmission risk, and predicted delay hours. After this stage, the app also explains why the model produced those outputs.

---

## What Stage 4 Adds

- Patient-level risk reason panel in the Control Tower.
- Top drivers for discharge delay risk.
- Top drivers for 30-day readmission risk.
- Top drivers for expected delay hours.
- Plain-English explanation summary.
- Global model feature-importance tables in the Model Performance tab.
- New API endpoint for patient-level explanations.
- New API endpoint for global feature importance.
- Audit payload support for saving model explanations with human-reviewed decisions.

---

## Important Method Note

This implementation uses:

```text
XGBoost feature_importances_ + selected-patient active feature values
```

It is intentionally lightweight and dependency-free. It is not full SHAP.

For a portfolio demo, this is useful because it shows transparency without adding heavy explainability dependencies. A production version could add SHAP, calibration, model cards, and formal model-governance review.

---

## New Backend Behavior

The model layer now exposes:

```python
bedflow_models.explain_patient(patient_data, model_outputs, top_n=5)
bedflow_models.get_global_feature_importance(top_n=12)
```

The explanation function returns:

- Explanation method
- Plain-English summary
- Discharge delay drivers
- Readmission risk drivers
- Delay-hours drivers
- Governance note

Example payload shape:

```json
{
  "status": "success",
  "explanation_method": "XGBoost feature-importance + selected-patient active feature values. This is a lightweight explanation, not formal SHAP.",
  "plain_english_summary": "This case is rated High for discharge delay and Medium for readmission...",
  "discharge_delay": {
    "prediction": "High delay risk (0.72 probability)",
    "top_drivers": []
  },
  "readmission_risk": {
    "prediction": "Medium readmission risk (0.43 probability)",
    "top_drivers": []
  },
  "expected_delay_hours": {
    "prediction": "8.4 predicted delay hours",
    "top_drivers": []
  }
}
```

---

## New API Endpoints

```text
POST /api/explain_patient
GET  /api/model_feature_importance?top_n=12
```

### POST /api/explain_patient

Input:

```json
{
  "patient_data": {},
  "model_outputs": {},
  "top_n": 5
}
```

Output:

```json
{
  "plain_english_summary": "...",
  "discharge_delay": {
    "prediction": "...",
    "top_drivers": []
  },
  "readmission_risk": {
    "prediction": "...",
    "top_drivers": []
  },
  "expected_delay_hours": {
    "prediction": "...",
    "top_drivers": []
  }
}
```

### GET /api/model_feature_importance

Returns global feature-importance summaries for the currently trained in-memory models.

---

## Frontend Changes

After the user clicks **Evaluate Patient Case**, the Control Tower now shows:

```text
Model Explainability & Risk Reasons
```

This section includes:

- Plain-English summary
- Discharge delay risk drivers
- Readmission risk drivers
- Expected delay-hours drivers
- Why each driver matters
- Governance note

The **Model Performance** tab now includes global feature-importance tables for the three trained models.

---

## Audit Trail Changes

When the human supervisor saves a decision, the app now stores the explanation payload with the audit record:

```json
{
  "model_explanations": {
    "plain_english_summary": "...",
    "discharge_delay": {},
    "readmission_risk": {},
    "expected_delay_hours": {}
  }
}
```

This makes the saved decision easier to review later because the audit record contains not only the recommendation and human decision, but also the model reasoning summary shown at the time of review.

---

## Why This Makes the App More Professional

Hospital users do not want black-box predictions. They need to know:

- Why is this patient high risk?
- Which operational or clinical factors are driving the prediction?
- Is the model reacting to pharmacy, insurance, transport, home care, prior admissions, bed pressure, or clinical instability?
- Can a supervisor defend the decision later?

Stage 4 directly answers those questions.

---

## Done When

Stage 4 is complete when:

- Evaluating a patient shows risk reasons.
- The risk reason panel has top drivers for all three model outputs.
- The Model Performance tab shows global feature importance.
- Human-review audit records save the model explanation payload.
- The README documents the explainability method and limitation.

---

## Next Recommended Stage

The next stage should be:

```text
Stage 5 — Model Lifecycle and Governance
```

That should add:

- Saved model artifacts
- Model version number
- Training timestamp
- Feature column artifact
- Metrics history
- Model card
- Startup model loading instead of first-request training

This is the next logical step because Stage 4 explains the model, while Stage 5 makes the model lifecycle look production-grade.
