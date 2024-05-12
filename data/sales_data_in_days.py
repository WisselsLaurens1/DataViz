import pandas as pd
from datetime import datetime
import json

PATH = "./suncharge/Sales.csv"
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

plant_customer_region_map = {
    "ANT2": ["Belgium", "Germany", "Netherlands"],
    "BIR2": ["United Kingdom"],
    "WRO2": ["Czech Republic", "Greece", "Hungary", "Poland"],
    "GOT2": ["Denmark", "Estonia", "Finland", "Latvia", "Lithuania", "Norway", "Sweden"],
    "LYO2": ["Croatia", "France", "Italy", "Portugal", "Slovenia", "Spain", "Switzerland"]
}

data = []
columns = [
    "PlantKey",
    "SalesOrderCreationDate",
    "RequestedDeliveryDate",
    "DeliveryDate"
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

sales_per_plant = {}
for dp in data:
    plant_key = plant_key_map[dp["PlantKey"]]
    sales_per_plant.setdefault(plant_key, {
        "metadata": {
            "Route": f"{plant_key}-{', '.join(plant_customer_region_map[plant_key])}",
            "CustomerRegion": plant_customer_region_map[plant_key]
        },
        "data": []
    } )
    del dp["PlantKey"]
    dp["SalesOrderCreationDate"] = days_from_year_0(dp["SalesOrderCreationDate"] )
    dp["RequestedDeliveryDate"] = days_from_year_0(dp["RequestedDeliveryDate"] )
    dp["DeliveryDate"] = days_from_year_0(dp["DeliveryDate"])

    sales_per_plant[plant_key]["data"].append(dp)

with open("./data.json", "r") as f:
    data = json.load(f)
    data["sales_data_in_days"] = sales_per_plant

with open("./data.json", "w") as f:
    f.write(json.dumps(data, indent=2))