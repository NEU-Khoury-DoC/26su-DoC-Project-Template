-- =============================================================
-- GAS STORAGE — journalist pages (Country Snapshot, Comparison, Risk)
-- Daily + winter rows: 06_gas_storage_data.sql (loaded on db init)
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

-- Logistic regression weights (features: storage_at_start, storage_trend_30d, storage_volatility, vol_x_start)
-- vol_x_start is the interaction term storage_at_start * storage_volatility
-- Source: datasets/apsi/apsi.ipynb — logreg.fit(X, y) on all winter rows
-- Inputs are standardized at prediction time: x_scaled = (x - mean) / std
CREATE TABLE IF NOT EXISTS gas_storage_model (
    model_id                   INT    NOT NULL,
    intercept                  DOUBLE NOT NULL,
    weight_storage_at_start    DOUBLE NOT NULL,
    weight_storage_trend_30d   DOUBLE NOT NULL,
    weight_storage_volatility  DOUBLE NOT NULL,
    weight_vol_x_start         DOUBLE NOT NULL,
    mean_storage_at_start      DOUBLE NOT NULL,
    mean_storage_trend_30d     DOUBLE NOT NULL,
    mean_storage_volatility    DOUBLE NOT NULL,
    mean_vol_x_start           DOUBLE NOT NULL,
    std_storage_at_start       DOUBLE NOT NULL,
    std_storage_trend_30d      DOUBLE NOT NULL,
    std_storage_volatility     DOUBLE NOT NULL,
    std_vol_x_start            DOUBLE NOT NULL,
    CONSTRAINT pk_gas_storage_model PRIMARY KEY (model_id)
);

INSERT INTO gas_storage_model (
    model_id, intercept,
    weight_storage_at_start, weight_storage_trend_30d, weight_storage_volatility, weight_vol_x_start,
    mean_storage_at_start, mean_storage_trend_30d, mean_storage_volatility, mean_vol_x_start,
    std_storage_at_start, std_storage_trend_30d, std_storage_volatility, std_vol_x_start
) VALUES (
    1,
    -0.004441541811143235,
    -0.6820174064981015,
    -0.40200831065688064,
    -0.010932891829800194,
    0.017385439403829923,
    88.6093914559721,
    2.5504864864864865,
    8.61439122200191,
    761.9049563164259,
    12.702145281437595,
    4.853537053066873,
    4.154950755150775,
    383.08865405235053
);

