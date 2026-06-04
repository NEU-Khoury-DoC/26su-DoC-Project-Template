USE housing_db;

-- Insert all countries which EuroStat data convers
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

-- The 7 datatypes covered with our EuroStat data
INSERT INTO social_indicator_types (sit_id, name) VALUES
(1, 'Pollution'),
(2, 'Crime, Violence, and Vandalism'),
(3, 'Poverty'),
(4, 'Overcrowding'),
(5, 'Noise'),
(6, 'House Price Index'),
(7, 'Under-occupied');


-- 50 Universities 
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (1,19,'Bowie State University','Vienna','8538 Becker Place');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (2,1,'Seattle Pacific University','Brussels','4546 Graceland Way');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (3,35,'Xinjiang University of Finance and Economics','Ankara','2 Main Center');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (4,22,'Omsk State Technical University','Bucharest','17733 Crowley Place');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (5,5,'Fasa Faculty of Medical Sciences','Berlin','3287 Gulseth Crossing');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (6,2,'Lahti Polytechnic','Sofia','7714 Fremont Plaza');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (7,14,'New York Chiropractic College','Riga','40976 Moland Center');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (8,33,'Ecole Nationale Supérieure de Chimie de Rennes','Tirana','2055 Sullivan Alley');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (9,15,'University Of Medical Sciences & Technology (UMST)','Vilnius','50846 Anthes Plaza');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (10,1,'Haigazian University','Brussels','93564 Emmet Pass');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (11,11,'Universiti Malaya','Zagreb','0101 Melby Way');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (12,19,'Moore College of Art and Design','Vienna','28446 Pennsylvania Hill');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (13,27,'Felician College','Reykjavik','059 Judy Road');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (14,18,'City University of New York, Medgar Evers College','Amsterdam','90 John Wall Terrace');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (15,6,'Universidad Politecnica de Nicaragua','Tallinn','0632 Graceland Avenue');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (16,1,'Babes-Bolyai University of Cluj-Napoca','Liege','80227 Debs Junction');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (17,2,'Bashkir State Medical University','Plovdiv','46 Tomscot Place');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (18,8,'University of St. Cyril and Methodius in Trnava','Athens','884 Lindbergh Hill');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (19,13,'Philosophisch-Theologische Hochschule der Salesianer Don Boscos','Nicosia','925 Holmberg Court');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (20,9,'Institute of Teachers Education, Darul Aman','Barcelona','1344 Bonner Way');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (21,14,'Université d''Antananarivo','Riga','4 Summit Circle');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (22,23,'Centennial University','Ljubljana','79 Brown Trail');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (23,2,'University of Fribourg','Sofia','62174 Thierer Way');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (24,3,'Mugla University','Prague','8882 Rusk Terrace');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (25,12,'Banasthali University','Rome','31 Arizona Alley');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (26,16,'North Dakota State University','Luxembourg City','27 Victoria Terrace');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (27,16,'MacMurray College','Luxembourg City','0 Ramsey Place');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (28,27,'East China Normal University','Reykjavik','11095 Esch Terrace');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (29,29,'Faculdade Italo Brasileira','Zurich','437 Sheridan Pass');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (30,12,'Athlone Institute of Technology','Milan','9034 Miller Street');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (31,18,'Trakia University Stara Zagora','Amsterdam','896 Fairfield Crossing');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (32,24,'University of Strathclyde','Bratislava','0 Lake View Court');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (33,8,'Nagoya University','Thessaloniki','2 Springs Road');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (34,6,'Katholische Universität Eichstätt','Tallinn','7 Trailsway Road');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (35,7,'Ecole Nationale Supérieure en Electrotechnique, Electronique, Informatique et Hydraulique de Toulouse','Dublin','536 Park Meadow Terrace');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (36,22,'Universitas Padjadjaran','Cluj-Napoca','5 Dahle Street');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (37,25,'Carroll College Waukesha','Helsinki','32068 Sauthoff Park');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (38,36,'Jingdezhen China Institute','Pristina','4630 Beilfuss Place');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (39,13,'Katholieke Hogeschool Kempen','Nicosia','584 Menomonie Crossing');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (40,14,'Virginia College','Jurmala','79 Cherokee Court');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (41,17,'Gujarat Technological University Ahmedabad','Budapest','83 Amoth Court');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (42,35,'Harvey Mudd College','Istanbul','92856 Schmedeman Pass');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (43,25,'The Federal Polytechnic Offa','Tampere','02003 Huxley Way');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (44,32,'The World Islamic Sciences & Education University','Skopje','512 Springview Trail');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (45,6,'Luzhou Medical College','Tartu','0045 Buhler Hill');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (46,19,'University of Applied Sciences Upper Austria','Linz','37988 Beilfuss Point');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (47,19,'Ecole Supérieure d''Electronique de l''Ouest','Graz','4782 Lotheville Point');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (48,4,'University of Peloponnese','Copenhagen','0 Corben Avenue');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (49,13,'Fundación Universitaria Manuela Beltrán','Limassol','85 Jana Drive');
INSERT INTO university(university_id,country_id,university_name,city_name,address) VALUES (50,30,'University of Rousse','London','556 Weeping Birch Point');


