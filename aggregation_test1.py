from datetime import datetime
import requests
import json
import pandas as pd
from pandas import json_normalize

second_parameter_id_alpha = {
    "T_1H" : 726,
    "RH_1H" : 1648,
    "TD_1H" : 1652,
    "ST_5" : 569,
    "ST_10" : 596,
    "ST_20" : 830,
    "ST_30" : 930,
    "SM_5" : 102,
    "SM_10" : 103,
    "SM_20" : 104,
    "SM_30" : 105,
    "SR_10M" : 106,
    "PCPN" : 1
}

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

data = response.json()
#print the index of the data
df = pd.DataFrame(data)
#print(df.columns)

# to print the response of the API call in json format
#print(json.dumps(data, indent=1))


for station in data:
    for parameters in station['parameters']:
        data_items = json_normalize(parameters['data']) #flatten the 'data' field if its nested and check the structure
            #print(data_items.head())
        if 'time' in data_items.columns and 'value' in data_items.columns:
            #Convert datetime to pandas datetime object
            data_items['time'] = pd.to_datetime(data_items['time'])
    #setting datetime as index
            data_items.set_index('time', inplace=True)
    #resampling the data every 10 minute
            data_resampled = data_items.resample('10min').mean()
            data_resampled = round(data_resampled,2)
    
    #grouping the hourly intervals and calculating the aveage for each hour
            aggregated_data = data_resampled.resample('h').mean()

    #shifting the result to allign with the next hour
            aggregated_data = aggregated_data.shift(0, freq='h')

    #Convert the index(timestamps) to string format for json serialization
            aggregated_data.index =  aggregated_data.index.strftime('%Y-%m-%d %H:%M:%S')
    #print the aggregated data
                #print(json.dumps(aggregated_data.to_dict(orient='index'),indent=1))
        else: 
            print("required columns {datetime and value} are not found")
print(json.dumps(aggregated_data.to_dict(orient='index'),indent=1))

print(json.dumps(second_parameter_id_alpha, indent = 4))

second_parameter_id_alpha_num = int(input(f"which parameter you want to aggregate "))

ten_minutevalue = []
for stationten in data:
    for parameterten in stationten["parameters"]:
        if parameterten["parameter_id"] == second_parameter_id_alpha_num:
            for entry_ten in parameterten["data"]:
                ten_minutevalue.append(entry_ten["value"])

for valueten in ten_minutevalue:
       print(round(valueten,2))
       #if valueten in aggregated_data['value']:
       if (aggregated_data['value'].round(2) == round(valueten,2)).any():
           print("aggregation is okay")
       else:
           print("aggregation not okay")
        
           

