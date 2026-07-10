import os
import sys

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import bedflow_models
from backend.api import app
from backend.committee import run_committee
from backend.memory import init_memory, get_memory_state, append_memory_history

def test_imports():
    print("Imports successful.")
    
def test_dataset():
    assert os.path.exists("database/bedflow_patient_data.csv"), "Dataset not found"
    print("Dataset check passed.")
    
def test_models():
    metrics = bedflow_models.train_models()
    assert "discharge_delay" in metrics
    assert "readmission_risk" in metrics
    assert "expected_delay_hours" in metrics
    assert os.path.exists("database/model_metrics.json")
    print("Model training and metrics check passed.")

def test_committee():
    # Mock prediction
    sample_patient = {
        "patient_id": "TEST001",
        "diagnosis_group": "Cardiology",
        "acuity_level": "Medium",
        "mobility_status": "Independent",
        "home_support_level": "Good",
        "discharge_destination": "Home",
        "lab_stability_flag": "Stable",
        "vital_sign_stability_flag": "Stable",
        "ed_wait_time_pressure": "Medium",
        "medication_complexity": "Low",
        "primary_discharge_bottleneck": "Pharmacy"
    }
    preds = bedflow_models.predict_patient(sample_patient)
    result = run_committee(sample_patient, preds)
    assert "final_recommendation" in result
    print("Committee logic check passed.")

def test_memory():
    init_memory()
    state = get_memory_state()
    assert "recent_avg_discharge_delay_hours" in state
    
    append_memory_history({
        "test": "event",
        "scenario_signature": {"primary_bottleneck": "Pharmacy"}
    })
    print("Memory check passed.")

if __name__ == "__main__":
    print("Starting smoke tests...")
    test_imports()
    test_dataset()
    test_models()
    test_committee()
    test_memory()
    print("All smoke tests passed!")
