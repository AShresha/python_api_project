
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

    return aggregated_data