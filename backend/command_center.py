"""Hospital command-center helpers for BedFlow AI.

Stage 1 turns the original single-patient demo into a hospital-style
operations dashboard. These helpers deliberately avoid model inference so the
command center loads quickly. The queue uses operational proxy fields that are
already present in the synthetic BedFlow dataset.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd


UNIT_CAPACITY = {
    "Emergency Department": 40,
    "ICU": 20,
    "Telemetry": 35,
    "Med/Surg": 80,
    "Oncology": 25,
    "Orthopedics": 30,
}

RISK_ORDER = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}

OWNER_BY_BOTTLENECK = {
    "Clinical Stability": "Physician",
    "Doctor": "Physician",
    "Home Care": "Case Manager",
    "Insurance": "Utilization Management",
    "None": "Bed Manager",
    "Pharmacy": "Pharmacy",
    "Rehab/SNF": "Case Manager",
    "Transport": "Transport",
}

NEXT_ACTION_BY_BOTTLENECK = {
    "Clinical Stability": "Request physician safety review",
    "Doctor": "Request discharge order/sign-off",
    "Home Care": "Confirm home-health agency and support plan",
    "Insurance": "Escalate authorization with payer/UM team",
    "None": "Progress routine discharge workflow",
    "Pharmacy": "Prioritize medication reconciliation",
    "Rehab/SNF": "Escalate facility placement or bed confirmation",
    "Transport": "Confirm transport or family pickup ETA",
}


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _risk_badge(level: str) -> str:
    badges = {
        "Critical": "🔴 Critical",
        "High": "🟠 High",
        "Medium": "🟡 Medium",
        "Low": "🟢 Low",
    }
    return badges.get(level, level)


def infer_unit(row: pd.Series | dict[str, Any]) -> str:
    """Infer a hospital unit from the available demo fields.

    The dataset does not contain a real unit/ward column, so this creates a
    realistic operational proxy for the command-center screen.
    """
    diagnosis = str(row.get("diagnosis_group", "General Medicine"))
    acuity = str(row.get("acuity_level", "Medium"))

    if acuity == "High" and diagnosis in {"Cardiology", "Pulmonology", "Neurology"}:
        return "ICU"
    if diagnosis in {"Cardiology", "Pulmonology", "Neurology"}:
        return "Telemetry"
    if diagnosis == "Oncology":
        return "Oncology"
    if diagnosis == "Orthopedics":
        return "Orthopedics"
    return "Med/Surg"


def pressure_level_from_occupancy(occupancy_percent: float, ed_boarders: int = 0) -> str:
    if occupancy_percent >= 95 or ed_boarders > 10:
        return "Critical"
    if occupancy_percent >= 85 or ed_boarders >= 6:
        return "High"
    if occupancy_percent >= 75:
        return "Medium"
    return "Low"


def estimate_delay_risk(row: pd.Series | dict[str, Any]) -> str:
    hours = _to_float(row.get("expected_discharge_delay_hours", 0))
    delayed = _to_int(row.get("delayed_discharge", 0))
    occ = _to_float(row.get("current_bed_occupancy_percent", 80))
    boarders = _to_int(row.get("ed_boarding_count", 0))
    bottleneck = str(row.get("primary_discharge_bottleneck", "None"))

    if hours >= 16 or (delayed and occ >= 95 and boarders > 10):
        return "Critical"
    if delayed or hours >= 8 or bottleneck in {"Insurance", "Rehab/SNF", "Clinical Stability"}:
        return "High"
    if hours >= 4 or bottleneck not in {"None", ""}:
        return "Medium"
    return "Low"


def estimate_readmission_risk(row: pd.Series | dict[str, Any]) -> str:
    readmitted = _to_int(row.get("readmitted_30_days", 0))
    prior_readmits = _to_int(row.get("prior_readmissions_12mo", 0))
    prior_admissions = _to_int(row.get("prior_admissions_6mo", 0))
    meds = _to_int(row.get("medication_count", 0))
    labs = str(row.get("lab_stability_flag", "Stable"))
    vitals = str(row.get("vital_sign_stability_flag", "Stable"))

    if labs == "Unstable" or vitals == "Unstable" or (readmitted and prior_readmits >= 2):
        return "Critical"
    if readmitted or prior_readmits >= 2 or prior_admissions >= 4 or meds >= 15:
        return "High"
    if prior_readmits == 1 or prior_admissions >= 2 or meds >= 8:
        return "Medium"
    return "Low"


def bottleneck_owner(bottleneck: str) -> str:
    return OWNER_BY_BOTTLENECK.get(str(bottleneck), "Bed Manager")


def bottleneck_next_action(bottleneck: str) -> str:
    return NEXT_ACTION_BY_BOTTLENECK.get(str(bottleneck), "Review discharge plan")


def estimate_case_status(row: pd.Series | dict[str, Any], delay_risk: str, readmission_risk: str) -> str:
    bottleneck = str(row.get("primary_discharge_bottleneck", "None"))
    if delay_risk == "Critical" or readmission_risk == "Critical":
        return "Escalate Now"
    if bottleneck not in {"None", ""} and delay_risk in {"High", "Critical"}:
        return "Blocked"
    if delay_risk == "Medium" or readmission_risk == "Medium":
        return "Needs Review"
    return "Ready / Routine"


def bed_recovery_score(row: pd.Series | dict[str, Any], delay_risk: str, readmission_risk: str) -> float:
    hours = _to_float(row.get("expected_discharge_delay_hours", 0))
    occ = _to_float(row.get("current_bed_occupancy_percent", 80))
    boarders = _to_int(row.get("ed_boarding_count", 0))
    bottleneck = str(row.get("primary_discharge_bottleneck", "None"))

    score = 0.0
    score += min(hours, 24) * 1.7
    score += max(0.0, occ - 75) * 0.9
    score += min(boarders, 20) * 1.2
    score += RISK_ORDER.get(delay_risk, 1) * 8
    score += RISK_ORDER.get(readmission_risk, 1) * 4
    if bottleneck != "None":
        score += 10
    if bottleneck in {"Insurance", "Rehab/SNF", "Clinical Stability"}:
        score += 8
    return round(score, 1)


def build_discharge_queue(df: pd.DataFrame, limit: int | None = None) -> list[dict[str, Any]]:
    """Build a prioritized multi-patient queue for the command center."""
    if df.empty:
        return []

    records: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        unit = infer_unit(row)
        delay_risk = estimate_delay_risk(row)
        readmission_risk = estimate_readmission_risk(row)
        bottleneck = str(row.get("primary_discharge_bottleneck", "None"))
        status = estimate_case_status(row, delay_risk, readmission_risk)
        score = bed_recovery_score(row, delay_risk, readmission_risk)
        delay_hours = round(_to_float(row.get("expected_discharge_delay_hours", 0)), 1)

        records.append(
            {
                "patient_id": str(row.get("patient_id", "")),
                "unit": unit,
                "age": _to_int(row.get("age", 0)),
                "diagnosis_group": str(row.get("diagnosis_group", "Unknown")),
                "acuity_level": str(row.get("acuity_level", "Unknown")),
                "discharge_destination": str(row.get("discharge_destination", "Unknown")),
                "delay_risk_level": delay_risk,
                "delay_risk_display": _risk_badge(delay_risk),
                "readmission_risk_level": readmission_risk,
                "readmission_risk_display": _risk_badge(readmission_risk),
                "predicted_delay_hours_proxy": delay_hours,
                "primary_bottleneck": bottleneck,
                "owner_role": bottleneck_owner(bottleneck),
                "case_status": status,
                "next_action": bottleneck_next_action(bottleneck),
                "bed_recovery_score": score,
                "current_bed_occupancy_percent": _to_int(row.get("current_bed_occupancy_percent", 0)),
                "ed_boarding_count": _to_int(row.get("ed_boarding_count", 0)),
            }
        )

    records.sort(key=lambda item: item["bed_recovery_score"], reverse=True)
    if limit is not None:
        return records[:limit]
    return records


def build_hospital_capacity_snapshot(df: pd.DataFrame) -> dict[str, Any]:
    """Create hospital-wide and unit-level capacity KPIs."""
    if df.empty:
        return {
            "snapshot_time_utc": datetime.now(timezone.utc).isoformat(),
            "total_beds": sum(UNIT_CAPACITY.values()),
            "occupied_beds": 0,
            "available_beds": sum(UNIT_CAPACITY.values()),
            "occupancy_percent": 0,
            "beds_pending_cleaning": 0,
            "ed_boarders": 0,
            "expected_discharges_today": 0,
            "delayed_discharges": 0,
            "critical_delay_cases": 0,
            "units": [],
        }

    working = df.copy()
    working["unit"] = working.apply(infer_unit, axis=1)
    working["delay_risk_level"] = working.apply(estimate_delay_risk, axis=1)

    units: list[dict[str, Any]] = []

    # Emergency Department is displayed as its own pressure row. It is derived
    # from ED-boarder pressure fields, not from an inpatient ward assignment.
    ed_boarders = int(round(float(working["ed_boarding_count"].quantile(0.75)))) if "ed_boarding_count" in working else 0
    ed_occupied = min(UNIT_CAPACITY["Emergency Department"], max(0, 28 + ed_boarders))
    ed_available = max(0, UNIT_CAPACITY["Emergency Department"] - ed_occupied)
    ed_occ = round((ed_occupied / UNIT_CAPACITY["Emergency Department"]) * 100, 1)
    units.append(
        {
            "unit": "Emergency Department",
            "total_beds": UNIT_CAPACITY["Emergency Department"],
            "occupied_beds": ed_occupied,
            "available_beds": ed_available,
            "occupancy_percent": ed_occ,
            "pending_discharges": 0,
            "delayed_discharges": 0,
            "ed_boarders": ed_boarders,
            "pressure_level": pressure_level_from_occupancy(ed_occ, ed_boarders),
        }
    )

    for unit, bed_count in UNIT_CAPACITY.items():
        if unit == "Emergency Department":
            continue

        group = working[working["unit"] == unit]
        if group.empty:
            occupancy = 70.0
            delayed_rate = 0.0
            expected_ready_rate = 0.0
        else:
            occupancy = round(float(group["current_bed_occupancy_percent"].mean()), 1)
            delayed_rate = float(group["delayed_discharge"].mean()) if "delayed_discharge" in group else 0.0
            expected_ready_rate = float((group["expected_discharge_delay_hours"] <= 6).mean()) if "expected_discharge_delay_hours" in group else 0.0

        occupied = min(bed_count, max(0, int(round(bed_count * occupancy / 100))))
        available = max(0, bed_count - occupied)
        pending_discharges = max(0, int(round(occupied * expected_ready_rate * 0.35)))
        delayed_discharges = max(0, int(round(occupied * delayed_rate * 0.25)))
        unit_boarders = max(0, int(round(ed_boarders * (occupied / max(1, sum(UNIT_CAPACITY.values()))))))

        units.append(
            {
                "unit": unit,
                "total_beds": bed_count,
                "occupied_beds": occupied,
                "available_beds": available,
                "occupancy_percent": occupancy,
                "pending_discharges": pending_discharges,
                "delayed_discharges": delayed_discharges,
                "ed_boarders": unit_boarders,
                "pressure_level": pressure_level_from_occupancy(occupancy, unit_boarders),
            }
        )

    total_beds = sum(unit["total_beds"] for unit in units)
    occupied_beds = sum(unit["occupied_beds"] for unit in units)
    available_beds = sum(unit["available_beds"] for unit in units)
    expected_discharges = sum(unit["pending_discharges"] for unit in units)
    delayed_discharges = sum(unit["delayed_discharges"] for unit in units)
    critical_delay_cases = int((working["delay_risk_level"] == "Critical").sum())
    beds_pending_cleaning = max(1, min(12, int(round(expected_discharges * 0.25))))

    return {
        "snapshot_time_utc": datetime.now(timezone.utc).isoformat(),
        "total_beds": total_beds,
        "occupied_beds": occupied_beds,
        "available_beds": available_beds,
        "occupancy_percent": round((occupied_beds / total_beds) * 100, 1) if total_beds else 0,
        "beds_pending_cleaning": beds_pending_cleaning,
        "ed_boarders": ed_boarders,
        "expected_discharges_today": expected_discharges,
        "delayed_discharges": delayed_discharges,
        "critical_delay_cases": critical_delay_cases,
        "units": units,
    }
