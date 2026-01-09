# fs.py
from pathlib import Path

# Root directory of the project
ROOT=Path(__file__).resolve().parent

# To save configs of location and sources
CONFIG_DIR=ROOT/"configs"
DB_DIR=ROOT/"db"                    # Main DB /connector of project

# Make dirs if not exist
# CONFIG_DIR.mkdir(exist_ok=True)
# DATA_DIR.mkdir(exist_ok=True)
# DB_DIR.mkdir(exist_ok=True)

# CONFIGS BY NAME
CITIES_CONFIG=CONFIG_DIR/"cities.json"
OPEN_AQI_CONFIG=CONFIG_DIR/"openaq_api.json"


# Raw Data files
DATA_DIR=ROOT/"data"                # Raw csv and json data files if any
# Database
SQLITE_DB=DB_DIR/"frozen_V1_deb.db"