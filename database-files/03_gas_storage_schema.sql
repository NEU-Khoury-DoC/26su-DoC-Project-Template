-- =============================================================
-- GAS STORAGE — journalist pages (Country Snapshot, Comparison, Risk)
-- Daily rows: seed from datasets/apsi/agsi_clean.csv via
--   docker compose exec api python scripts/seed_gas_storage.py
-- Winter rows: seed from app/src/assets/dataset.csv (same script)
-- Model inference uses api/backend/ml_models/gas_model.pkl (not retrained from DB)
-- =============================================================

USE ngo_db;

CREATE TABLE IF NOT EXISTS gas_storage_daily (
    storage_id     BIGINT       NOT NULL AUTO_INCREMENT,
    country_code   CHAR(2)      NOT NULL,
    gas_day        DATE         NOT NULL,
    full_pct       DECIMAL(6, 2) NOT NULL,
    gas_in_storage DECIMAL(12, 4),
    trend          DECIMAL(8, 2),
    CONSTRAINT pk_gas_storage_daily PRIMARY KEY (storage_id),
    CONSTRAINT uq_gas_storage_daily_country_day UNIQUE (country_code, gas_day),
    INDEX idx_gas_storage_daily_country_day (country_code, gas_day)
);

-- storage_at_start / storage_trend_30d / storage_volatility must stay DOUBLE —
-- DECIMAL(8,2) rounding would change gas_model.pkl predictions.
CREATE TABLE IF NOT EXISTS gas_storage_winters (
    winter_id          INT          NOT NULL AUTO_INCREMENT,
    country_code       CHAR(2)      NOT NULL,
    winter_year        SMALLINT     NOT NULL,
    min_winter_full    DECIMAL(6, 2) NOT NULL,
    days               INT,
    storage_stress     TINYINT      NOT NULL,
    storage_at_start   DOUBLE       NOT NULL,
    storage_trend_30d  DOUBLE       NOT NULL,
    storage_volatility DOUBLE       NOT NULL,
    CONSTRAINT pk_gas_storage_winters PRIMARY KEY (winter_id),
    CONSTRAINT uq_gas_storage_winters_country_year UNIQUE (country_code, winter_year),
    INDEX idx_gas_storage_winters_country (country_code)
);
