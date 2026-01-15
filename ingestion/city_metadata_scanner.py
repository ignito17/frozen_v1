import requests, json, csv
from datetime import datetime, timezone
from collections import Counter
from frozen_v1.fs_root import CITIES_CONFIG, OPEN_AQI_CONFIG, DATA_DIR
from frozen_v1.ingestion.http_validator import validate_response

VERFIY_SSL=False     # for cts laptop

# Loading data constraints
# load cities data
def load_cities():
    with open(CITIES_CONFIG) as f:
        return json.load(f)
    
# load openaq config    
def load_source_openaq_api():
    with open(OPEN_AQI_CONFIG) as f:
        return json.load(f)
    
# build location params    
def build_location_params(city,limit=10):
    lat,lon=city["center"]
    return{
        "coordinates":f"{lat},{lon}",
        "radius":city["radius_m"],
        "isMonitor":"true",
        "limit":limit
    }

# hitting api and fetchig locations
def fetch_locations(headers, params):
    resp=requests.get(
        f"https://api.openaq.org/v3/locations",
        headers=headers,
        params=params,
        timeout=30,
        verify=VERFIY_SSL
    )
    validate_response(resp)
    return resp.json()["results"]

# Safe utc, in case location does not return datatime
# Decided to keep utc and local and no timestamp as well
# For data breadth and history
def extract_datetime(dt):
    # Safely extract utc and local datetime from OpenAQ datetime object
    if not isinstance(dt,dict):
        return None,None
    utc=dt.get("utc")
    local=dt.get("local")
    # Normalize empty strings
    if utc=="":
        utc=None
    if local =="":
        local = None
    return utc,local

def parse_utc(ts):
    # Parse OpenAQ UTC timestamps safely.
    # Expected format: YYYY-MM-DDTHH:MM:SSZ
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except Exception:
        return None

# Classifying Sensors instead of rejecting explicitly
def classify_sensor(datetime_last_utc, datetime_last_local):
    if datetime_last_utc:
        last=parse_utc(datetime_last_utc)
        if last:
            try:
                now=datetime.now(timezone.utc)
                age_days=(now-last).days
                if age_days<=7:
                    return "active"
                elif age_days<=90:
                    return "recently_inactive"
                else:
                    return "historical"
            except Exception:
                return "utc_parse_error"
    elif datetime_last_local:
        return "local_time_only"
    return "unknown"

# Extract location and sensor id with pm25 data.
def extract_pm25_sensors(city_key, city_name, locations, parameter):
    rows = []

    for loc in locations:
        sensors = loc.get("sensors", [])
        first_utc,first_local=extract_datetime(loc.get("datetimeFirst"))
        last_utc,last_local=extract_datetime(loc.get("datetimeLast"))
        category=classify_sensor(last_utc,last_local)
        for s in sensors:
            if s.get("parameter", {}).get("name") == parameter:
                rows.append({
                    "city_key": city_key,
                    "city_name": city_name,
                    "location_id": loc["id"],
                    "location_name": loc["name"],
                    "sensor_id": s["id"],
                    "parameter": parameter,
                    "latitude": loc["coordinates"]["latitude"],
                    "longitude": loc["coordinates"]["longitude"],
                    "datetime_first_utc":first_utc,
                    "datetime_first_local":first_local,
                    "datetime_last_utc":last_utc,
                    "datetime_last_local":last_local,
                    "sensor_category":category,
                })
    return rows

# write to csv
def write_csv(rows,output_path):
    if not rows:
        print("No rows to write:")
        return
    
    with open(output_path, "w", newline="") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def main():

    BASE_URL=load_source_openaq_api()["source"]["base_url"]
    API_KEY=load_source_openaq_api()["source"]["api_key"]
    limit=load_source_openaq_api()["scanner"]["limit"]

    headers={'X-API-Key':API_KEY}
    cities=load_cities()
    all_rows=[]
    for city_key,city in cities.items():
        print(f"Scanning {city["name"]}")
        
        params=build_location_params(city,limit=limit)
        locations=fetch_locations(headers,params)
        rows=extract_pm25_sensors(city_key,city["name"],locations,city["parameter"])
        all_rows.extend(rows)
    
    output=DATA_DIR/f"metadata_locations_pm25_limit{limit}.csv"
    write_csv(all_rows,output)
    print(f"Saved {len(all_rows)} rows -> {output}")
    print("Sensor categories:")
    for k,v in Counter(r["sensor_category"] for r in all_rows).items():
        print(F" {k}:{v}")

if __name__=="__main__":
    main()
