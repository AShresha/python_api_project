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
print(json.dumps(data, indent=1))
#print(json.dumps(aggregated_data.to_dict(orient='index', indent=1)))


if 'data' in data:
    data_items = json_normalize(data['data'])
    print(data_items.head())
else:
    print("No 'data' key found in the response")


if 'datetime' in data_items.columns and 'value' in data_items.columns:
    data_items['datetime'] = pd.to_datetime(data_items['datetime'])

    data_items.set_index('datetime', inplace=True)

    data_resampled = data_items.resample('10min').mean()

    aggregated_data = data_resampled.resample('h').mean()

    aggregated_data = aggregated_data.shift(1, freq='h')

    aggregated_data.index =  aggregated_data.index.strftime('%Y-%m-%d %H:%M:%S')
    print(json.dumps(aggregated_data.to_dict(orient='index'),indent=1))
else:
    print("required columns {datetime and value} are not found")








