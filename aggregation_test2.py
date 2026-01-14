from datetime import datetime
import requests
import json
import os
import pandas as pd
from pandas import json_normalize
from flask import Flask, request, jsonify

token = str(input("please enter token here"))

headers = {
    "Authorization" : f"Bearer {token}",
    "Accept" : "application/json"
}

params = {
    "stations" : int(input("please enter station numbere")),
    "parameters" : str(input("Please enter the parameters id")),
    "date_from" : str(input("Please enter the data in 2025-12-25T00:00:00 ")),
    "date_to" : str(input("Please enter the data in 2025-12-25T10:00:00 ")),
    "show_qc" : "undefined",
    "use_tag" : "undefined",
    "tag_id" : "undefined",
    "returnMetaData" : "undefined"
}

url = "https://alpha.wscada.net/api/analysis/more"

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)

hour_dict = {"T_1H": 505, "TD_1H": 510, "RH_1H": 540, "GLOB_1H": 589}
min_dict = {"T_10M": 2, "TD_10M": 511, "RH_10M": 539, "GLOB_10M": 591}
min_set = {"T1_10M", "TD.1_10M", "RH.1_10M","GLOB_10M"}


'''
for station in data:
    for parameters in station["parameters"]:
        data_items = json_normalize(parameters['data'])
        if parameters.get == "T_10M":
            if 'time' in data_items.columns and 'value' in data_items.columns:
                data_items['time'] = pd.to_datetime(data_items['time'])
                data_items.set_index('time', inplace=True)
                data_resampled = data_items.resample('10min').mean()
                data_resampled = round(data_resampled,2)
                aggregated_data = data_resampled.resample('h').mean()
                aggregated_data.index = aggregated_data.index.strftime('%Y-%m-%d %H:%M:%S')
            else:
                print("required columns are not found")
        else:
            print("the data are not 10 minutes data")
'''


app = Flask(__name__)
@app.route("/")
def home():
    results = []
    for station in data:
        for parameter in station.get("parameters",[]):
            if parameter.get("parameter_code") in min_set:
                if parameter.get("parameter_code") == "T1_10M" or "TD.1_10M" or "RH.1_10M":
                    results.append(parameter.get("parameter_code"))
                    for entry in parameter.get("data",[]):
                        results.append({
                            "time" : entry.get("time"),
                            "Value": round(entry.get("value"),2)
                        })
    return jsonify(results)

app.run()
