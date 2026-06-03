USE housing_db;

INSERT INTO country (country_id, country_name, country_code) VALUES
(1, 'Belgium', 'BE'),
(2, 'Bulgaria', 'BG'),
(3, 'Czechia', 'CZ'),
(4, 'Denmark', 'DK'),
(5, 'Germany', 'DE'),
(6, 'Estonia', 'EE'),
(7, 'Ireland', 'IE'),
(8, 'Greece', 'EL'),
(9, 'Spain', 'ES'),
(10, 'France', 'FR'),
(11, 'Croatia', 'HR'),
(12, 'Italy', 'IT'),
(13, 'Cyprus', 'CY'),
(14, 'Latvia', 'LV'),
(15, 'Lithuania', 'LT'),
(16, 'Luxembourg', 'LU'),
(17, 'Hungary', 'HU'),
(18, 'Netherlands', 'NL'),
(19, 'Austria', 'AT'),
(20, 'Poland', 'PL'),
(21, 'Portugal', 'PT'),
(22, 'Romania', 'RO'),
(23, 'Slovenia', 'SI'),
(24, 'Slovakia', 'SK'),
(25, 'Finland', 'FI'),
(26, 'Sweden', 'SE'),
(27, 'Iceland', 'IS'),
(28, 'Norway', 'NO'),
(29, 'Switzerland', 'CH'),
(30, 'United Kingdom', 'UK'),
(31, 'Montenegro', 'ME'),
(32, 'North Macedonia', 'MK'),
(33, 'Albania', 'AL'),
(34, 'Serbia', 'RS'),
(35, 'Turkiye', 'TR'),
(36, 'Kosovo', 'XK');

INSERT INTO social_indicator_types (sit_id, name) VALUES
(1, 'Pollution'),
(2, 'Crime, Violence, and Vandalism'),
(3, 'Poverty'),
(4, 'Overcrowding'),
(5, 'Noise'),
(6, 'House Price Index'),
(7, 'Under-occupied');




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


INSERT INTO reviews (review_id, listing_id, rating, comment) VALUES
(1, 1, 5, 'Great location and very affordable!'),
(2, 1, 4, 'Close to the university but a bit noisy at night.'),
(3, 2, 3, 'Decent place but the price is a bit high for the area.'),
(4, 3, 4, 'Spacious apartment with good amenities.'),
(5, 4, 2, 'Not well-maintained and had some issues with plumbing.');

INSERT INTO funding (funding_id, country_id, year, amount, program, agency) VALUES
(1, 1, 2023, 500000.00, 'Affordable Housing Initiative', 'Belgian Housing Agency'),
(2, 2, 2023, 300000.00, 'Student Housing Support', 'Bulgarian Ministry of Education'),
(3, 3, 2023, 400000.00, 'University Housing Grant', 'Czech Ministry of Education'),
(4, 4, 2023, 600000.00, 'Housing for Students Program', 'Danish Ministry of Higher Education'),
(5, 5, 2023, 700000.00, 'Affordable Housing Fund', 'German Federal Ministry of Housing');