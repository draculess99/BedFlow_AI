from __future__ import annotations

from backend.audit import log_human_decision


def test_audit_record_contains_reviewer_and_model_version(tmp_path, monkeypatch):
    audit_path = tmp_path / "audit.json"
    monkeypatch.setattr("backend.audit.AUDIT_LOG_PATH", str(audit_path))

    record = log_human_decision(
        patient_id="P-TEST",
        model_outputs={"delay_risk_level": "Low", "readmission_risk_level": "Low"},
        research_outputs={},
        committee_rec="Recommend clinician review",
        human_decision="Approve",
        human_note="Checklist verified.",
        memory_insight="No similar case.",
        reviewer_name="Alex Morgan",
        reviewer_role="Bed Manager",
        model_version="model-test-1",
    )

    assert record["reviewer_name"] == "Alex Morgan"
    assert record["reviewer_role"] == "Bed Manager"
    assert record["model_version"] == "model-test-1"
    assert record["timestamp_utc"].endswith("+00:00")


def test_api_rejects_unattributed_or_unexplained_exception_decisions():
    from backend.api import app

    client = app.test_client()
    base = {
        "patient_id": "P-TEST",
        "human_decision": "Override",
        "model_outputs": {},
        "research_outputs": {},
    }

    missing_identity = client.post("/api/save_human_decision", json=base)
    assert missing_identity.status_code == 400

    missing_reason = client.post(
        "/api/save_human_decision",
        json={**base, "reviewer_name": "Alex", "reviewer_role": "Bed Manager"},
    )
    assert missing_reason.status_code == 400
