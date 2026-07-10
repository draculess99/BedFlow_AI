import json
import os
import datetime

AUDIT_LOG_PATH = "database/audit_log.json"

def init_audit_log():
    if not os.path.exists(AUDIT_LOG_PATH):
        os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
        with open(AUDIT_LOG_PATH, "w") as f:
            json.dump([], f, indent=4)

def log_human_decision(patient_id, model_outputs, research_outputs, committee_rec, human_decision, human_note, memory_insight):
    init_audit_log()
    record = {
        "timestamp": str(datetime.datetime.now()),
        "patient_id": patient_id,
        "model_outputs": model_outputs,
        "research_outputs": research_outputs,
        "committee_recommendation": committee_rec,
        "human_decision": human_decision,
        "human_note": human_note,
        "risk_level": model_outputs.get("delay_risk_level", "Unknown"),
        "bed_capacity_impact": research_outputs.get("bed_capacity", {}).get("bed_pressure_level", "Unknown"),
        "memory_insight": memory_insight
    }
    
    with open(AUDIT_LOG_PATH, "r") as f:
        log = json.load(f)
        
    log.append(record)
    
    with open(AUDIT_LOG_PATH, "w") as f:
        json.dump(log, f, indent=4)
        
    return record

def get_audit_log():
    init_audit_log()
    with open(AUDIT_LOG_PATH, "r") as f:
        return json.load(f)
