--					=======================================================					
--					Frozen_v1 Schema
--					Determenistic, interval-based air quality ingestionn
--					=======================================================
--
PRAGMA FOREIGN_KEYS=ON;
-- PRAGMA JOURNAL_MODE=WAL;
--					=======================================================
--					City Configuration (Logically defined cities for fv1)
--					=======================================================
CREATE TABLE IF NOT EXISTS city(
city_key TEXT PRIMARY KEY,
city_name TEXT NOT NULL,
center_latitude REAL NOT NULL,
center_longitude REAL NOT NULL,
radius_m INTEGER NOT NULL,
-- Column Checks and Constraints
CHECK (
 typeof(city_key)='text'),
CHECK (
 typeof(city_name)='text'),
CHECK (
 typeof(center_latitude) IN ('integer','real')),
CHECK (center_latitude BETWEEN -90 AND 90),
CHECK (
 typeof(center_longitude) IN ('integer','real')),
CHECK (center_longitude BETWEEN -180 AND 180),
CHECK (
 typeof(radius_m) = 'integer'),
CHECK (radius_m > 0 and radius_m <= 25000)
);
-- OpenAQ allows 25,000 meters maximum query radius from a geolocation point on globe.

--					=======================================================
--					Monitoring Locations (Unique in OpenAQ)
--					=======================================================

CREATE TABLE IF NOT EXISTS location(
location_id INTEGER PRIMARY KEY,
city_key TEXT NOT NULL,
location_name TEXT,
latitude REAL NOT NULL,
longitude REAL NOT NULL,
-- Column checks and Constraints
CHECK (
 typeof(location_id) = 'integer'),
CHECK (
 typeof(city_key) = 'text'),
CHECK (location_name IS NULL OR typeof(location_name) = 'text'),
CHECK (
 typeof(latitude) IN ('integer','real')),
CHECK (
 typeof(longitude) IN ('integer','real')),
CHECK (latitude BETWEEN -90 AND 90),
CHECK (longitude BETWEEN -180 AND 180),

FOREIGN KEY (city_key)
  REFERENCES city(city_key)
  ON DELETE RESTRICT
  ON UPDATE CASCADE
);

--					==========================================================
--					Sensor Metdata (sensor_id unique in OpenAQ)
--					==========================================================

CREATE TABLE IF NOT EXISTS sensor (
sensor_id INTEGER PRIMARY KEY,
location_id INTEGER NOT NULL,
parameter TEXT NOT NULL,
unit TEXT,
datetime_first_utc TEXT,
datetime_last_utc TEXT,
-- Column checks and constraints
CHECK (
 typeof(sensor_id)='integer'),
CHECK (
 typeof(location_id)='integer'),
CHECK (
 typeof(parameter)='text'),
CHECK (parameter IN ('pm25')),
CHECK (unit IS NULL OR typeof(unit)='text'),
CHECK (
	datetime_first_utc IS NULL OR
	typeof(datetime_first_utc)='text'
	AND datetime_first_utc LIKE '%T%Z'),
CHECK (
	datetime_last_utc IS NULL OR
	typeof(datetime_last_utc)='text'
	AND datetime_last_utc LIKE '%T%Z'),
CHECK (
	datetime_first_utc IS NULL OR
	datetime_last_utc IS NULL OR
	datetime_last_utc >= datetime_first_utc),

FOREIGN KEY (location_id) REFERENCES location(location_id)
	ON DELETE RESTRICT ON UPDATE CASCADE);

--					=============================================================
--					PM2.5 Measurements (interval-based time series fact table)
--					=============================================================
CREATE TABLE IF NOT EXISTS measurement_pm25 (
sensor_id INTEGER NOT NULL,
datetime_utc_start TEXT NOT NULL,
datetime_utc_end TEXT NOT NULL,
interval_minutes INTEGER NOT NULL,
value REAL NOT NULL,
unit TEXT NOT NULL,
ingestion_ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- Composite Primary key to prevent duplicate measurement
PRIMARY KEY(sensor_id,datetime_utc_start,datetime_utc_end),
-- Column checks and Constraints
CHECK (typeof(sensor_id)='integer'),
CHECK (typeof(datetime_utc_start)='text'),
CHECK (typeof(datetime_utc_end)='text'),

CHECK (datetime_utc_end > datetime_utc_start),
CHECK (typeof(interval_minutes)='integer'),
-- CHECK(interval_minutes=15),
CHECK (typeof(value) in ('real','integer')),
CHECK (value >=0), -- AND value <= 1000
CHECK (typeof(unit)='text'),
CHECK (unit LIKE 'µg/m³'),
CHECK (typeof(ingestion_ts)='text'),

FOREIGN KEY (sensor_id) REFERENCES sensor(sensor_id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

--					=================================================================
--					Indexes for query performance
--					===============================================================
CREATE INDEX IF NOT EXISTS idx_measurement_sensor_time 
ON measurement_pm25 (sensor_id,datetime_utc_start);

CREATE INDEX IF NOT EXISTS idx_location_city 
ON location(city_key);