-- Real estate agents
INSERT INTO user(user_id,country_id,name,role,email) VALUES (6,28,'Sonnnie Tucker','Real Estate Agent','stucker5@amazon.co.uk');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (7,12,'Mimi Holtham','Real Estate Agent','mholtham6@home.pl');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (9,9,'Eva Macey','Real Estate Agent','emacey8@blogs.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (10,8,'Gretchen Sprackling','Real Estate Agent','gsprackling9@wunderground.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (11,35,'Sibilla Buntine','Real Estate Agent','sbuntinea@simplemachines.org');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (15,24,'Shamus Branscomb','Real Estate Agent','sbranscombe@irs.gov');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (17,25,'Nanine Dine-Hart','Real Estate Agent','ndinehartg@amazon.co.jp');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (20,14,'Donalt Simonassi','Real Estate Agent','dsimonassij@auda.org.au');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (24,29,'Eugenia Mewhirter','Real Estate Agent','emewhirtern@pcworld.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (30,30,'Benedikt Dwight','Real Estate Agent','bdwightt@usgs.gov');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (33,16,'Shane Van der Kruis','Real Estate Agent','svanw@fc2.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (34,15,'Clerkclaude McConville','Real Estate Agent','cmcconvillex@uol.com.br');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (39,17,'Thor Prosh','Real Estate Agent','tprosh12@cdbaby.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (43,6,'Phineas Endley','Real Estate Agent','pendley16@amazon.de');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (45,8,'Molli Coller','Real Estate Agent','mcoller18@earthlink.net');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (46,18,'Rip Gautrey','Real Estate Agent','rgautrey19@ycombinator.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (47,6,'Cobb Parzizek','Real Estate Agent','cparzizek1a@deviantart.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (48,33,'Lenee Cavan','Real Estate Agent','lcavan1b@cnet.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (50,6,'Felicity Cubuzzi','Real Estate Agent','fcubuzzi1d@unblog.fr');


-- Government agency users
INSERT INTO user(user_id,country_id,name,role,email) VALUES (4,34,'Cammy Blampy','Government Agency','cblampy3@wordpress.org');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (5,36,'Bartlet Lackmann','Government Agency','blackmann4@mysql.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (8,17,'Karim Kettle','Government Agency','kkettle7@friendfeed.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (12,12,'Nelle Sarfass','Government Agency','nsarfassb@opensource.org');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (13,12,'Demott Cattow','Government Agency','dcattowc@ask.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (16,26,'Terrill Cordes','Government Agency','tcordesf@ucla.edu');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (19,19,'Alaric Boggers','Government Agency','aboggersi@jigsy.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (22,4,'Philly Lapides','Government Agency','plapidesl@telegraph.co.uk');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (25,1,'Udell McNea','Government Agency','umcneao@yelp.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (28,4,'Ingeberg Ounsworth','Government Agency','iounsworthr@gmpg.org');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (32,16,'Elle Ivanonko','Government Agency','eivanonkov@wired.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (36,13,'Trace Whaymand','Government Agency','twhaymandz@cmu.edu');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (40,32,'Yolane Feechan','Government Agency','yfeechan13@histats.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (41,36,'Aili Soutter','Government Agency','asoutter14@flavors.me');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (42,15,'Rubi Seger','Government Agency','rseger15@walmart.com');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (44,3,'Abbye Horstead','Government Agency','ahorstead17@irs.gov');
INSERT INTO user(user_id,country_id,name,role,email) VALUES (49,35,'Eldin Gillimgham','Government Agency','egillimgham1c@joomla.org');


-- Students
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (1,9,15,'Kacey Ivons','Student','kivons0@blogtalkradio.com',1600);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (2,22,23,'Ahmed Jerche','Student','ajerche1@dot.gov',1350);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (3,16,1,'Nessy Satchell','Student','nsatchell2@bloomberg.com',2450);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (14,38,36,'Venus Landy','Student','vlandyd@domainmarket.com',650);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (18,43,25,'Leah McPike','Student','lmcpikeh@multiply.com',1100);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (21,5,5,'Shantee Tippings','Student','stippingsk@tumblr.com',2100);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (23,42,35,'Gar Carnalan','Student','gcarnalanm@simplemachines.org',1650);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (26,19,13,'Thomasine Keasey','Student','tkeaseyp@cornell.edu',1450);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (27,28,27,'Angelia Bernette','Student','abernetteq@wsj.com',1550);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (29,40,14,'Lucias Rumsby','Student','lrumsbys@xrea.com',2150);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (31,47,19,'Chen Pomphrett','Student','cpomphrettu@spotify.com',1450);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (35,23,2,'Zachery Barrar','Student','zbarrary@discovery.com',1150);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (37,2,1,'Fraser Geke','Student','fgeke10@qq.com',2300);
INSERT INTO user(user_id,university_id,country_id,name,role,email,max_budget) VALUES (38,35,7,'Tasha Lyddiard','Student','tlyddiard11@i2i.jp',500);

-- housing listings, some related to universities and others not.
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (1,'Charming Parisian House Near City Centre',10,NULL,9,2600,'House','Paris');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (2,'Cosy Studio Apartment in Nicosia',13,NULL,45,1000,'Studio Apartment','Nicosia');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (3,'Modern Townhouse Close to University',16,26,17,1000,'Townhouse','Luxembourg City');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (4,'Spacious Apartment in Prague Old Town',3,24,50,2550,'Apartment','Prague');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (5,'Bright Townhouse in Central Skopje',32,NULL,30,2350,'Townhouse','Skopje');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (6,'Affordable Studio in Bucharest City Centre',22,NULL,33,1300,'Studio Apartment','Bucharest');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (7,'Spacious Family House in Ankara',35,NULL,11,2200,'House','Ankara');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (8,'Contemporary Studio in Pristina',36,NULL,1,2650,'Studio Apartment','Pristina');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (9,'Quiet House Near University in Linz',19,46,48,700,'House','Linz');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (10,'Modern Apartment in Central Riga',14,NULL,6,2700,'Apartment','Riga');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (11,'Well-Located Apartment Near University Ljubljana',23,22,26,700,'Apartment','Ljubljana');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (12,'Charming Townhouse in Tallinn Old Town',6,NULL,35,900,'Townhouse','Tallinn');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (13,'Spacious Townhouse in Quiet Skopje Street',32,NULL,46,2050,'Townhouse','Skopje');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (14,'Modern Apartment Near University in Plovdiv',2,17,43,2600,'Apartment','Plovdiv');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (15,'Elegant Townhouse in Central Vilnius',15,NULL,31,2150,'Townhouse','Vilnius');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (16,'Cosy Studio With Balcony in Lisbon',21,NULL,47,1400,'Studio Apartment','Lisbon');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (17,'Affordable Family House in Dublin Suburbs',7,NULL,27,350,'House','Dublin');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (18,'Quaint House in Historic Porto',21,NULL,2,1350,'House','Porto');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (19,'Bright Studio Apartment in Amsterdam',18,NULL,10,1050,'Studio Apartment','Amsterdam');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (20,'Modern Apartment in Central Sofia',2,NULL,14,2000,'Apartment','Sofia');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (21,'Sunny Family House Near University Barcelona',9,20,50,550,'House','Barcelona');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (22,'Compact Studio in Central Riga',14,NULL,7,1350,'Studio Apartment','Riga');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (23,'Stylish Studio Apartment in Istanbul',35,NULL,20,2550,'Studio Apartment','Istanbul');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (24,'Elegant Apartment in Geneva City Centre',29,NULL,34,850,'Apartment','Geneva');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (25,'Spacious Studio With City Views Reykjavik',27,NULL,3,2250,'Studio Apartment','Reykjavik');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (26,'Detached House in Quiet Tallinn Street',6,NULL,24,1950,'House','Tallinn');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (27,'Modern Apartment With Stunning Views Reykjavik',27,NULL,37,2400,'Apartment','Reykjavik');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (28,'Spacious Apartment in Central London',30,50,38,2200,'Apartment','London');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (29,'Traditional House Near University in Athens',8,18,43,950,'House','Athens');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (30,'Cosy Townhouse in Tallinn City Centre',6,NULL,39,500,'Townhouse','Tallinn');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (31,'Bright Apartment in Pristina',36,NULL,21,1000,'Apartment','Pristina');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (32,'Spacious Apartment in Central Riga',14,NULL,15,1750,'Apartment','Riga');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (33,'Modern Apartment in Belgrade City Centre',34,NULL,23,800,'Apartment','Belgrade');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (34,'Luxury Studio Apartment in Zurich',29,NULL,45,1950,'Studio Apartment','Zurich');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (35,'Charming Townhouse Near University Thessaloniki',8,33,18,1100,'Townhouse','Thessaloniki');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (36,'Affordable Studio in Central Skopje',32,NULL,29,1300,'Studio Apartment','Skopje');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (37,'Elegant Townhouse Near University in Jurmala',14,40,33,2600,'Townhouse','Jurmala');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (38,'Spacious Townhouse With Garden Reykjavik',27,NULL,6,2250,'Townhouse','Reykjavik');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (39,'Modern Townhouse in Central Copenhagen',4,NULL,24,1050,'Townhouse','Copenhagen');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (40,'Cosy Studio Apartment in Nicosia',13,NULL,9,2250,'Studio Apartment','Nicosia');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (41,'Bright Family House in Tallinn',6,NULL,47,1500,'House','Tallinn');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (42,'Charming House in Lyon City Centre',10,NULL,11,1400,'House','Lyon');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (43,'Affordable Townhouse in Central Podgorica',31,NULL,1,900,'Townhouse','Podgorica');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (44,'Spacious Apartment in Skopje',32,NULL,30,2050,'Apartment','Skopje');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (45,'Grand Townhouse in Marseille',10,NULL,27,2450,'Townhouse','Marseille');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (46,'Cosy Townhouse Near University in Sofia',2,6,48,1100,'Townhouse','Sofia');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (47,'Comfortable Townhouse in Budapest',17,NULL,7,800,'Townhouse','Budapest');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (48,'Spacious Family House in Munich',5,NULL,29,2150,'House','Munich');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (49,'Elegant House in Central Milan',12,NULL,10,2100,'House','Milan');
INSERT INTO listing(listing_id,title,country_id,associated_university_id,user_id,price,property_type,city_name) VALUES (50,'Modern Studio Apartment in Warsaw',20,NULL,34,2750,'Studio Apartment','Warsaw');


INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('1','3','5','Breathtaking view from every window');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('2','7','2','Decent place but overpriced for this neighbourhood');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('3','12','5','Stunning view of the surroundings');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('4','18','4','Very spacious and well laid out');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('5','24','5','Prime location, very convenient');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('6','31','4','Lovely view from the balcony');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('7','2','3','Spacious apartment with solid amenities');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('8','9','1','Neighbours are quite loud at all hours');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('9','15','4','Wonderful view of the city');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('10','22','2','Near the university but noisy after dark');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('11','28','5','Gorgeous view, very peaceful');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('12','35','2','Fair price but a little steep for the area');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('13','41','5','Excellent location near everything');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('14','47','2','Slightly overpriced for what you get');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('15','4','2','Reasonable place but pricey for the street');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('16','10','4','Nice view, especially in the morning');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('17','16','1','Desperately needs some renovation work');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('18','21','5','Amazing view, worth every penny');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('19','27','4','Open floor plan, plenty of room');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('20','33','5','Fantastic spot, great access to transport');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('21','39',NULL,'Close to campus but loud late at night');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('22','44',NULL,'Renovation needed but has real potential');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('23','50','1','The neighbours make too much noise');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('24','5','3','Walking distance to uni, though noisy nights');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('25','11','4','Charming view, cosy atmosphere');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('26','17','3','Just minutes from uni, some nighttime noise');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('27','23','2','University nearby but evenings get noisy');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('28','29','3','A bit pricey but overall a decent place');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('29','36','5','Generous space and smart layout');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('30','42','2','Could use some updating and repairs');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('31','48','4','Pleasant view, nice natural light');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('32','1',NULL,'Roomy interior with a good layout');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('33','6','5','Incredible view, absolutely loved it');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('34','13','4','Lots of space and a smart floor plan');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('35','19','4','Lovely view, very relaxing setting');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('36','25','2','Slightly overpriced given the location');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('37','30','1','Neighbours are a constant nuisance');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('38','37','3','Comfortable apartment with decent facilities');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('39','43','1','Long overdue for a full renovation');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('40','49','1','Noise from neighbours is a real issue');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('41','8','1','Near uni but very noisy in the evenings');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('42','14','4','Impressive space and open layout');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('43','20','1','Renovation is overdue in several areas');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('44','26','2','A touch overpriced for this part of town');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('45','32','4','Scenic view, very enjoyable');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('46','38','2','Close to campus but noisy at night');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('47','45','1','Neighbours are quite disruptive');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('48','3','3','A bit pricey but a solid enough place');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('49','34','2','Priced a little high for what is offered');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('50','40','5','Spectacular view, truly stunning');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('51','46','4','Well-appointed apartment, good facilities');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('52','2','1','Disruptive noise from nearby neighbours');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('53','7','5','Ideal location, close to everything');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('54','13','1','Overpriced for the quality on offer');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('55','19','2','Renovation needed but great bones');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('56','25','5','Well-equipped apartment, great amenities');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('57','31','1','Serious renovation required throughout');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('58','37','5','Superb location, easy to get around');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('59','43','1','Renovation is badly needed here');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('60','49','2','Major renovation required, much potential');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('61','1',NULL,'Picturesque view from the main rooms');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('62','6','5','Unbeatable location, very well situated');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('63','11','1','Far too much noise from the neighbours');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('64','16','1','Renovation is clearly long overdue');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('65','21','4','Spacious apartment, well worth it');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('66','26','3','Good apartment but amenities are average');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('67','31','1','Neighbours are noisy and inconsiderate');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('68','36','2','Pricey for the area, not great value');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('69','41','1','Neighbour noise is a persistent problem');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('70','46','1','Renovation work is urgently needed');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('71','2','2','A bit steep given what is on offer');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('72','7','1','High price for the quality provided');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('73','12',NULL,'Good space with a sensible layout');
INSERT INTO reviews(review_id,listing_id,rating,comment) VALUES ('74','17','1','Far too expensive for this location');

-- government funding
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (1,13,2016,48000,'Urban Green Spaces Initiative','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (2,22,2004,31000,'Tenant Support Program','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (3,14,2010,67000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (4,29,2004,29000,'Student Welfare Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (5,7,2015,112000,'Public Health Outreach','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (6,36,2012,18000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (7,18,2023,95000,'Air Quality Improvement','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (8,10,2002,143000,'Low Income Housing Support','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (9,17,2000,77000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (10,8,2007,54000,'Community Wellness Program','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (11,7,2026,88000,'Residential Safety Fund','Crime Prevention Unit');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (12,16,2024,41000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (13,3,2002,63000,'Anti-Pollution in Cities','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (14,33,2003,22000,'Housing Renovation Grant','Urban Development Office');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (15,6,2019,175000,'Emissions Reduction Fund','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (16,3,2002,134000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (17,35,2002,59000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (18,13,2006,12000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (19,24,2012,83000,'Anti-Pollution in Cities','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (20,31,2022,46000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (21,32,2003,9000,'Social Housing Initiative','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (22,33,2020,37000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (23,15,2010,71000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (24,6,2020,98000,'Urban Air Quality Program','Noise Control Commission');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (25,33,2008,25000,'Low Income Housing Support','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (26,26,2013,161000,'Urban Green Spaces Initiative','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (27,4,2006,74000,'Neighbourhood Health Program','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (28,16,2026,52000,'Community Health Initiative','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (29,32,2001,118000,'Residential Support Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (30,4,2008,66000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (31,21,2008,93000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (32,29,2025,107000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (33,35,2002,34000,'Anti-Pollution in Cities','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (34,25,2017,189000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (35,11,2018,145000,'Public Health Outreach','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (36,3,2020,211000,'Neighbourhood Wellness Grant','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (37,18,2012,79000,'Emissions Reduction Fund','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (38,9,2019,55000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (39,1,2026,28000,'Anti-Pollution in Cities','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (40,30,2012,19000,'Low Income Housing Support','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (41,11,2025,167000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (42,31,2017,23000,'Urban Air Quality Program','Noise Control Commission');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (43,32,2019,86000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (44,26,2006,194000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (45,4,2009,8000,'Housing Renovation Grant','Urban Development Office');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (46,24,2022,43000,'Community Health Initiative','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (47,30,2003,221000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (48,31,2021,38000,'Anti-Pollution in Cities','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (49,22,2009,61000,'Tenant Support Program','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (50,5,2026,152000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (51,13,2013,47000,'Urban Green Spaces Initiative','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (52,24,2024,33000,'Air Quality Improvement','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (53,2,2010,128000,'Community Health Initiative','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (54,28,2001,57000,'Neighbourhood Wellness Grant','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (55,2,2017,91000,'Anti-Pollution in Cities','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (56,34,2018,44000,'Public Health Outreach','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (57,10,2003,176000,'Urban Air Quality Program','Noise Control Commission');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (58,8,2019,103000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (59,17,2006,36000,'Low Income Housing Support','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (60,15,2019,27000,'Emissions Reduction Fund','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (61,7,2002,148000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (62,13,2011,119000,'Urban Green Spaces Initiative','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (63,15,2025,204000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (64,11,2015,58000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (65,1,2014,72000,'Residential Safety Fund','Crime Prevention Unit');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (66,25,2012,85000,'Community Wellness Program','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (67,31,2003,196000,'Social Housing Initiative','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (68,3,2023,39000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (69,32,2007,131000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (70,2,2015,42000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (71,12,2002,109000,'Anti-Pollution in Cities','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (72,8,2013,97000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (73,31,2008,53000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (74,22,2003,114000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (75,9,2018,31000,'Neighbourhood Health Program','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (76,26,2010,158000,'Housing Renovation Grant','Urban Development Office');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (77,30,2006,17000,'Low Income Housing Support','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (78,4,2023,64000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (79,14,2025,122000,'Residential Support Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (80,23,2026,76000,'Urban Green Spaces Initiative','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (81,27,2018,89000,'Community Health Initiative','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (82,34,2004,183000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (83,8,2014,101000,'Anti-Pollution in Cities','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (84,30,2021,147000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (85,5,2021,68000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (86,14,2005,178000,'Air Quality Improvement','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (87,1,2007,193000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (88,25,2000,116000,'Community Wellness Program','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (89,33,2016,21000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (90,9,2006,173000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (91,34,2016,14000,'Tenant Support Program','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (92,7,2003,26000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (93,20,2024,49000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (94,25,2001,35000,'Residential Safety Fund','Crime Prevention Unit');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (95,19,2004,162000,'Campus Accommodation Fund','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (96,28,2002,57000,'Urban Green Spaces Initiative','Environmental Protection Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (97,35,2000,138000,'Community Health Initiative','Community Health Board');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (98,22,2015,69000,'Affordable Housing Fund','Housing Assistance Agency');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (99,5,2014,104000,'Student Housing Grant','Community Development Corporation');
INSERT INTO funding(funding_id,country_id,year,amount,program,agency) VALUES (100,34,2008,156000,'Neighbourhood Wellness Grant','Community Health Board');


# generating mock funding drafts
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (1,1,1,'Green City Initiative',75000,'Pollution','All Demographics','Targeting urban air quality improvements in Brussels');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (2,2,5,'Student Housing Expansion',120000,'House Price Index','Students','Addressing housing shortage near German universities');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (3,3,10,'Crime Reduction Program',55000,'Crime, Violence, and Vandalism','Low Income','Community safety initiatives in Paris neighborhoods');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (4,4,7,'Overcrowding Relief Fund',90000,'Overcrowding','Families','Emergency housing support for overcrowded Dublin households');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (5,5,9,'Noise Reduction Initiative',43000,'Noise','Elderly','Soundproofing grants near Madrid transport hubs');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (6,6,4,'Affordable Housing Plan',135000,'House Price Index','Low Income','Subsidized housing development in Copenhagen suburbs');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (7,7,2,'Poverty Relief Program',67000,'Poverty','All Demographics','Support for households below poverty line in Sofia');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (8,8,16,'Luxembourg Housing Fund',200000,'Overcrowding','Families','New residential units for growing Luxembourg City population');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (9,9,22,'Romania Green Initiative',48000,'Pollution','All Demographics','Air quality monitoring and improvement in Bucharest');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (10,10,12,'Rome Safety Initiative',82000,'Crime, Violence, and Vandalism','Elderly','Neighborhood safety infrastructure in Rome');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (11,11,21,'Lisbon Student Housing',95000,'House Price Index','Students','Affordable student accommodation near Lisbon universities');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (12,12,26,'Stockholm Noise Reduction',61000,'Noise','All Demographics','Noise barriers along Stockholm transit corridors');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (13,13,14,'Riga Housing Support',44000,'Overcrowding','Low Income','Renovation grants for overcrowded Riga apartments');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (14,14,18,'Amsterdam Green Housing',115000,'Pollution','Families','Eco-friendly housing retrofits in Amsterdam');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (15,15,6,'Tallinn Poverty Fund',38000,'Poverty','Low Income','Income support and housing assistance in Tallinn');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (16,16,20,'Warsaw Student Grant',72000,'House Price Index','Students','Student housing subsidies in Warsaw university district');
INSERT INTO funding_draft(draft_id, user_id, country_id, program, amount, indicators_targeted, demographics_targeted, description) VALUES (17,17,23,'Ljubljana Safety Program',53000,'Crime, Violence, and Vandalism','All Demographics','Community policing improvements in Ljubljana');
