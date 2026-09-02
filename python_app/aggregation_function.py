from datetime import datetime
import requests
import json
import os
import pandas as pd
from pandas import json_normalize
from flask import Flask, request, jsonify


def run_analysis(token, station, param_ids, date_from, date_to):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    params = {
        "stations": station,
        "parameters": ",".join(map(str, param_ids)),
        "date_from": date_from,
        "date_to": date_to,
        "show_qc": "undefined",
        "use_tag": "undefined",
        "tag_id": "undefined",
        "returnMetaData": "undefined"
    }

    url = "https://alpha.wscada.net/api/analysis/more"

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()


    # ---- your processing logic here ----
    aggregated_data = []

    for station in data:
        for parameters in station.get('parameters', []):
            if parameters.get("parameter_code") == "T_10M":

                df = json_normalize(parameters.get('data', []))

                if {'time', 'value'}.issubset(df.columns):
                    df['time'] = pd.to_datetime(df['time'])
                    df.set_index('time', inplace=True)

                    resampled = df.resample('10min').mean()
                    hourly = resampled.resample('h', label='right', closed='right').mean().round(2)

                    aggregated_data.append(hourly)

    if aggregated_data:
        aggregated_data = pd.concat(aggregated_data)
        aggregated_data.index = aggregated_data.index.floor('h')
    else:
        aggregated_data = pd.DataFrame()


    results = []
    #time = []
    value = []
    for station in data:
        for parameter in station.get("parameters",[]):
            if parameter.get("parameter_code") == "T_1H": #T1_10M" or "TD.1_10M" or "RH.1_10M":# need to change for different 10 minutes data
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
                    if t_time not in aggregated_data.index:
                         continue
                    
                    agg_value = aggregated_data.loc[t_time, "value"]
                    api_value = v_value["value"]            
                    
                    #t_time = t_time.floor('H').strftime('%Y-%m-%d %H:%M:%S')
                    #if t_time in aggregated_data.index:
                        #agg_value = aggregated_data.loc[t_time, 'value']
                    #else: 
                         #continue
                    status = bool(round(agg_value,2) == round(api_value,2))
            
                    #results.append(parameter.get("parameter_code"))
                    #for entry in parameter.get("data",[]):
                    #results.append({
                        #"time" : t_time,
                        #"aggregated_value" : round(agg_value,2),
                        #"tss_value" : round(api_value,2),
                        #"aggregation" : status,
                        #"value" : round(agg_value,2)
                        # "time" : entry.get("time"),
                        #"Value": round(entry.get("value"),2)
                        #})
                    if status == False:
                        results.append({
                            "time" : t_time,
                            "Aggregated Value" : round(agg_value, 2),
                            "tss_value" : round(api_value,2)
                        })
    results = pd.DataFrame(results)
    return results
    #return jsonify(results)


    #return aggregated_data