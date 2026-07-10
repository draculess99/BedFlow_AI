import json
import os
import datetime

STATE_PATH = "database/bedflow_memory_state.json"
HISTORY_PATH = "database/bedflow_memory_history.json"

def init_memory():
    if not os.path.exists(STATE_PATH):
        os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
        default_state = {
            "recent_avg_discharge_delay_hours": 0.0,
            "recent_readmission_risk_trend": "stable",
            "most_common_bottleneck": "None",
            "recent_bed_recovery_count": 0,
            "last_recommendation": "None",
            "last_updated": str(datetime.datetime.now()),
            "memory_reasoning": "Initial state"
        }
        with open(STATE_PATH, "w") as f:
            json.dump(default_state, f, indent=4)
            
    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "w") as f:
            json.dump([], f, indent=4)

def get_memory_state():
    init_memory()
    with open(STATE_PATH, "r") as f:
        return json.load(f)

def update_memory_state(updates):
    state = get_memory_state()
    state.update(updates)
    state["last_updated"] = str(datetime.datetime.now())
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=4)
    return state

def append_memory_history(record):
    init_memory()
    record["timestamp"] = str(datetime.datetime.now())
    with open(HISTORY_PATH, "r") as f:
        history = json.load(f)
    history.append(record)
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=4)

def find_similar_bedflow_events(current_case, top_k=3):
    init_memory()
    with open(HISTORY_PATH, "r") as f:
        history = json.load(f)
        
    if not history:
        return []
        
    # Simple matching based on matching keys in scenario_signature
    scored_history = []
    curr_sig = current_case.get("scenario_signature", {})
    
    for event in history:
        score = 0
        ev_sig = event.get("scenario_signature", {})
        
        if ev_sig.get("primary_bottleneck") == curr_sig.get("primary_bottleneck"): score += 3
        if ev_sig.get("readmission_risk_level") == curr_sig.get("readmission_risk_level"): score += 2
        if ev_sig.get("delay_risk_level") == curr_sig.get("delay_risk_level"): score += 2
        if ev_sig.get("discharge_destination") == curr_sig.get("discharge_destination"): score += 1
        
        scored_history.append((score, event))
        
    scored_history.sort(key=lambda x: x[0], reverse=True)
    return [ev for score, ev in scored_history[:top_k] if score > 0]
