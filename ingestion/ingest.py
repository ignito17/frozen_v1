import csv
from frozen_v1.fs_root import DATA_DIR

# csv_list=[csv_path for csv_path in DATA_DIR.iterdir()]
metdata_csv=DATA_DIR/"metadata_locations_pm25_limit25.csv"

def read_csv_as_dict(csv_path):
    with open(csv_path, 'r',newline='') as file:
        reader=csv.reader(file)
        for row in reader:
            row[1]

read_csv_as_dict(metdata_csv)