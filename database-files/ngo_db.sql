DROP DATABASE IF EXISTS ngo_db;
CREATE DATABASE IF NOT EXISTS ngo_db;

USE ngo_db;


CREATE TABLE IF NOT EXISTS WorldNGOs (
    NGO_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    Founding_Year INTEGER,
    Focus_Area VARCHAR(100),
    Website VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Projects (
    Project_ID INT AUTO_INCREMENT PRIMARY KEY,
    Project_Name VARCHAR(255) NOT NULL,
    Focus_Area VARCHAR(100),
    Budget DECIMAL(15, 2),
    NGO_ID INT,
    Start_Date DATE,
    End_Date DATE,
    FOREIGN KEY (NGO_ID) REFERENCES WorldNGOs(NGO_ID)
);

CREATE TABLE IF NOT EXISTS Donors (
    Donor_ID INT AUTO_INCREMENT PRIMARY KEY,
    Donor_Name VARCHAR(255) NOT NULL,
    Donor_Type ENUM('Individual', 'Organization') NOT NULL,
    Donation_Amount DECIMAL(15, 2),
    NGO_ID INT,
    FOREIGN KEY (NGO_ID) REFERENCES WorldNGOs(NGO_ID)
);

INSERT INTO WorldNGOs (Name, Country, Founding_Year, Focus_Area, Website)
VALUES
('World Wildlife Fund', 'United States', 1961, 'Environmental Conservation', 'https://www.worldwildlife.org'),
('Doctors Without Borders', 'France', 1971, 'Medical Relief', 'https://www.msf.org'),
('Oxfam International', 'United Kingdom', 1995, 'Poverty and Inequality', 'https://www.oxfam.org'),
('Amnesty International', 'United Kingdom', 1961, 'Human Rights', 'https://www.amnesty.org'),
('Save the Children', 'United States', 1919, 'Child Welfare', 'https://www.savethechildren.org'),
('Greenpeace', 'Netherlands', 1971, 'Environmental Protection', 'https://www.greenpeace.org'),
('International Red Cross', 'Switzerland', 1863, 'Humanitarian Aid', 'https://www.icrc.org'),
('CARE International', 'Switzerland', 1945, 'Global Poverty', 'https://www.care-international.org'),
('Habitat for Humanity', 'United States', 1976, 'Affordable Housing', 'https://www.habitat.org'),
('Plan International', 'United Kingdom', 1937, 'Child Rights', 'https://plan-international.org');

INSERT INTO Projects (Project_Name, Focus_Area, Budget, NGO_ID, Start_Date, End_Date)
VALUES
('Save the Amazon', 'Environmental Conservation', 5000000.00, 1, '2022-01-01', '2024-12-31'),
('Emergency Medical Aid in Syria', 'Medical Relief', 3000000.00, 2, '2023-03-01', '2023-12-31'),
('Education for All', 'Poverty and Inequality', 2000000.00, 3, '2021-06-01', '2025-05-31'),
('Human Rights Advocacy in Asia', 'Human Rights', 1500000.00, 4, '2022-09-01', '2023-08-31'),
('Child Nutrition Program', 'Child Welfare', 2500000.00, 5, '2022-01-01', '2024-01-01');

INSERT INTO Donors (Donor_Name, Donor_Type, Donation_Amount, NGO_ID)
VALUES
('Bill & Melinda Gates Foundation', 'Organization', 10000000.00, 1),
('Elon Musk', 'Individual', 5000000.00, 2),
('Google.org', 'Organization', 2000000.00, 3),
('Open Society Foundations', 'Organization', 3000000.00, 4),
('Anonymous Philanthropist', 'Individual', 1000000.00, 5);

CREATE TABLE model1_params (
    sequence_number INT,
    beta_vals TEXT
);

INSERT INTO model1_params (sequence_number, beta_vals) VALUES
(1, '[0.25, 0.45, 0.67]');



CREATE TABLE country (
    country_id INTEGER PRIMARY KEY
    country_name VARCHAR(30) NOT NULL
);

CREATE TABLE social_indicator_types (
    sit_id INTEGER PRIMARY KEY
    name VARCHAR(100) NOT NULL
);

CREATE TABLE social_indicator_types (
    stats_id INTEGER PRIMARY KEY
    country_id INTEGER NOT NULL
    sit_id INTEGER NOT NULL
    year YEAR 
    value DECIMAL
    unit VARCHAR(50)

    CONSTRAINT fk_sis_country FOREIGN KEY (country_id) REFERENCES country (country_id)
    CONSTRAINT fk_sis_sit FOREIGN KEY (sit_id) REFERENCES social_indicator_types (sit_id)
);

INSERT INTO social_indicator_types (sit_id, name) VALUES
(1, 'Pollution')
(2, 'Crime')
(3, 'Poverty')
(4, 'Overcrowding')
(5, 'Noise')
(6, 'House Price Index')
(7, 'Under-occupied');


CREATE TABLE university (
    university_id INTEGER PRIMARY KEY
    country_id INTEGER NOT NULL
    university_name VARCHAR(75) NOT NULL
    city_name VARCHAR(30)
    address VARCHAR(250)

    CONSTRAINT fk_uni_country FOREIGN KEY (country_id) REFERENCES country (country_id)
)

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY
    university_id INTEGER
    country_id INTEGER
    name VARCHAR(100)
    role VARCHAR(50)
    email VARCHAR(100) UNIQUE
    max_budget DECIMAL
    max_distance_km DECIMAL

    CONSTRAINT fk_user_country FOREIGN KEY (country_id) REFERENCES country (country_id)
    CONSTRAINT fk_user_uni FOREIGN KEY (university_id) REFERENCES university (university_id)
)


CREATE TABLE listing (
    listing_id INTEGER PRIMARY KEY
    country_id INTEGER
    associated_university_id INTEGER
    user_id INTEGER
    price DECIMAL
    property_type VARCHAR(50)
    city_name VARCHAR(50)

    CONSTRAINT fk_listing_country FOREIGN KEY (country_id) REFERENCES country (country_id)
    CONSTRAINT fk_listing_uni FOREIGN KEY (associated_university_id) REFERENCES university (university_id)
    CONSTRAINT fk_listing_user FOREIGN KEY (user_id) REFERENCES user (user_id)
)

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY
    listing_id INTEGER NOT NULL
    rating INTEGER
    comment VARCHAR(2000)

    CONSTRAINT fk_reviews_listing FOREIGN KEY (listing_id) REFERENCES listing (listing_id)
)

CREATE TABLE funding (
    funding_id INTEGER PRIMARY KEY
    country_id INTEGER NOT NULL
    year YEAR
    amount DECIMAL
    program VARCHAR(100)
    agency VARCHAR(100)

    CONSTRAINT fk_funding_country FOREIGN KEY (country_id) REFERENCES country (country_id)
)