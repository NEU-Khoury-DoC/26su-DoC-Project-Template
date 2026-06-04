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
(1, '[17.163229086853594, -4.055617680655049, 0.032384733797264253, 4.116760058805894, -0.8009490520006273, -3.1509773479122125, 4.191915297758115, -0.3750841997263201, -0.5665241526828857, 0.8150943283928452, 2.207429622564287, 0.2649283873577718, 4.532692168114665, 9.479853634509423, -0.42092919735955603, -0.7224790962825944, -3.9309960356306908, -2.364547518935558, 0.41239683568005264, 7.306797499887298, 0.802204956374758, 5.552764093861776, 12.078772678327395, -3.159998007794143, -2.5813282878838133, 0.49520489645019333, 5.082705673425818, -0.8502386891934479, 7.655095021732872, 1.8280543077882234, -0.015658330744076843, 9.606932730884814, 4.557016104085569, -4.873948787100378]');

-- To rescale, need to save the means and std of features
CREATE TABLE IF NOT EXISTS price_scaler (
    sequence_number INT,
    feature_means   TEXT,   -- e.g. "[74.32, 0.0106]"
    feature_stds    TEXT    -- e.g. "[1.85, 0.00092]"
);

INSERT INTO price_scaler (sequence_number, feature_means, feature_stds) VALUES
(1, '[11.863803408037972, 714.1319948186527, 18.892370466321243, 18.171386010362692, 556134.2881217618]',
    '[3.3872679353610713, 214.8250034285889, 6.512089590267215, 6.270133748497953, 348318.1698134389]');

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