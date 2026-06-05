-- =============================================================
-- GAS STORAGE — journalist pages (Country Snapshot, Comparison, Risk)
-- Daily rows: seed from datasets/apsi/agsi_clean.csv via
--   docker compose exec api python scripts/seed_gas_storage.py
-- Winter rows: seed from datasets/apsi/dataset.csv (same script)
-- Model weights: INSERT below (from datasets/apsi/apsi.ipynb LogisticRegression fit)
-- =============================================================

USE Zeus;

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
-- DECIMAL rounding would change logistic-regression predictions.
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

-- Logistic regression weights (features: storage_at_start, storage_trend_30d, storage_volatility)
-- Source: datasets/apsi/apsi.ipynb — logreg.fit(X, y) on all winter rows
CREATE TABLE IF NOT EXISTS gas_storage_model (
    model_id                   INT    NOT NULL,
    intercept                  DOUBLE NOT NULL,
    weight_storage_at_start    DOUBLE NOT NULL,
    weight_storage_trend_30d   DOUBLE NOT NULL,
    weight_storage_volatility  DOUBLE NOT NULL,
    CONSTRAINT pk_gas_storage_model PRIMARY KEY (model_id)
);

INSERT INTO gas_storage_model (
    model_id, intercept, weight_storage_at_start,
    weight_storage_trend_30d, weight_storage_volatility
) VALUES (
    1,
    -0.01364296582364657,
    -0.776213,
    -0.374907,
    -0.127339
);
