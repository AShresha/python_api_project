from datetime import datetime
import requests
import json

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

url = "https://aws.wscada.net/api/observation"

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

#name = input("Hey, what is your name?").strip()
#mood = input(f"\n tell me {name} how are you feeling?").strip()

data = response.json()

with open("Data_test1.json", "a", encoding = "utf-8") as file:
    entry = {
        "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #"name" : name,
        #"mood" : mood
        "data" : data
    }

    file.write(json.dumps(entry, indent=1) + "\n")
    #file.write(json.dumps(data, indent=1))

#print(f"\n {name}, you feeling {mood}")
print(json.dumps(data, indent=1))









