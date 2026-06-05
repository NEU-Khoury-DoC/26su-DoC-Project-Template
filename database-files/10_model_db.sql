USE farmers_market_db;

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
    country VARCHAR(100),
    crop VARCHAR(100),
    year INT,
    selling_price FLOAT
);

CREATE TABLE IF NOT EXISTS WeatherData (
    year INT,
    temperature_2m_mean FLOAT,
    precipitation_sum FLOAT,
    geo VARCHAR(11)
);

INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,11.9413698630137,561.2,'Austria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,11.251912568306011,704.2,'Austria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,11.234794520547945,527.5,'Austria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,12.166027397260274,614.9,'Austria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,12.056712328767123,614.0,'Austria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,11.448087431693988,739.5,'Austria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,10.806849315068494,643.6,'Austria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,11.750410958904109,666.2,'Austria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,12.194246575342465,767.8,'Austria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,12.65737704918033,741.9,'Austria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,11.223013698630137,691.6,'Belgium');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,11.056010928961749,779.7,'Belgium');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,11.116712328767123,736.2,'Belgium');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,11.602739726027398,630.6,'Belgium');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,11.308493150684933,787.9,'Belgium');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,11.881693989071037,766.2,'Belgium');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,10.319178082191781,974.2,'Belgium');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,11.816986301369862,623.0,'Belgium');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,11.832054794520548,1000.9,'Belgium');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,11.614207650273224,1027.5,'Belgium');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,11.269315068493151,614.4,'Bulgaria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,11.360109289617487,636.0,'Bulgaria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,10.825205479452054,773.9,'Bulgaria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,11.431232876712327,678.7,'Bulgaria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,12.208219178082192,552.8,'Bulgaria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,11.473497267759564,727.0,'Bulgaria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,11.054794520547945,792.2,'Bulgaria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,11.659999999999998,576.4,'Bulgaria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,12.378082191780821,814.8,'Bulgaria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,12.789071038251366,502.1,'Bulgaria');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,12.622739726027397,893.0,'Croatia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,12.18142076502732,919.6,'Croatia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,11.992876712328766,932.5,'Croatia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,12.192876712328767,919.8,'Croatia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,12.374246575342466,1020.6,'Croatia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,12.118852459016393,921.3,'Croatia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,11.538630136986303,803.4,'Croatia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,12.366575342465755,710.4,'Croatia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,12.634520547945206,1182.9,'Croatia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,13.059562841530056,1015.0,'Croatia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,19.97287671232877,361.0,'Cyprus');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,20.746994535519125,236.0,'Cyprus');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,19.736438356164385,195.9,'Cyprus');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,20.601369863013698,330.6,'Cyprus');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,19.729589041095892,429.5,'Cyprus');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,20.09016393442623,337.2,'Cyprus');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,20.363561643835617,215.6,'Cyprus');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,19.656712328767124,228.0,'Cyprus');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,20.167397260273972,286.2,'Cyprus');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,20.880054644808745,318.8,'Cyprus');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,11.291780821917808,527.2,'Czechia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,10.3672131147541,630.1,'Czechia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,10.092054794520548,613.3,'Czechia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,11.403561643835618,412.0,'Czechia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,11.113698630136986,604.9,'Czechia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,10.791256830601093,761.4,'Czechia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,9.351506849315069,680.7,'Czechia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,10.772328767123287,683.1,'Czechia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,11.405753424657535,771.4,'Czechia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,11.671038251366122,714.6,'Czechia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,9.472328767123289,745.3,'Denmark');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,9.366666666666665,578.4,'Denmark');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,9.23890410958904,838.8,'Denmark');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,10.105479452054794,472.90000000000003,'Denmark');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,10.11917808219178,729.6,'Denmark');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,10.451639344262295,632.6,'Denmark');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,9.337260273972602,679.5,'Denmark');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,9.875068493150685,554.8,'Denmark');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,9.763287671232877,829.3,'Denmark');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,10.08224043715847,704.6,'Denmark');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,7.646575342465753,596.8,'Estonia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,6.630327868852459,660.0,'Estonia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,6.229041095890411,772.2,'Estonia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,7.122191780821917,561.1,'Estonia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,7.262739726027397,788.2,'Estonia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,8.033879781420765,811.2,'Estonia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,6.611780821917809,748.9,'Estonia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,6.941095890410959,691.4,'Estonia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,6.896986301369863,889.0,'Estonia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,7.873770491803279,796.3,'Estonia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,7.255068493150684,688.8,'Finland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,6.221311475409836,663.7,'Finland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,5.966027397260274,922.2,'Finland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,6.64958904109589,580.9,'Finland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,6.725205479452054,831.7,'Finland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,8.045081967213115,948.8,'Finland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,6.053424657534246,777.2,'Finland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,6.537534246575342,736.8,'Finland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,6.398082191780823,856.9,'Finland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,7.104918032786886,804.2,'Finland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,12.179178082191779,534.7,'France');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,11.641256830601092,707.7,'France');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,12.0413698630137,736.7,'France');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,12.552328767123289,779.4,'France');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,12.240821917808217,753.3,'France');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,13.007377049180327,649.0,'France');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,11.40027397260274,741.5,'France');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,12.873424657534247,706.1,'France');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,12.913698630136986,973.7,'France');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,12.213934426229509,1151.1,'France');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,10.829589041095891,575.4,'Germany');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,10.458743169398907,511.8,'Germany');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,9.966575342465754,836.0,'Germany');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,11.186849315068493,412.5,'Germany');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,11.452054794520548,532.0,'Germany');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,11.272404371584699,538.7,'Germany');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,9.788767123287672,661.1,'Germany');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,10.990958904109588,489.0,'Germany');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,11.14,830.9,'Germany');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,11.74672131147541,647.3,'Germany');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,17.82904109589041,403.3,'Greece');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,18.56584699453552,254.20000000000002,'Greece');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,17.715616438356165,461.5,'Greece');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,18.075342465753426,593.0,'Greece');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,17.815068493150687,715.6,'Greece');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,17.75846994535519,579.6,'Greece');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,17.90986301369863,511.9,'Greece');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,17.728219178082192,353.3,'Greece');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,18.416986301369864,561.4,'Greece');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,19.231147540983606,486.0,'Greece');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,12.249589041095891,554.9,'Hungary');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,11.54207650273224,749.6,'Hungary');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,11.373698630136985,675.9,'Hungary');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,12.382191780821918,692.0,'Hungary');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,12.407945205479452,730.0,'Hungary');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,11.935245901639345,700.4,'Hungary');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,11.133972602739727,512.9,'Hungary');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,12.287397260273972,579.0,'Hungary');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,12.50164383561644,952.9,'Hungary');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,13.015573770491804,616.1,'Hungary');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,10.046301369863015,866.4,'Ireland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,10.307103825136613,804.7,'Ireland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,10.813698630136987,934.1,'Ireland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,10.692054794520548,920.8,'Ireland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,10.61890410958904,973.8,'Ireland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,10.652732240437158,900.1,'Ireland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,10.792054794520547,841.0,'Ireland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,11.20082191780822,919.9,'Ireland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,11.418082191780822,1089.1,'Ireland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,11.059016393442622,975.0,'Ireland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,16.148219178082194,778.0,'Italy');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,16.08743169398907,810.4,'Italy');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,16.183013698630138,583.3,'Italy');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,16.489315068493152,1130.7,'Italy');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,16.43013698630137,943.4,'Italy');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,16.331967213114755,888.3,'Italy');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,16.15068493150685,913.9,'Italy');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,17.20794520547945,899.0,'Italy');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,16.863835616438358,925.1,'Italy');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,17.207377049180327,875.6,'Italy');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,8.542739726027397,600.5,'Latvia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,7.848360655737705,788.9,'Latvia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,7.337534246575342,795.4,'Latvia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,8.311780821917809,546.9,'Latvia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,8.65972602739726,718.7,'Latvia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,9.12377049180328,702.2,'Latvia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,7.433698630136987,797.1,'Latvia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,7.79013698630137,747.8,'Latvia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,8.297808219178082,860.9,'Latvia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,9.216666666666667,799.6,'Latvia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,8.548493150684932,629.1,'Lithuania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,7.65,801.0,'Lithuania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,7.281917808219179,936.3,'Lithuania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,7.990958904109589,679.3,'Lithuania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,8.721917808219178,657.4,'Lithuania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,9.042896174863387,630.6,'Lithuania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,6.885479452054794,910.4,'Lithuania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,7.472876712328767,824.4,'Lithuania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,8.623561643835616,836.4,'Lithuania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,9.405737704918034,767.5,'Lithuania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,10.112602739726027,636.6,'Luxembourg');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,9.554098360655738,809.5,'Luxembourg');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,9.849863013698629,831.7,'Luxembourg');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,10.63890410958904,819.1,'Luxembourg');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,10.202739726027398,948.3000000000001,'Luxembourg');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,10.872677595628415,872.2,'Luxembourg');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,9.315068493150685,997.3,'Luxembourg');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,10.976712328767123,772.9,'Luxembourg');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,10.88986301369863,993.5,'Luxembourg');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,10.530054644808743,1096.3,'Luxembourg');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,19.607397260273974,362.40000000000003,'Malta');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,19.78551912568306,349.2,'Malta');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,19.48986301369863,351.7,'Malta');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,19.747945205479454,373.7,'Malta');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,19.473698630136987,504.2,'Malta');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,19.754918032786886,263.3,'Malta');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,20.052054794520547,463.8,'Malta');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,20.114794520547946,248.6,'Malta');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,20.273150684931505,339.0,'Malta');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,20.73415300546448,242.0,'Malta');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,10.776438356164384,768.7,'Netherlands');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,10.812841530054644,706.9,'Netherlands');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,10.786849315068492,925.0,'Netherlands');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,11.153150684931507,727.2,'Netherlands');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,11.005205479452055,965.1,'Netherlands');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,11.44535519125683,923.1,'Netherlands');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,10.286575342465753,943.9,'Netherlands');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,11.324931506849316,802.0,'Netherlands');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,11.512602739726029,1241.5,'Netherlands');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,11.558743169398907,1154.0,'Netherlands');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,10.206027397260273,485.0,'Poland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,9.624043715846994,728.3,'Poland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,9.268219178082193,919.3,'Poland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,10.362191780821917,637.2,'Poland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,10.867671232876711,604.7,'Poland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,10.477868852459016,780.3,'Poland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,8.926849315068493,765.4,'Poland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,9.73150684931507,657.7,'Poland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,10.610958904109589,755.0,'Poland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,11.457377049180327,628.6,'Poland');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,16.682191780821917,353.2,'Portugal');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,16.737158469945356,595.7,'Portugal');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,17.121917808219177,410.0,'Portugal');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,16.42931506849315,634.1,'Portugal');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,16.627123287671232,487.7,'Portugal');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,17.023224043715846,562.8,'Portugal');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,16.65150684931507,554.4,'Portugal');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,17.36931506849315,773.0,'Portugal');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,17.526301369863013,462.5,'Portugal');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,17.315027322404372,595.9,'Portugal');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,12.733972602739724,601.2,'Romania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,12.191803278688525,697.0,'Romania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,11.641917808219178,795.5,'Romania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,12.294246575342465,698.3,'Romania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,13.024109589041096,617.9,'Romania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,13.182513661202186,620.7,'Romania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,11.9,671.3,'Romania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,12.906575342465752,444.3,'Romania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,13.807671232876713,597.1,'Romania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,14.09672131147541,562.6,'Romania');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,11.896438356164383,544.2,'Slovakia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,11.330327868852459,630.4,'Slovakia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,11.349315068493151,556.2,'Slovakia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,12.344109589041096,573.4,'Slovakia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,12.077260273972602,630.5,'Slovakia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,11.560382513661203,716.9,'Slovakia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,10.789315068493151,611.2,'Slovakia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,11.93917808219178,527.6,'Slovakia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,12.217260273972602,735.4,'Slovakia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,12.7672131147541,721.5,'Slovakia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,11.26849315068493,1005.3,'Slovenia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,10.90054644808743,1246.8,'Slovenia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,10.505479452054795,1343.1000000000001,'Slovenia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,11.096986301369864,1112.9,'Slovenia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,11.093150684931507,1345.7,'Slovenia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,10.800819672131148,1275.0,'Slovenia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,10.262739726027398,1105.1,'Slovenia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,11.501917808219178,940.5,'Slovenia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,11.28109589041096,1601.0,'Slovenia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,11.52295081967213,1304.0,'Slovenia');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,15.20082191780822,245.0,'Spain');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,14.85464480874317,497.8,'Spain');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,15.903287671232876,356.8,'Spain');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,14.651232876712328,538.3,'Spain');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,15.424931506849315,373.1,'Spain');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,15.39863387978142,507.4,'Spain');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,15.012876712328767,553.6,'Spain');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,16.32904109589041,531.5,'Spain');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,15.87205479452055,516.7,'Spain');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,15.801092896174863,490.6,'Spain');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2015,8.122191780821918,675.7,'Sweden');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2016,7.534972677595629,454.7,'Sweden');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2017,6.975890410958904,580.6,'Sweden');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2018,7.896986301369863,469.8,'Sweden');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2019,7.637260273972602,703.7,'Sweden');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2020,8.789617486338798,612.5,'Sweden');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2021,7.089863013698631,671.4,'Sweden');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2022,7.646027397260275,601.5,'Sweden');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2023,7.1,772.0,'Sweden');
INSERT INTO WeatherData(year,temperature_2m_mean,precipitation_sum,geo) VALUES (2024,7.9554644808743165,647.9,'Sweden');
