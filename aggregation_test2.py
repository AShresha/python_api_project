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

param_id_raw = str(input("Please enter the parameter ids"))
try:
    param_ids = [int(p.strip()) for p in param_id_raw.split(",")]
except Exception:
    jsonify({"error":"Parameter ids must be multiples"})


params = {
    "stations" : int(input("please enter station numbere")),
    "parameters" : ",".join(map(str, param_ids)),
    #"parameters" : str(input("Please enter the parameters id")),
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

aggregated_data = []

for station in data:
    for parameters in station.get('parameters', []):
        if parameters.get("parameter_code") == "T1_10M":

            data_items = json_normalize(parameters.get('data', []))

            if {'time', 'value'}.issubset(data_items.columns):
                data_items['time'] = pd.to_datetime(data_items['time'])
                data_items.set_index('time', inplace=True)

                data_resampled = data_items.resample('10min').mean()
                print(data_resampled)
                #hourly = data_resampled.resample('h').mean()
                hourly = data_resampled.resample('h', label='right',closed='right').mean().round(2)
                #hourly = data_items.resample('h').mean().round(2)

                #hourly.index = hourly.index.strftime('%Y-%m-%d %H:%M:%S')
                hourly = hourly.shift(0, freq='h')

                aggregated_data.append(hourly)
            else:
                print("required columns are not found")
print(aggregated_data)

if aggregated_data:
     aggregated_data_10m = pd.concat(aggregated_data)
     aggregated_data_10m.index = aggregated_data_10m.index.floor('h')
else:
     aggregated_data_10m = pd.DataFrame()

'''
aggregated_data = []
for station in data:
    for parameters in station['parameters']:
        if parameters.get("parameter_id") == "T1_10M":
            data_items = json_normalize(parameters['data'])
            if 'time' in data_items.columns and 'value' in data_items.columns:
                data_items['time'] = pd.to_datetime(data_items['time'])
                data_items.set_index('time', inplace=True)
                data_resampled = data_items.resample('10min').mean()
                data_resampled = round(data_resampled,2)
                aggregated_data_raw = data_resampled.resample('h').mean()
                aggregated_data.append(aggregated_data_raw)
                aggregated_data.index = aggregated_data_raw.index.strftime('%Y-%m-%d %H:%M:%S')
            else:
                print("required columns are not found")
            
        else:
            print("the data are not 10 minutes data")
'''


app = Flask(__name__)
@app.route("/")
def home():
    results = []
    #time = []
    value = []
    for station in data:
        for parameter in station.get("parameters",[]):
            if parameter.get("parameter_code") == "T1_1H": #T1_10M" or "TD.1_10M" or "RH.1_10M":
                for entry in parameter.get("data", []):
                    value.append({
                         "time" : pd.to_datetime(entry["time"]).floor('h'),
                         "value" : entry["value"]
                    })
                    #time.append(entry["time"])
                    #value.append(entry["value"])
    #time = pd.to_datetime(time)
    value_1h = pd.DataFrame(value)
    value_1h.set_index("time", inplace=True)

    for t_time, v_value in value_1h.iterrows():
                    if t_time not in aggregated_data_10m.index:
                         continue
                    
                    agg_value = aggregated_data_10m.loc[t_time, "value"]
                    api_value = v_value["value"]            
                    
                    #t_time = t_time.floor('H').strftime('%Y-%m-%d %H:%M:%S')
                    #if t_time in aggregated_data.index:
                        #agg_value = aggregated_data.loc[t_time, 'value']
                    #else: 
                         #continue
                    status = bool(round(agg_value,2) == round(api_value,2))
            
                    #results.append(parameter.get("parameter_code"))
                    #for entry in parameter.get("data",[]):
                    results.append({
                        "time" : t_time,
                        "aggregated_value" : round(agg_value,2),
                        "tss_value" : round(api_value,2),
                        "aggregation" : status,
                        #"value" : round(agg_value,2)
                        # "time" : entry.get("time"),
                        #"Value": round(entry.get("value"),2)
                        })
    return jsonify(results)

app.run()
