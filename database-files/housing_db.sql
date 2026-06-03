DROP DATABASE IF EXISTS housin_db;
CREATE DATABASE IF NOT EXISTS housing_db;
USE housing_db;

CREATE TABLE country (
    country_id INTEGER PRIMARY KEY,
    country_name VARCHAR(30) NOT NULL
);

INSERT INTO country (country_id, country_name) VALUES
(1, 'Belgium'),
(2, 'Bulgaria'),
(3, 'Czechia'),
(4, 'Denmark'),
(5, 'Germany'),
(6, 'Estonia'),
(7, 'Ireland'),
(8, 'Greece'),
(9, 'Spain'),
(10, 'France'),
(11, 'Croatia'),
(12, 'Italy'),
(13, 'Cyprus'),
(14, 'Latvia'),
(15, 'Lithuania'),
(16, 'Luxembourg'),
(17, 'Hungary'),
(18, 'Netherlands'),
(19, 'Austria'),
(20, 'Poland'),
(21, 'Portugal'),
(22, 'Romania'),
(23, 'Slovenia'),
(24, 'Slovakia'),
(25, 'Finland'),
(26, 'Sweden'),
(27, 'Iceland'),
(28, 'Norway'),
(29, 'Switzerland'),
(30, 'United Kingdom'),
(31, 'Montenegro'),
(32, 'North Macedonia'),
(33, 'Albania'),
(34, 'Serbia'),
(35, 'Turkiye'),
(36, 'Konsovo');


