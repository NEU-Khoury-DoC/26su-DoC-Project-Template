DROP DATABASE IF EXISTS farmers_market_db;
CREATE DATABASE IF NOT EXISTS farmers_market_db;

USE farmers_market_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    user_type ENUM('farmer', 'politician', 'researcher') NOT NULL,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    text VARCHAR(255),
    img CHAR(64),
    user_id INT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    texts VARCHAR(255),
    post_id INT,
    user_id INT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE IF NOT EXISTS reactions (
    reaction_id INT AUTO_INCREMENT PRIMARY KEY,
    pos_neg BOOLEAN,
    post_id INT,
    user_id INT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE IF NOT EXISTS farms (
    farm_id INT AUTO_INCREMENT PRIMARY KEY,
    farm_name VARCHAR(255),
    user_id INT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS farms_location (
    farm_data_id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT,
    longitude FLOAT,
    latitude FLOAT,
    country VARCHAR(50),
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(farm_id)
);

CREATE TABLE IF NOT EXISTS crops (
    crop_id INT AUTO_INCREMENT PRIMARY KEY,
    crop_name VARCHAR(50),
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS farm_crops (
    farm_id INT NOT NULL,
    crop_id INT NOT NULL,
    PRIMARY KEY (farm_id, crop_id),
    FOREIGN KEY (farm_id) REFERENCES farms(farm_id),
    FOREIGN KEY (crop_id) REFERENCES crops(crop_id)
);

CREATE TABLE IF NOT EXISTS user_crop_data (
    user_crop_data_id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT,
    temperature FLOAT,
    humidity FLOAT,
    elevation FLOAT,
    rainfall FLOAT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(farm_id)
);

CREATE TABLE IF NOT EXISTS ml_crop_data (
    user_crop_data_id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    elevation FLOAT,
    rainfall FLOAT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS crop_price_model_coefficients (
    crops_price_coe_id INT AUTO_INCREMENT PRIMARY KEY,
    crop_id INT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES crops(crop_id)
);

-- Model 2 parameters: GDP ~ Fossil_Fuels + CO2_Upop
-- Fitted on the full Belgium dataset (HW2 Part 3.1)
-- beta_vals = [intercept, b_Fossil_Fuels, b_CO2_Upop]
CREATE TABLE IF NOT EXISTS price_params (
    sequence_number INT,
    beta_vals       TEXT
);

-- NOTE: These parameters are based on the scaled features
-- The user will be inputting the raw values, so:
-- will need to scale before applying model in function
INSERT INTO price_params (sequence_number, beta_vals) VALUES
(1, '[18.76528131992353, 0.4395023300115466, -0.36885073989100237, 2.2013231632126735, 1.1207381049347107, 0.7893850872270421, 1.1380283076380877, -0.5029495429645382, -0.634217890034992, 0.4531026091993922, -0.7455228115714604, 0.2604294999772836, -0.8312646887379568, 2.312233340578175, 0.23912872320678263, 2.445475529885603, 0.6322941558875317, 1.9072300650448335, 0.7714820957708662, 0.27915407588619584, -0.41015774794396703, 2.9761937178303413, 2.2376129005634344, -0.5137987914096419, -0.11740895031365493, 0.9592454876450357, 0.057426126820612655, -0.029147637632855636, -0.08816101068713166, -1.4931050994892154, 0.46370885814230445, -0.5263104766734047, -0.5781942817571771, 0.13040279857671594]');

-- To rescale, need to save the means and std of features
CREATE TABLE IF NOT EXISTS price_scaler (
    sequence_number INT,
    feature_means   TEXT,   -- e.g. "[74.32, 0.0106]"
    feature_stds    TEXT    -- e.g. "[1.85, 0.00092]"
);

INSERT INTO price_scaler (sequence_number, feature_means, feature_stds) VALUES
(1, '[12.553323235923022, 735.3423913043476, 590783.3555434782, 21.860760869565215, 30.296086956521737]',
    '[3.391847370608103, 223.72957581482527, 371975.20699760463, 5.3219948110556805, 6.851753973558719]');

CREATE TABLE IF NOT EXISTS CropPrices (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100),
    crop VARCHAR(100),
    year INT,
    selling_price FLOAT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS WeatherData (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100),
    year INT,
    temperature_2m_mean FLOAT,
    precipitation_sum FLOAT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS crop_health_model_coefficients (
    crops_health_coe_id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    elevation FLOAT,
    rainfall FLOAT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS saved_data (
    saved_data_id INT AUTO_INCREMENT PRIMARY KEY,
    saved_data TEXT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS saved_graphs (
    saved_graph_id INT AUTO_INCREMENT PRIMARY KEY,
    saved_data_id INT,
    graph CHAR(64),
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (saved_data_id) REFERENCES saved_data(saved_data_id)
);

CREATE TABLE IF NOT EXISTS saved_reports (
    saved_report_id INT AUTO_INCREMENT PRIMARY KEY,
    saved_data_id INT,
    title VARCHAR(255),
    texts TEXT,
    graph CHAR(64),
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (saved_data_id) REFERENCES saved_data(saved_data_id)
);