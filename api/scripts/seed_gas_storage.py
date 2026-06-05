#!/usr/bin/env python3
"""
Load AGSI daily storage and winter feature rows into MySQL.

Run once after the db container is up and schema files have been applied:
    docker compose exec api python scripts/seed_gas_storage.py

Source CSVs (notebook outputs in datasets/apsi — seed only):
    datasets/apsi/agsi_clean.csv
    datasets/apsi/dataset.csv
"""

import csv
import os
import sys
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

API_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = API_ROOT.parent
AGSI_CSV = Path(os.getenv(
    "AGSI_CSV",
    REPO_ROOT / "datasets" / "apsi" / "agsi_clean.csv",
))
WINTERS_CSV = Path(os.getenv(
    "WINTERS_CSV",
    REPO_ROOT / "datasets" / "apsi" / "dataset.csv",
))

# Fallback when running inside the API container (/datasets mount)
if not AGSI_CSV.is_file():
    AGSI_CSV = Path("/datasets/apsi/agsi_clean.csv")
if not WINTERS_CSV.is_file():
    WINTERS_CSV = Path("/datasets/apsi/dataset.csv")
BATCH_SIZE = 2000


def _optional_float(value):
    if value is None:
        return None
    text = str(value).strip()
    if text in ("", "-", "NA", "N/A"):
        return None
    return float(text)


def get_connection():
    load_dotenv(API_ROOT / ".env")
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database=os.getenv("DB_NAME", "ngo_db"),
        port=int(os.getenv("DB_PORT", "3306")),
    )


def seed_daily_storage(cursor):
    if not AGSI_CSV.is_file():
        raise FileNotFoundError(f"Missing AGSI CSV: {AGSI_CSV}")

    cursor.execute("SELECT COUNT(*) AS n FROM gas_storage_daily")
    if cursor.fetchone()["n"]:
        print("gas_storage_daily already seeded — skipping")
        return

    insert_sql = """
        INSERT INTO gas_storage_daily
            (country_code, gas_day, full_pct, gas_in_storage, trend)
        VALUES (%s, %s, %s, %s, %s)
    """
    batch = []
    total = 0

    with AGSI_CSV.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            batch.append((
                row["country"].strip().upper(),
                row["gasDayStart"].strip(),
                float(row["full"]),
                _optional_float(row["gasInStorage"]),
                _optional_float(row["trend"]),
            ))
            if len(batch) >= BATCH_SIZE:
                cursor.executemany(insert_sql, batch)
                total += len(batch)
                batch.clear()
                print(f"  inserted {total} daily rows...", end="\r")

    if batch:
        cursor.executemany(insert_sql, batch)
        total += len(batch)

    print(f"Seeded gas_storage_daily: {total} rows")


def seed_winters(cursor):
    if not WINTERS_CSV.is_file():
        raise FileNotFoundError(f"Missing winters CSV: {WINTERS_CSV}")

    cursor.execute("SELECT COUNT(*) AS n FROM gas_storage_winters")
    if cursor.fetchone()["n"]:
        print("gas_storage_winters already seeded — skipping")
        return

    insert_sql = """
        INSERT INTO gas_storage_winters (
            country_code, winter_year, min_winter_full, days, storage_stress,
            storage_at_start, storage_trend_30d, storage_volatility
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    rows = []
    with WINTERS_CSV.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append((
                row["country"].strip().upper(),
                int(float(row["winter"])),
                float(row["min_winter_full"]),
                int(float(row["days"])) if row["days"] else None,
                int(row["storage_stress"]),
                float(row["storage_at_start"]),
                float(row["storage_trend_30d"]),
                float(row["storage_volatility"]),
            ))

    cursor.executemany(insert_sql, rows)
    print(f"Seeded gas_storage_winters: {len(rows)} rows")


def main():
    print("Seeding gas storage tables from datasets/apsi ...")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        seed_daily_storage(cursor)
        seed_winters(cursor)
        conn.commit()
        print("Done.")
    except Exception as exc:
        conn.rollback()
        print(f"Seed failed: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