CREATE TABLE social_indicator_types (
    sit_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE social_indicator_stats (
    stats_id INTEGER PRIMARY KEY,
    country_id INTEGER NOT NULL,
    sit_id INTEGER NOT NULL,
    year YEAR,
    value DECIMAL,
    unit VARCHAR(50),

    CONSTRAINT fk_sis_country FOREIGN KEY (country_id) REFERENCES country (country_id),
    CONSTRAINT fk_sis_sit FOREIGN KEY (sit_id) REFERENCES social_indicator_types (sit_id)
);

INSERT INTO social_indicator_types (sit_id, name) VALUES
(1, 'Pollution'),
(2, 'Crime, Violence, and Vandalism'),
(3, 'Poverty'),
(4, 'Overcrowding'),
(5, 'Noise'),
(6, 'House Price Index'),
(7, 'Under-occupied');


CREATE TABLE university (
    university_id INTEGER PRIMARY KEY,
    country_id INTEGER NOT NULL,
    university_name VARCHAR(75) NOT NULL,
    city_name VARCHAR(30),
    address VARCHAR(250),

    CONSTRAINT fk_uni_country FOREIGN KEY (country_id) REFERENCES country (country_id)
);

INSERT INTO university (university_id, country_id, university_name, city_name, address) VALUES
(1, 1, 'KU Leuven', 'Leuven', 'Oude Markt 13, 3000 Leuven, Belgium'),
(2, 1, 'Ghent University', 'Ghent', 'Sint-Pietersnieuwstraat 25, 9000 Ghent, Belgium'),
(3, 1, 'Université catholique de Louvain', 'Louvain-la-Neuve', 'Place de lUniversité 1, 1348 Louvain-la-Neuve, Belgium'),
(4, 2, 'Sofia University', 'Sofia', '15 Tsar Osvoboditel Blvd, Sofia 1504, Bulgaria'),
(5, 2, 'Plovdiv University', 'Plovdiv', '24 Tsar Asen St, Plovdiv 4000, Bulgaria'),
(6, 3, 'Charles University', 'Prague', 'Ovocný trh 5, 116 36 Praha 1, Czechia'),
(7, 3, 'Czech Technical University in Prague', 'Prague', 'Zikova 4, 166 36 Praha 6, Czechia'),
(8, 4, 'University of Copenhagen', 'Copenhagen', 'Nørregade 10, 1165 København K, Denmark'),
(9, 4, 'Aarhus University', 'Aarhus', 'Nordre Ringgade 1, 8000 Aarhus C, Denmark'),
(10, 5, 'Technical University of Munich', 'Munich', 'Arcisstraße 21, 80333 München, Germany');

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


INSERT INTO user (user_id, university_id, country_id, name, role, email, max_budget, max_distance_km) VALUES
(1, 1, 7, 'Seamus Coyne', 'Student', 'coyne.s@gmail.com', 1000, 10),
(2, 2, 10, 'Nicole Stekol', 'Student', 'stekol.n@gmail.com', 750, 8),
(3, 3, 22, 'Lauryn Gong', 'Student', 'gong.l@gmail.com', 500, 15);

INSERT INTO user (user_id, country_id, name, role, email) VALUES
(4, 25, 'Stevoon Sparkle', 'Real Estate Agent', 'sparkles@realestate.com'),
(5, 31, 'Petar Pintar', 'Real Estate Agent', 'pintarp@realestate.com'),
(6, 29, 'Elise Wisemann', 'Real Estate Agent', 'wisemanne@realestate.com'),
(7, 12, 'Beth Lepore', 'Government Agency', 'leporeb@org.gov'),
(8, 21, 'Susan Thatch', 'Government Agency', 'thatchs@org.gov'),
(9, 13, 'George Igoe', 'Government Agency', 'igoeg@org.gov');


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

INSERT INTO listing (listing_id, country_id, associated_university_id, user_id, price, property_type, city_name) VALUES
(1, 1, 1, 1, 500.00, 'Apartment', 'Leuven'),
(2, 1, 2, 2, 450.00, 'Studio', 'Ghent'),
(3, 1, 3, 3, 550.00, 'Apartment', 'Louvain-la-Neuve'),
(4, 2, 4, 4, 400.00, 'Apartment', 'Sofia'),
(5, 2, 5, 5, 350.00, 'Studio', 'Plovdiv'),
(6, 3, 6, 6, 600.00, 'Apartment', 'Prague'),
(7, 3, 7, 7, 650.00, 'Apartment', 'Prague'),
(8, 4, 8, 8, 700.00, 'Apartment', 'Copenhagen'),
(9, 4, 9, 9, 750.00, 'Apartment', 'Aarhus');

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    listing_id INTEGER NOT NULL,
    rating INTEGER,
    comment VARCHAR(2000),

    CONSTRAINT fk_reviews_listing FOREIGN KEY (listing_id) REFERENCES listing (listing_id)
);

INSERT INTO reviews (review_id, listing_id, rating, comment) VALUES
(1, 1, 5, 'Great location and very affordable!'),
(2, 1, 4, 'Close to the university but a bit noisy at night.'),
(3, 2, 3, 'Decent place but the price is a bit high for the area.'),
(4, 3, 4, 'Spacious apartment with good amenities.'),
(5, 4, 2, 'Not well-maintained and had some issues with plumbing.');

CREATE TABLE funding (
    funding_id INTEGER PRIMARY KEY,
    country_id INTEGER NOT NULL,
    year YEAR,
    amount DECIMAL,
    program VARCHAR(100),
    agency VARCHAR(100),

    CONSTRAINT fk_funding_country FOREIGN KEY (country_id) REFERENCES country (country_id)
);

INSERT INTO funding (funding_id, country_id, year, amount, program, agency) VALUES
(1, 1, 2023, 500000.00, 'Affordable Housing Initiative', 'Belgian Housing Agency'),
(2, 2, 2023, 300000.00, 'Student Housing Support', 'Bulgarian Ministry of Education'),
(3, 3, 2023, 400000.00, 'University Housing Grant', 'Czech Ministry of Education'),
(4, 4, 2023, 600000.00, 'Housing for Students Program', 'Danish Ministry of Higher Education'),
(5, 5, 2023, 700000.00, 'Affordable Housing Fund', 'German Federal Ministry of Housing');