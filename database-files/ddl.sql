
CREATE DATABASE IF NOT EXISTS ramm_lobbying;
USE ramm_lobbying;
 
CREATE TABLE IF NOT EXISTS country (
    country_code    VARCHAR(10)     PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    region          VARCHAR(100),
    income_group    VARCHAR(100),
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
 
CREATE TABLE IF NOT EXISTS country_indicator (
    indicator_id    INTEGER         PRIMARY KEY,
    country_code    VARCHAR(10)     NOT NULL,
    year            INTEGER         NOT NULL,
    gdp_usd         FLOAT,
    population      INTEGER,
    inflation_rate  FLOAT,
    source          VARCHAR(255),
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (country_code) REFERENCES country(country_code)
);
 
CREATE TABLE IF NOT EXISTS industry (
    industry_id     INTEGER         PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
 
CREATE TABLE IF NOT EXISTS policy_area (
    policy_area_id  INTEGER         PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    description     VARCHAR(10000),
    tags            VARCHAR(255),
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
 
CREATE TABLE IF NOT EXISTS app_user (
    user_id         INTEGER         PRIMARY KEY,
    email           VARCHAR(255)    NOT NULL,
    password_hash   VARCHAR(255)    NOT NULL,
    role            VARCHAR(100),
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
 
CREATE TABLE IF NOT EXISTS organization (
    org_id                  INTEGER         PRIMARY KEY,
    name                    VARCHAR(255)    NOT NULL,
    lobbyfacts_url          VARCHAR(500),
    members_eu              INTEGER,
    members_fte             INTEGER,
    lobbying_cost           FLOAT,
    log_lobbying_cost       FLOAT,
    interest_represented    VARCHAR(255),
    country_code            VARCHAR(10),
    industry_id             INTEGER,
    created_at              DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (country_code) REFERENCES country(country_code),
    FOREIGN KEY (industry_id) REFERENCES industry(industry_id)
);
 
CREATE TABLE IF NOT EXISTS lobbying_activity (
    activity_id     INTEGER         PRIMARY KEY,
    org_id          INTEGER         NOT NULL,
    policy_area_id  INTEGER         NOT NULL,
    eu_institution  VARCHAR(255),
    activity_type   VARCHAR(100),
    description     VARCHAR(10000),
    source          VARCHAR(255),
    start_date      DATE,
    end_date        DATE,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organization(org_id),
    FOREIGN KEY (policy_area_id) REFERENCES policy_area(policy_area_id)
);
 
CREATE TABLE IF NOT EXISTS expenditure_record (
    expenditure_id          INTEGER         PRIMARY KEY,
    org_id                  INTEGER         NOT NULL,
    policy_area_id          INTEGER,
    year                    INTEGER         NOT NULL,
    amount_eur              FLOAT,
    amount_range_min_eur    FLOAT,
    amount_range_max_eur    FLOAT,
    currency                VARCHAR(20),
    source                  VARCHAR(255),
    created_at              DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organization(org_id),
    FOREIGN KEY (policy_area_id) REFERENCES policy_area(policy_area_id)
);
 
CREATE TABLE IF NOT EXISTS meeting (
    meeting_id      INTEGER         PRIMARY KEY,
    org_id          INTEGER         NOT NULL,
    eu_body         VARCHAR(255),
    meeting_date    DATE,
    subject         VARCHAR(10000),
    attendees_count INTEGER,
    source          VARCHAR(255),
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organization(org_id)
);
 
CREATE TABLE IF NOT EXISTS access_pass (
    pass_id         INTEGER         PRIMARY KEY,
    org_id          INTEGER         NOT NULL,
    person_name     VARCHAR(255),
    role_title      VARCHAR(255),
    eu_body         VARCHAR(255),
    issue_date      DATE,
    expiry_date     DATE,
    source          VARCHAR(255),
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organization(org_id)
);
 
CREATE TABLE IF NOT EXISTS lobby_model_weights (
    model_id        INTEGER         PRIMARY KEY,
    beta_vals       TEXT            NOT NULL
);

CREATE TABLE IF NOT EXISTS lobby_model_scaler (
    sequence_number INT,
    feature_means   TEXT,   -- e.g. "[74.32, 0.0106]"
    feature_stds    TEXT    -- e.g. "[1.85, 0.00092]"
);
 
CREATE TABLE IF NOT EXISTS influence_prediction (
    prediction_id       INTEGER         PRIMARY KEY,
    org_id              INTEGER         NOT NULL,
    policy_area_id      INTEGER,
    model_id            INTEGER,
    run_date            DATE,
    influence_score     FLOAT,
    influence_class     VARCHAR(100),
    top_features_json   VARCHAR(10000),
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organization(org_id),
    FOREIGN KEY (policy_area_id) REFERENCES policy_area(policy_area_id),
    FOREIGN KEY (model_id) REFERENCES lobby_model_weights(model_id)
);
 
CREATE TABLE IF NOT EXISTS saved_query_export (
    export_id       INTEGER         PRIMARY KEY,
    user_id         INTEGER         NOT NULL,
    query_json      VARCHAR(10000),
    file_format     VARCHAR(50),
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES app_user(user_id)
);

-- Insertions
INSERT INTO lobby_model_weights (model_id, beta_vals) VALUES
(123, '[-0.00470672  0.61737005  0.06048751  1.0781912  -1.06305793  0.1429552]');

INSERT INTO lobby_model_scaler (sequence_number, feature_means, feature_stds) VALUES
(1, '[  8.30994891   1.15619662 359.0225555    2.59393102 484.52407528
   1.68052178]', '[5.07376641e+00 1.50773957e+00 2.34243942e+03 2.18585360e+01
 3.12590236e+04 5.41726502e-01]');