USE farmers_market_db;

INSERT INTO `farms` (`farm_id`,`farm_name`,`user_id`,`created_by`)
VALUES
(1,'Hagston Family Farm',1,'mockaroo'),
(2,'Lesslie Acres',2,'mockaroo'),
(3,'Blowfield Organics',8,'mockaroo'),
(4,'Greenlies Grove',10,'mockaroo'),
(5,'Olenin Orchards',11,'mockaroo'),
(6,'Antrag Fields',16,'mockaroo'),
(7,'Keston Pastures',17,'mockaroo'),
(8,'Worland Gardens',19,'mockaroo'),
(9,'Labbet Homestead',21,'mockaroo'),
(10,'Murray Meadows',22,'mockaroo');

INSERT INTO `farms_location` (`farm_id`,`longitude`,`latitude`,`country`,`created_by`)
VALUES
(1,4.720,50.860,'Belgium','mockaroo'),
(2,-1.548,53.801,'United Kingdom','mockaroo'),
(3,2.349,48.864,'France','mockaroo'),
(4,11.582,48.135,'Germany','mockaroo'),
(5,4.895,52.370,'Netherlands','mockaroo'),
(6,-3.703,40.417,'Spain','mockaroo'),
(7,-1.257,51.752,'United Kingdom','mockaroo'),
(8,9.190,45.464,'Italy','mockaroo'),
(9,4.351,50.846,'Belgium','mockaroo'),
(10,12.496,41.903,'Italy','mockaroo');
