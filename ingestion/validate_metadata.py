import pandas as pd
import os, sqlite3
from frozen_v1.fs_root import DATA_DIR, DB_DIR

db_schema=DB_DIR/'fv1-db_schema.sql'
db_views=DB_DIR/'fv1-db_views.sql'

data=[x for x in os.listdir(DATA_DIR) if x[-1:-4:-1]]
# print(data)
raw_df=pd.read_csv(DATA_DIR/data[0])

data_df=raw_df.copy()
data_df=data_df.drop(columns=["city_name","datetime_first_local","datetime_last_local","sensor_category"])
# print(data_df.info(),data_df.head(10))

# sqlite db connection
conn_db=sqlite3.connect(DB_DIR/"frozen-v1.db")
cur_db=conn_db.cursor()

# sqlite memeory connection
conn_m=sqlite3.connect(":memory:")
cur_m=conn_m.cursor()

# write to memory db
with open(db_schema,'r',encoding='utf-8') as sf, open(db_views,'r',encoding='utf-8') as vf:
    schema=sf.read()
    views=vf.read()
    cur_m.executescript(schema)
    cur_m.executescript(views)

tables=pd.read_sql(
    "select name from sqlite_master where type='table' and name not like 'sqlite_%';",conn_m
)
schema={}
for table in tables["name"]:
    schema[table]=pd.read_sql(
        f"PRAGMA table_info('{table}')",conn_m
    ).set_index("cid")

location_df=data_df[[str(col) for col in schema["location"]["name"]]]
print(location_df)