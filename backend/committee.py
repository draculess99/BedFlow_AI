import json
from .research_modules import run_all_modules
from .memory import get_memory_state, find_similar_bedflow_events

def run_committee(patient_data, model_outputs):
    research_outputs = run_all_modules(patient_data, model_outputs)
    
    # 1. Retrieve similar events for memory insight
    scenario = {
        "primary_bottleneck": patient_data.get("primary_discharge_bottleneck", "None"),
        "readmission_risk_level": model_outputs.get("readmission_risk_level", "Low"),
        "delay_risk_level": model_outputs.get("delay_risk_level", "Low"),
        "discharge_destination": patient_data.get("discharge_destination", "Home"),
        "home_support_level": patient_data.get("home_support_level", "Good"),
        "bed_occupancy_percent": patient_data.get("current_bed_occupancy_percent", 80),
        "ed_boarding_count": patient_data.get("ed_boarding_count", 0)
    }
    
    similar_events = find_similar_bedflow_events({"scenario_signature": scenario})
    if similar_events:
        memory_insight = f"Found {len(similar_events)} similar prior cases. "
        actions = [ev.get("committee_recommendation", "") for ev in similar_events]
        memory_insight += f"Common prior recommendations included: {', '.join(set(actions))}."
    else:
        memory_insight = "No closely matching prior bed-flow memory event was found."

    # 2. Formulate AI Committee Recommendation
    action_plan = []
    final_rec = "Proceed with routine discharge preparation"
    human_review = True # Always True
    
    safety = research_outputs["safety"]["patient_safety_level"]
    delay_risk = model_outputs["delay_risk_level"]
    
    if safety == "Critical":
        final_rec = "Hold discharge for safety"
        action_plan.append("MD review required due to clinical instability.")
    elif safety == "High":
        final_rec = "Case manager review required"
        action_plan.append("Lock in post-discharge support before proceeding.")
    else:
        if delay_risk in ["High", "Critical"]:
            # Check bottlenecks
            if research_outputs["rehab"]["placement_pressure_level"] in ["High", "Critical"]:
                final_rec = "Rehab placement escalation required"
                action_plan.append("Escalate SNF/Rehab placement to case manager.")
            elif research_outputs["insurance"]["insurance_pressure_level"] in ["High", "Critical"]:
                final_rec = "Insurance authorization escalation required"
                action_plan.append("Urgent UM review for auth.")
            elif research_outputs["pharmacy"]["pharmacy_pressure_level"] in ["High", "Critical"]:
                final_rec = "Pharmacy escalation required"
                action_plan.append("Prioritize MedRec for this patient.")
            elif research_outputs["transport"]["transport_pressure_level"] in ["High", "Critical"]:
                final_rec = "Transport escalation required"
                action_plan.append("Confirm EMS/family ETA.")
            elif research_outputs["home_care"]["home_care_pressure_level"] in ["High", "Critical"]:
                final_rec = "Home-care setup required"
                action_plan.append("Expedite home health agency intake.")
            else:
                final_rec = "Escalate bottleneck"
                action_plan.append("General delay risk flagged, review case.")
        else:
            final_rec = "Expedite discharge workflow after human review."
            action_plan.append("Clear remaining minor tasks.")

    return {
        "final_recommendation": final_rec,
        "risk_summary": {
            "delay_risk": delay_risk,
            "readmission_risk": model_outputs["readmission_risk_level"],
            "safety_level": safety
        },
        "primary_bottleneck": patient_data.get("primary_discharge_bottleneck", "None"),
        "action_plan": action_plan,
        "bed_capacity_impact": research_outputs["bed_capacity"],
        "human_review_required": human_review,
        "memory_insight": memory_insight,
        "audit_reasoning": f"Based on {safety} safety, {delay_risk} delay risk.",
        "research_outputs": research_outputs
    }
