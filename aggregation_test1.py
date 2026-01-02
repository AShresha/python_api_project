from datetime import datetime
import requests
import json
import pandas as pd
from pandas import json_normalize

token = str(input("Please enter the Token here"))

headers = {
    #token = str(input("Please enter the Token here"))
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

params = {
    "stations" : int(input("please enter the station number")),
    "parameters": str(input("please enter the parameters ids")),
    "date_from" : str(input("Enter the start date in the format 2025-12-26T00:00:00")),
    "date_to" : str(input("Enter the end date in the format 2025-12-26T00:00:00")),
    "show_qc": "undefined",
    "use_tag": "undefined",
    "tag_id": "undefined",
    "returnMetaData": "undefined"
}

url = "https://alpha.wscada.net/api/analysis/more"

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

#name = input("Hey, what is your name?").strip()
#mood = input(f"\n tell me {name} how are you feeling?").strip()

data = response.json()
#tp print the index of the data
df = pd.DataFrame(data)
#print(df.columns)

# to print the response of the API call in json format
#print(json.dumps(data, indent=1))

all_values = []
for station in data:
    for parameter in station["parameters"]:
        for entry in parameter["data"]:
            all_values.append(entry["value"])        

for value in all_values:
    print(round(value, 2))



#values = [entry["value"] for entry in data_dict["data"]]
#print(round(values, 2))
'''
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







