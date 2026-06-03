DROP DATABASE IF EXISTS housing_db;
CREATE DATABASE IF NOT EXISTS housing_db;
USE housing_db;

CREATE TABLE country (
    country_id INTEGER PRIMARY KEY,
    country_name VARCHAR(30) NOT NULL,
    country_code VARCHAR(10) NOT NULL
);

CREATE TABLE social_indicator_types (
    sit_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE social_indicator_stats (
    stats_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    country_id INTEGER NOT NULL,
    sit_id INTEGER NOT NULL,
    year YEAR,
    value DECIMAL,
    unit VARCHAR(50),

    CONSTRAINT fk_sis_country FOREIGN KEY (country_id) REFERENCES country (country_id),
    CONSTRAINT fk_sis_sit FOREIGN KEY (sit_id) REFERENCES social_indicator_types (sit_id)
);

CREATE TABLE university (
    university_id INTEGER PRIMARY KEY,
    country_id INTEGER NOT NULL,
    university_name VARCHAR(75) NOT NULL,
    city_name VARCHAR(30),
    address VARCHAR(250),

    CONSTRAINT fk_uni_country FOREIGN KEY (country_id) REFERENCES country (country_id)
);

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY,
    university_id INTEGER,
    country_id INTEGER,
    name VARCHAR(100),
    role VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    max_budget DECIMAL,
    max_distance_km DECIMAL,

    CONSTRAINT fk_user_country FOREIGN KEY (country_id) REFERENCES country (country_id),
    CONSTRAINT fk_user_uni FOREIGN KEY (university_id) REFERENCES university (university_id)
);

CREATE TABLE listing (
    listing_id INTEGER PRIMARY KEY,
    country_id INTEGER,
    associated_university_id INTEGER,
    user_id INTEGER,
    price DECIMAL,
    property_type VARCHAR(50),
    city_name VARCHAR(50),

    CONSTRAINT fk_listing_country FOREIGN KEY (country_id) REFERENCES country (country_id),
    CONSTRAINT fk_listing_uni FOREIGN KEY (associated_university_id) REFERENCES university (university_id),
    CONSTRAINT fk_listing_user FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    listing_id INTEGER NOT NULL,
    rating INTEGER,
    comment VARCHAR(2000),

    CONSTRAINT fk_reviews_listing FOREIGN KEY (listing_id) REFERENCES listing (listing_id)
);

CREATE TABLE funding (
    funding_id INTEGER PRIMARY KEY,
    country_id INTEGER NOT NULL,
    year YEAR,
    amount DECIMAL,
    program VARCHAR(100),
    agency VARCHAR(100),

    CONSTRAINT fk_funding_country FOREIGN KEY (country_id) REFERENCES country (country_id)
);
