DROP DATABASE IF EXISTS farmers_market_db;
CREATE DATABASE IF NOT EXISTS farmers_market_db;

USE farmers_market_db;

CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    user_type ENUM('farmer', 'politician', 'researcher') NOT NULL,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    text VARCHAR(255),
    img CHAR(64),
    user_id INT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    texts VARCHAR(255),
    post_id INT,
    user_id INT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);

CREATE TABLE IF NOT EXISTS Reactions (
    reaction_id INT AUTO_INCREMENT PRIMARY KEY,
    pos_neg BOOLEAN,
    post_id INT,
    user_id INT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);

CREATE TABLE IF NOT EXISTS Farms (
    farm_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    user_id INT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS FarmsData (
    farm_data_id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT,
    longitude FLOAT,
    latitude FLOAT,
    country VARCHAR(50),
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES Farms(farm_id)
);

CREATE TABLE IF NOT EXISTS Crops (
    crop_id INT AUTO_INCREMENT PRIMARY KEY,
    crop_name VARCHAR(50),
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS crop_list (
    farm_data_id INT NOT NULL,
    crop_id INT NOT NULL,
    PRIMARY KEY (farm_data_id, crop_id),
    FOREIGN KEY (farm_data_id) REFERENCES FarmsData(farm_data_id),
    FOREIGN KEY (crop_id) REFERENCES Crops(crop_id)
);

CREATE TABLE IF NOT EXISTS (
    ideal_data_id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT,
    temperature FLOAT,
    humidity FLOAT,
    elevation FLOAT,
    rainfall FLOAT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES Farms(farm_id)
);

CREATE TABLE IF NOT EXISTS cropPriceModelCoefficients (
    crops_price_coe_id INT AUTO_INCREMENT PRIMARY KEY,
    crop_id INT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES Crops(crop_id)
);

CREATE TABLE IF NOT EXISTS cropHealthModelCoefficients (
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

CREATE TABLE IF NOT EXISTS savedData (
    saved_data_id INT AUTO_INCREMENT PRIMARY KEY,
    saved_data TEXT,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS savedGraphs (
    saved_graph_id INT AUTO_INCREMENT PRIMARY KEY,
    saved_data_id INT,
    graph CHAR(64),
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (saved_data_id) REFERENCES savedData(saved_data_id)
);

CREATE TABLE IF NOT EXISTS savedReports (
    saved_report_id INT AUTO_INCREMENT PRIMARY KEY,
    saved_data_id INT,
    title VARCHAR(255),
    texts TEXT,
    graph CHAR(64),
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100) DEFAULT NULL,
    updated_at DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (saved_data_id) REFERENCES savedData(saved_data_id)
);