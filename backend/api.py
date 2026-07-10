from flask import Flask, jsonify, request
import pandas as pd
import json
import os
from .models import bedflow_models, DATA_PATH, METRICS_PATH
from .committee import run_committee
from .memory import get_memory_state, append_memory_history, find_similar_bedflow_events
from .audit import log_human_decision, get_audit_log

app = Flask(__name__)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "app": "BedFlow AI"})

@app.route("/api/train_models", methods=["POST"])
def train():
    try:
        metrics = bedflow_models.train_models()
        return jsonify({"status": "success", "metrics": metrics})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/model_metrics", methods=["GET"])
def metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            return jsonify(json.load(f))
    return jsonify({"status": "error", "message": "No metrics found"}), 404

@app.route("/api/demo_patients", methods=["GET"])
def demo_patients():
    if not os.path.exists(DATA_PATH):
        return jsonify([])
    df = pd.read_csv(DATA_PATH, keep_default_na=False)
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/predict_patient", methods=["POST"])
def predict():
    data = request.json
    try:
        preds = bedflow_models.predict_patient(data)
        return jsonify(preds)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/run_committee", methods=["POST"])
def committee():
    data = request.json
    patient_data = data.get("patient_data", {})
    model_outputs = data.get("model_outputs", {})
    try:
        result = run_committee(patient_data, model_outputs)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/memory_state", methods=["GET"])
def memory_state():
    return jsonify(get_memory_state())

@app.route("/api/save_human_decision", methods=["POST"])
def save_decision():
    data = request.json
    try:
        record = log_human_decision(
            patient_id=data.get("patient_id"),
            model_outputs=data.get("model_outputs"),
            research_outputs=data.get("research_outputs"),
            committee_rec=data.get("committee_recommendation"),
            human_decision=data.get("human_decision"),
            human_note=data.get("human_note"),
            memory_insight=data.get("memory_insight")
        )
        
        # Append to memory history
        history_record = {
            "patient_id": data.get("patient_id"),
            "scenario_signature": {
                "primary_bottleneck": data.get("patient_data", {}).get("primary_discharge_bottleneck", "None"),
                "readmission_risk_level": data.get("model_outputs", {}).get("readmission_risk_level", "Low"),
                "delay_risk_level": data.get("model_outputs", {}).get("delay_risk_level", "Low"),
                "discharge_destination": data.get("patient_data", {}).get("discharge_destination", "Home"),
                "home_support_level": data.get("patient_data", {}).get("home_support_level", "Good"),
                "bed_occupancy_percent": data.get("patient_data", {}).get("current_bed_occupancy_percent", 80),
                "ed_boarding_count": data.get("patient_data", {}).get("ed_boarding_count", 0)
            },
            "model_outputs": data.get("model_outputs"),
            "research_outputs": data.get("research_outputs"),
            "committee_recommendation": data.get("committee_recommendation"),
            "human_decision": data.get("human_decision"),
            "outcome_proxy": "Unknown",
            "memory_reasoning": "Appended from human decision."
        }
        append_memory_history(history_record)
        
        return jsonify({"status": "success", "record": record})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/audit_log", methods=["GET"])
def audit():
    return jsonify(get_audit_log())

if __name__ == "__main__":
    app.run(port=5005)
