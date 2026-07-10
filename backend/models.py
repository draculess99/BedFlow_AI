import json
import os
import pandas as pd
from xgboost import XGBClassifier, XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, mean_absolute_error, mean_squared_error, r2_score
import numpy as np

DATA_PATH = "database/bedflow_patient_data.csv"
METRICS_PATH = "database/model_metrics.json"

class BedFlowModels:
    def __init__(self):
        self.delay_clf = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        self.readmission_clf = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        self.hours_reg = XGBRegressor()
        self.is_trained = False
        self.feature_columns = []
        
    def train_models(self):
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run data generator first.")
            
        df = pd.read_csv(DATA_PATH, keep_default_na=False)
        
        # Preprocessing (simple encoding for synthetic data)
        categorical_cols = ["diagnosis_group", "acuity_level", "mobility_status", "home_support_level", "discharge_destination", "lab_stability_flag", "vital_sign_stability_flag", "ed_wait_time_pressure", "medication_complexity"]
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        
        # Features and targets
        drop_cols = ["patient_id", "delayed_discharge", "readmitted_30_days", "expected_discharge_delay_hours", "primary_discharge_bottleneck"]
        X = df_encoded.drop(columns=[col for col in drop_cols if col in df_encoded.columns])
        self.feature_columns = list(X.columns)
        
        y_delay = df_encoded["delayed_discharge"]
        y_readmit = df_encoded["readmitted_30_days"]
        y_hours = df_encoded["expected_discharge_delay_hours"]
        
        metrics = {}
        
        # 1. Discharge Delay Risk Model
        X_train, X_test, y_train, y_test = train_test_split(X, y_delay, test_size=0.2, random_state=42)
        self.delay_clf.fit(X_train, y_train)
        y_pred = self.delay_clf.predict(X_test)
        y_pred_proba = self.delay_clf.predict_proba(X_test)[:, 1]
        
        # Baseline: Majority Class
        majority_class = y_train.mode()[0]
        y_base = [majority_class] * len(y_test)
        
        metrics["discharge_delay"] = {
            "xgboost": {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, zero_division=0),
                "recall": recall_score(y_test, y_pred, zero_division=0),
                "f1": f1_score(y_test, y_pred, zero_division=0),
                "roc_auc": roc_auc_score(y_test, y_pred_proba)
            },
            "baseline": {
                "accuracy": accuracy_score(y_test, y_base),
                "precision": precision_score(y_test, y_base, zero_division=0),
                "recall": recall_score(y_test, y_base, zero_division=0),
                "f1": f1_score(y_test, y_base, zero_division=0)
            }
        }
        
        # 2. Readmission Risk Model
        X_train, X_test, y_train, y_test = train_test_split(X, y_readmit, test_size=0.2, random_state=42)
        self.readmission_clf.fit(X_train, y_train)
        y_pred = self.readmission_clf.predict(X_test)
        y_pred_proba = self.readmission_clf.predict_proba(X_test)[:, 1]
        
        majority_class = y_train.mode()[0]
        y_base = [majority_class] * len(y_test)
        
        metrics["readmission_risk"] = {
            "xgboost": {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, zero_division=0),
                "recall": recall_score(y_test, y_pred, zero_division=0),
                "f1": f1_score(y_test, y_pred, zero_division=0),
                "roc_auc": roc_auc_score(y_test, y_pred_proba)
            },
            "baseline": {
                "accuracy": accuracy_score(y_test, y_base),
                "precision": precision_score(y_test, y_base, zero_division=0),
                "recall": recall_score(y_test, y_base, zero_division=0),
                "f1": f1_score(y_test, y_base, zero_division=0)
            }
        }
        
        # 3. Expected Delay Hours
        X_train, X_test, y_train, y_test = train_test_split(X, y_hours, test_size=0.2, random_state=42)
        self.hours_reg.fit(X_train, y_train)
        y_pred = self.hours_reg.predict(X_test)
        
        # Baseline: Median
        median_val = y_train.median()
        y_base = [median_val] * len(y_test)
        
        metrics["expected_delay_hours"] = {
            "xgboost": {
                "mae": mean_absolute_error(y_test, y_pred),
                "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
                "r2": r2_score(y_test, y_pred)
            },
            "baseline": {
                "mae": mean_absolute_error(y_test, y_base),
                "rmse": np.sqrt(mean_squared_error(y_test, y_base)),
                "r2": r2_score(y_test, y_base)
            }
        }
        
        # Save metrics
        os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
        with open(METRICS_PATH, "w") as f:
            json.dump(metrics, f, indent=4)
            
        self.is_trained = True
        return metrics

    def get_risk_level(self, prob):
        if prob < 0.2: return "Low"
        if prob < 0.5: return "Medium"
        if prob < 0.8: return "High"
        return "Critical"

    def predict_patient(self, patient_data: dict):
        if not self.is_trained:
            self.train_models()
            
        df = pd.DataFrame([patient_data])
        categorical_cols = ["diagnosis_group", "acuity_level", "mobility_status", "home_support_level", "discharge_destination", "lab_stability_flag", "vital_sign_stability_flag", "ed_wait_time_pressure", "medication_complexity"]
        
        # Reconstruct dummy columns
        for col in categorical_cols:
            if col in df.columns:
                val = df[col].iloc[0]
                dummy_col = f"{col}_{val}"
                df[dummy_col] = 1
                df.drop(columns=[col], inplace=True)
                
        # Fill missing columns that were in training data
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
                
        X = df[self.feature_columns]
        
        delay_prob = float(self.delay_clf.predict_proba(X)[0][1])
        readmit_prob = float(self.readmission_clf.predict_proba(X)[0][1])
        hours_pred = max(0, float(self.hours_reg.predict(X)[0]))
        
        return {
            "discharge_delay_risk_probability": delay_prob,
            "delay_risk_level": self.get_risk_level(delay_prob),
            "readmission_risk_probability": readmit_prob,
            "readmission_risk_level": self.get_risk_level(readmit_prob),
            "predicted_delay_hours": round(hours_pred, 1)
        }

# Singleton instance
bedflow_models = BedFlowModels()
