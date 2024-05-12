import pandas as pd
from datetime import datetime
import json

PATH = "./suncharge/Purchases.csv"
df = pd.read_csv(PATH)

plant_key_map = {
    1001: "ANT1",
    1002: "WRO1",
    1003: "LYO1",
    1: "ANT1",
    2: "WRO1",
    3: "LYO1",
    4: "ANT2",
    5: "WRO2",
    6: "LYO2",
    7: "BIR2",
    8: "GOT2"
}

data = []
columns = [
    "PlantKey",
    "VendorKey",
    "PurchaseOrderCreationDate",
    "PlannedGoodsReceiptDate",
    "ActualGoodsReceiptDate",
    "PlannedArrivalDateYard",
    "ActualArrivalDateYard",
    "PlannedVendorShipmentDate",
    "ActualVendorShipmentDate",
]
for data_point in df[columns].values:
    default = {column: None for column in columns}
    populated_data_point = {key: data_point[i] for i, key in enumerate(default.keys())}
    data.append(populated_data_point)

def days_from_year_0(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    year_0 = datetime(1, 1, 1)
    difference = date_object - year_0
    return difference.days

sales_per_route = {}
for dp in data:
    vendor_key = plant_key_map[dp['VendorKey']]
    plant_key = plant_key_map[dp['PlantKey']]
    route = f"{vendor_key}-{plant_key}"
    sales_per_route.setdefault(route, [])
    for c in columns[2:]:
        dp[c] = days_from_year_0(dp[c])
    dp["Route"] = f"{vendor_key}-{plant_key}"
    dp["VendorKey"] = vendor_key
    dp["PlantKey"] = plant_key
    sales_per_route[route].append(dp)

with open("./data.json", "r") as f:
    data = json.load(f)
    data["purchases_data_in_days"] = sales_per_route

with open("./data.json", "w") as f:
    f.write(json.dumps(data, indent=2))