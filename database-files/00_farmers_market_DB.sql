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
    post_text VARCHAR(255),
    img BLOB,
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

CREATE TABLE IF NOT EXISTS user_crop_data (
    user_crop_data_id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT,
    type_of_crop VARCHAR(255) NOT NULL,
    season VARCHAR(100) NOT NULL,
    sown DATETIME NOT NULL,
    harvested DATETIME NOT NULL,
    water_source VARCHAR(100) NOT NULL,
    temp FLOAT NOT NULL,
    relative_humidity FLOAT NOT NULL,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(farm_id)
);


-- not sure if we need this yet
-- CREATE TABLE IF NOT EXISTS ml_crop_data (
--     user_crop_data_id INT AUTO_INCREMENT PRIMARY KEY,
--     temperature FLOAT,
--     humidity FLOAT,
--     elevation FLOAT,
--     rainfall FLOAT,
--     created_by VARCHAR(100) NOT NULL,
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
--     updated_by VARCHAR(100) DEFAULT NULL,
--     updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
-- );

CREATE TABLE IF NOT EXISTS crop_price_model_coefficients (
    crops_price_coe_id INT AUTO_INCREMENT PRIMARY KEY,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
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
    graph BLOB,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (saved_data_id) REFERENCES saved_data(saved_data_id)
);