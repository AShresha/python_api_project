from datetime import datetime
import requests
import json
import os
import pandas as pd
from pandas import json_normalize
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route("/aggregate")
def aggregate():
    # to get the token from the servers
    token = request.args.get("token")
    station = request.args.get("station")
    param_id = request.args.get("param_id")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    if not all([token, station,param_id, date_from, date_to]):
        return jsonify({"error": "missing parameters"}),400
    
    station = int(station)
    param_id =int(param_id)

    headers = {
        "Authorization" : f"Bearer {token}",
        "Accept": "application/json"
    }

    params = {
        "stations" : station,
        "parameters" : param_id,
        "date_from" : date_from,
        "date_to" : date_to,
        "show-qc" : "undefined",
        "use_tag": "undefined",
        "tag_id" : "undefined",
        "returnMetaData":"undefined"
    }

    url = "https://alpha.wscada.net/api/analysis/more"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    for station_data_1 in data:
        for parameters_data_1 in station_data_1['parameters']:
            data_items = json_normalize(parameters_data_1['data']) #flatten the 'data' field if its nested and check the structure
            #print(data_items.head())
            #if 'datetime' in data_items.columns and 'value' in data_items.columns: # for observation table
            if 'time' in data_items.columns and 'value' in data_items.columns:
                #Convert datetime to pandas datetime object
                data_items['time'] = pd.to_datetime(data_items['time'])
                #setting datetime as index
                data_items.set_index('time', inplace=True)
                #resampling the data every 10 minute
                data_resampled = data_items.resample('10min').mean()
                data_resampled = round(data_resampled,2)
    
                #grouping the hourly intervals and calculating the aveage for each hour
                #aggregated_data = data_resampled.resample('h').mean()
                aggregated_data = data_resampled.resample('h',label='right',closed='right').mean()

                #shifting the result to allign with the next hour
                aggregated_data = aggregated_data.shift(0, freq='h')

                #Convert the index(timestamps) to string format for json serialization
                aggregated_data.index =  aggregated_data.index.strftime('%Y-%m-%d %H:%M:%S')
                #print the aggregated data
                #print(json.dumps(aggregated_data.to_dict(orient='index'),indent=1))
            else: 
                print("required columns {datetime and value} are not found")

    

    ten_minute_time = []
    ten_minute_value = []

    for station_data in data:
        for param_data in station_data.get("parameters", []):
            if param_data.get("parameter_id") == param_id:
                for entry in param_data.get("data",[]):
                    ten_minute_time.append(pd.to_datetime(entry["time"]))
                    ten_minute_value.append(entry["value"])

    if not ten_minute_value:
        return jsonify({"error":"there are no data"}),404
    

    results = []
    
    for valueten, valuetime in zip(ten_minute_value, ten_minute_time):
        hour_time = valuetime.ceil('h').strftime('%Y-%m-%d %H:%M:%S')

        if hour_time in aggregated_data.index:
            agg_value = aggregated_data.loc[hour_time, 'value']
            status = bool(round(agg_value, 2) == round(valueten, 2))
        else:
            status = False

        results.append({
            "time": hour_time,
            "value": round(valueten, 2),
            "aggregation": status
         })
    return jsonify(results)


if __name__=="__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
    #pass
    #app.run(debug=True)





'''

#token = str(input("Please enter the Token here"))

headers = {
    #token = str(input("Please enter the Token here"))
    "Authorization": f"Bearer{token}",
    "Accept": "application/json"
}

params = {
    "series_id" : int(input("Please enter the data series")),
    "date_from" : str(input("Enter the start date in the format 2025-12-26T00:00:00")),
    "date_to" : str(input("Enter the end date in the format 2025-12-26T00:00:00"))
}

url = "https://alpha.wscada.net/api/observation"

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

#name = input("Hey, what is your name?").strip()
#mood = input(f"\n tell me {name} how are you feeling?").strip()

data = response.json()

df = pd.DataFrame(data)
print(df.columns)

#df['datetime'] = pd.to_datetime(df['datetime'])

#df.set_index('datetime', inplace=True)

#aggregated_data = df.resample('H').mean()
'''

'''
with open("Aggregated_Data.json", "a", encoding = "utf-8") as file:
    entry = {
        "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #"name" : name,
        #"mood" : mood
        #"data" : aggregated_data.to_dict(orient='index')
        #"data" : data
    }
    file.write(json.dumps(entry, indent=1) + "\n")
    #file.write(json.dumps(data, indent=1))

#print(f"\n {name}, you feeling {mood}")
'''
'''
# prints out the structure od the data to inspect
print(json.dumps(data, indent=1))
#print(json.dumps(aggregated_data.to_dict(orient='index', indent=1)))

#to check whether the 'data' contains the key we need, extracting and normalizing it
if 'data' in data:
    data_items = json_normalize(data['data']) #flatten the 'data' field if its nested and check the structure
    print(data_items.head())
else:
    print("No 'data' key found in the response")

#check for 'datetime and value' columns

if 'datetime' in data_items.columns and 'value' in data_items.columns:
    #Convert datetime to pandas datetime object
    data_items['datetime'] = pd.to_datetime(data_items['datetime'])
    #setting datetime as index
    data_items.set_index('datetime', inplace=True)
    #resampling the data every 10 minute
    data_resampled = data_items.resample('10min').mean()
    
    #grouping the hourly intervals and calculating the aveage for each hour
    aggregated_data = data_resampled.resample('h').mean()

    #shifting the result to allign with the next hour
    aggregated_data = aggregated_data.shift(1, freq='h')

    #Convert the index(timestamps) to string format for json serialization
    aggregated_data.index =  aggregated_data.index.strftime('%Y-%m-%d %H:%M:%S')
    #print the aggregated data
    print(json.dumps(aggregated_data.to_dict(orient='index'),indent=1))
else:
    print("required columns {datetime and value} are not found")

'''