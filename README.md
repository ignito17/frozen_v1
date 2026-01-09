# Frozen_V1
Frozen_V1 is a data engineering--oriented project that ingests, validates, and analyzes air quality data (PM25) for major Indian cities using the OpenAQ public API.
The project focus on **correct data modeling, deterministic ingestion and observability**, rather than ad-hoc API usage.

--

## Why this project exists

Most AQI dashboards treat cities as static points. In reality, air quality data is collected from **multiple monitoring stations (sensors (OpenAQ))** distributed across a city.

Frozen_V1 is built to answer:
- How do we **define a city** when the data sources does not?
- How do we **discover valid sensors dynamically**?
- How do we ingest time-series data **safely and repeatedly** without duplication?

The project is designed as a **realistic ingestion pipeline**.

--

# High-level system design

Cities are defined by **constraints**, not hardcoded IDs.

--

## Data Source

- **OpenAQ API (v3)**
- Data Includes
    - Locations (monitoring stations)
    - Sensors (pm25, pm10, etc)
    - Measurements (timestamped AQI values)

Official API: https://api.openaq.org

--

## City Definition strategy
Cities are **not first-class entities** in  OpenAQ.
They are derived using geographic constraints.

Example configuration:
```json
{
    "pune":{
        "name":"Pune",
        "geo_loco_center":[18.5204,73.8567],
        "radius_m":25000,
        "parameter":"pm25",
    }
}
```
- This allows 
    - Dynamic discovery of stations
    - Reproducible ingestion
    - Easy extension to new cities

--

## Metadata Discovery (current feature)
The Metadata scanner:
- Queries locations within a city radius.
- Filters only monitoring stations.
- Validates presence of pm25 sensors.
- Extract sensor + location metadata.
- Stores results in a CSV registry.
    - Example output:
    ```
        city_key,location_id,sensor_id,latitude,longitude,datetime_first_utc,datetime_last_utc
    ```
- This metdata is later used for **safe predictable ingestion**.

--

## Observability
The project includes basic observability to track runtime and resource usage.
- Every job/script can be wrapped with process metrics:
    - Runtime (wall-clock)
    - CPU usage (user + system)
    - Memory usage (RSS)
- This allows **Debugging, process optimisation and visibility of resources usage**

# Project Structure
This whole repo is intended as a python module
```
- frozen_v1/
    - configs/          # City & API configurations
    - ingestion/        # Metadata + measurement ingestion
    - db/               # SQLite connector & schema
    - observability/    # Runtime & resource metrics
    - data/             # Generated CSVs (ignored in git)
    - fs_root.py        # Project wide path resolution
```

--

## Deployment (How to run)
```
cd /to_the_folder_containing frozen_v1
python3 -m frozen_v1/module/run_feature
```

--

## Design Decisions (intentional)
- Cities are queries, not fixed points
- Metadata is ingested before measurements
- Validation is explicit, not assumed
- Modularity and Observability is built-in

--

## Design Tradeoffs (add later)

--

# Roadmap 
- [ ] Periodic scanning and Persistance of  Metadata into SQLite
- [ ] Incremental measurement ingestion
- [ ] Deduplication using composite key
- [ ] AQI trend analysis (Pune vs Delhi)
- [ ] Visualisation (matplotlib / seaborn)
- [ ] API layer serving (Flask)
- [ ] Deployment on Oracle VM/ Raspberry Pi

--

# Status 
Active Development
This project is intentionally built step-by-step to reflect real-world data engineering flows.