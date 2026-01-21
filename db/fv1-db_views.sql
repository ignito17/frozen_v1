-- ==========================================================
-- Frozen_v1 Semantic Views
-- Sensor state classification (time-relative)
-- ==========================================================

DROP VIEW IF EXISTS sensor_status;

CREATE VIEW sensor_status AS
SELECT
  s.sensor_id,
  s.location_id,
  s.parameter,

  s.datetime_last_utc AS metadata_last_utc,
  MAX(m.datetime_utc_start) AS last_measured_utc,

  CASE
    WHEN s.datetime_last_utc IS NULL
         AND MAX(m.datetime_utc_start) IS NULL
      THEN 'obsolete'

    WHEN datetime(
           replace(
             COALESCE(MAX(m.datetime_utc_start), s.datetime_last_utc),
             'Z', ''
           )
         ) >= datetime('now', '-7 days')
      THEN 'active'

    ELSE 'historical'
  END AS sensor_status

FROM sensor s
LEFT JOIN measurement_pm25 m
  ON s.sensor_id = m.sensor_id
GROUP BY s.sensor_id;
