import streamlit as st
import pandas as pd
import requests
import json
import os

API_URL = "http://localhost:5005/api"

st.set_page_config(page_title="BedFlow AI", layout="wide", initial_sidebar_state="collapsed")

# Minimal CSS enhancements (relying on config.toml for primary dark theme)
st.markdown("""
<style>
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Make metrics text a bit softer */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #ff5252 !important;
    }
    
    /* Smooth tabs */
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏥 BedFlow AI: Agentic Discharge Planning")
st.markdown("### *AI-Powered Readmission Risk & Discharge Delay Predictor*")

# Tabs
tabs = st.tabs([
    "Control Tower", 
    "Model Performance", 
    "Memory & Audit Log", 
    "Data & Limitations"
])

def load_patients():
    try:
        res = requests.get(f"{API_URL}/demo_patients")
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")
    return []

# Tab 1: Control Tower (Main Workflow)
with tabs[0]:
    st.header("Discharge Readiness & Bed Recovery")
    
    patients = load_patients()
    if not patients:
        st.warning("No patients found. Please ensure the backend is running and data is generated.")
    else:
        patient_ids = [p["patient_id"] for p in patients]
        selected_id = st.selectbox("Select Patient to Review", patient_ids)
        
        patient_data = next((p for p in patients if p["patient_id"] == selected_id), None)
        
        if patient_data:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Patient Context")
                st.write(f"**Age**: {patient_data['age']}")
                st.write(f"**Diagnosis**: {patient_data['diagnosis_group']}")
                st.write(f"**Acuity**: {patient_data['acuity_level']}")
                st.write(f"**Discharge Dest**: {patient_data['discharge_destination']}")
                st.write(f"**Bed Occupancy**: {patient_data['current_bed_occupancy_percent']}%")
                st.write(f"**ED Boarding Count**: {patient_data['ed_boarding_count']}")
                
            with col2:
                st.subheader("Run AI Analysis")
                if st.button("Evaluate Patient Case"):
                    with st.spinner("Analyzing models and running AI committee..."):
                        # 1. Predict
                        pred_res = requests.post(f"{API_URL}/predict_patient", json=patient_data)
                        if pred_res.status_code == 200:
                            model_outputs = pred_res.json()
                            st.session_state["model_outputs"] = model_outputs
                            
                            # 2. Run Committee
                            comm_payload = {
                                "patient_data": patient_data,
                                "model_outputs": model_outputs
                            }
                            comm_res = requests.post(f"{API_URL}/run_committee", json=comm_payload)
                            if comm_res.status_code == 200:
                                st.session_state["committee_result"] = comm_res.json()
                                
            # Display Results if available
            if "committee_result" in st.session_state and "model_outputs" in st.session_state:
                res = st.session_state["committee_result"]
                outs = st.session_state["model_outputs"]
                
                st.divider()
                st.subheader("AI Decision Support Outputs")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Discharge Delay Risk", outs["delay_risk_level"], f"{outs['discharge_delay_risk_probability']:.2f} prob")
                c2.metric("Readmission Risk", outs["readmission_risk_level"], f"{outs['readmission_risk_probability']:.2f} prob")
                c3.metric("Expected Delay", f"{outs['predicted_delay_hours']} hrs")
                
                st.markdown(f"**Primary Bottleneck**: {res['primary_bottleneck']}")
                st.markdown(f"**Bed Capacity Impact**: {res['bed_capacity_impact']['estimated_bed_recovery_value']}")
                
                st.info(f"**Memory Insight**: {res['memory_insight']}")
                
                st.warning(f"**Final Recommendation**: {res['final_recommendation']}")
                
                st.markdown("**Action Plan:**")
                for act in res['action_plan']:
                    st.write(f"- {act}")
                    
                st.divider()
                st.subheader("Human-in-the-Loop Review")
                human_dec = st.selectbox("Action", ["Approve", "Override", "Escalate to Case Manager", "Hold"])
                human_note = st.text_area("Supervisor Note")
                
                if st.button("Save Decision to Audit Log"):
                    audit_payload = {
                        "patient_id": selected_id,
                        "patient_data": patient_data,
                        "model_outputs": outs,
                        "research_outputs": res["research_outputs"],
                        "committee_recommendation": res["final_recommendation"],
                        "human_decision": human_dec,
                        "human_note": human_note,
                        "memory_insight": res["memory_insight"]
                    }
                    save_res = requests.post(f"{API_URL}/save_human_decision", json=audit_payload)
                    if save_res.status_code == 200:
                        st.success("Decision saved successfully.")
                        # Clear session state for next patient
                        del st.session_state["committee_result"]
                        del st.session_state["model_outputs"]
                        st.rerun()

# Tab 2: Model Performance
with tabs[1]:
    st.header("Predictive Models vs Baselines")
    st.write("XGBoost must outperform simple baselines to prove it learns operational patterns.")
    if st.button("Refresh / Train Models"):
        with st.spinner("Training models..."):
            requests.post(f"{API_URL}/train_models")
            st.success("Models trained.")
            
    try:
        metrics_res = requests.get(f"{API_URL}/model_metrics")
        if metrics_res.status_code == 200:
            metrics = metrics_res.json()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Discharge Delay Risk")
                st.json(metrics["discharge_delay"])
                
            with col2:
                st.subheader("Readmission Risk")
                st.json(metrics["readmission_risk"])
                
            st.subheader("Expected Delay Hours")
            st.json(metrics["expected_delay_hours"])
    except:
        st.write("No metrics available. Train models first.")

# Tab 3: Memory & Audit Log
with tabs[2]:
    st.header("System Memory and Audit Log")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current State")
        try:
            mem_res = requests.get(f"{API_URL}/memory_state")
            if mem_res.status_code == 200:
                st.json(mem_res.json())
        except:
            st.write("Failed to load memory state")
            
    with col2:
        st.subheader("Audit Log")
        try:
            audit_res = requests.get(f"{API_URL}/audit_log")
            if audit_res.status_code == 200:
                logs = audit_res.json()
                for log in reversed(logs):
                    st.write(f"**{log['timestamp']} - {log['patient_id']}**")
                    st.write(f"AI Rec: {log['committee_recommendation']}")
                    st.write(f"Human: {log['human_decision']} ({log['human_note']})")
                    st.divider()
        except:
            st.write("Failed to load audit log")

# Tab 4: Limitations
with tabs[3]:
    st.header("Data Sources and Limitations")
    st.write("""
    **Important Notice**:
    - This application uses completely **synthetic/proxy data**.
    - No Protected Health Information (PHI) or real patient records are used.
    - The research modules are synthetic/proxy operational modules built for decision-support demonstration.
    - They are not validated clinical models and do not use real patient data.
    - The AI committee provides **decision support only**.
    - It **does not automatically discharge patients**. Human review is strictly required before any action is taken.
    """)
