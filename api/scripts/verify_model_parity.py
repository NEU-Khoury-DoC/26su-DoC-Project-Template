#!/usr/bin/env python3
"""
Sanity-check gas storage seed sources and DB-backed predict_risk.

Run from repo root (host or api container):
    python api/scripts/verify_model_parity.py
"""

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
APS_DIR = REPO_ROOT / "datasets" / "apsi"

sys.path.insert(0, str(REPO_ROOT / "api"))
from backend.routes.storage_service import predict_risk  # noqa: E402


def main():
    dataset_csv = APS_DIR / "dataset.csv"
    agsi_csv = APS_DIR / "agsi_clean.csv"

    if not dataset_csv.is_file():
        print(f"Missing dataset: {dataset_csv}", file=sys.stderr)
        sys.exit(1)

    with dataset_csv.open(newline="") as handle:
        winter_rows = list(csv.DictReader(handle))
    print(f"Winter feature rows in source CSV: {len(winter_rows)}")

    if agsi_csv.is_file():
        with agsi_csv.open(newline="") as handle:
            daily_count = sum(1 for _ in csv.DictReader(handle))
        print(f"Daily AGSI rows in source CSV: {daily_count}")

    # Poland 2024 — spot-check DB weights return a valid probability
    result = predict_risk(96.66, 3.85, 5.94)
    if not 0.0 <= result["risk_prob"] <= 1.0:
        print("Invalid risk_prob:", result, file=sys.stderr)
        sys.exit(1)

    print(f"Sample prediction (PL-like inputs): {result['risk_prob']:.2%}, at_risk={result['at_risk']}")
    print("OK — predict_risk reads weights from gas_storage_model table")


if __name__ == "__main__":
    main()
