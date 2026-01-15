CREATE TABLE IF NOT EXISTS sensors_metadata(
    sensor_id INTEGER PRIMARY KEY,
    city_key TEXT NOT NULL,
    city_name TEXT NOT NULL,
    location_id INTEGER NOT NULL,
    location_name TEXT,
    parameter TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    datetime_first_utc TEXT,
    datetime_last_utc TEXT,
    datetime_first_local TEXT,
    datetime_last_local TEXT,
    sensor_category TEXT NOT NULL,
    ingested_at TEXT NOT NULL
);