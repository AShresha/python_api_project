import requests

#-------------
# ID = input("enter the parameter id: ")
# API_URL = f"https://alpha.wscada.net/api/station/791/data-series/{ID}"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjIiLCJyb2xlX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwibmFtZSI6ImFkbWluIiwiZGVzaWduYXRpb24iOiJBZG1pbmlzdHJhdG9yIiwiZW1haWwiOiJhZG1pbkBydHMuY29tLm5wIiwicGVybWlzc2lvbnMiOlsidmlldyB1bml0IiwidmlldyBxYy1ydWxlIiwibW9kaWZ5IHFjLXJ1bGUiLCJ2aWV3IG1ldGEtZGF0YSIsIm1vZGlmeSBtZXRhLWRhdGEiLCJ2aWV3IGRhdGEtc291cmNlIiwibW9kaWZ5IGRhdGEtc291cmNlIiwidmlldyB1c2VyIiwibW9kaWZ5IHVzZXIiLCJ2aWV3IGVkaXQtb2JzZXJ2YXRpb24iLCJtb2RpZnkgZWRpdC1vYnNlcnZhdGlvbiIsInZpZXcgZGF0YS1vcmlnaW4tcGFyYW1ldGVyIiwibW9kaWZ5IGRhdGEtb3JpZ2luLXBhcmFtZXRlciIsInZpZXcgZm9sZGVyIiwibW9kaWZ5IGZvbGRlciIsInZpZXcgc3RhdGlvbiIsIm1vZGlmeSBzdGF0aW9uIiwidmlldyBwZXJtaXNzaW9uIiwibW9kaWZ5IHBlcm1pc3Npb24iLCJ2aWV3IGRhdGEtc2VyaWVzIiwibW9kaWZ5IGRhdGEtc2VyaWVzIiwidmlldyBwYXJhbWV0ZXItdHlwZSIsIm1vZGlmeSBwYXJhbWV0ZXItdHlwZSIsInZpZXcgcGFyYW1ldGVyIiwibW9kaWZ5IHBhcmFtZXRlciIsInZpZXcgZGF0YS1vcmlnaW4iLCJtb2RpZnkgZGF0YS1vcmlnaW4iLCJ2aWV3IHJvbGUiLCJtb2RpZnkgcm9sZSIsInZpZXcgcWMtY2hlY2siLCJtb2RpZnkgcWMtY2hlY2siLCJ2aWV3IG1haW50ZW5hbmNlIiwibW9kaWZ5IG1haW50ZW5hbmNlIiwidmlldyB0YWciLCJtb2RpZnkgdGFnIiwidmlldyBpbnZlbnRvcnkiLCJtb2RpZnkgaW52ZW50b3J5IiwidmlldyBhbmFseXNpcyIsIm1vZGlmeSBhbmFseXNpcyIsInZpZXcgZGFxIiwibW9kaWZ5IGRhcSIsInZpZXcgZGFxLXByb2Nlc3NvciIsIm1vZGlmeSBkYXEtcHJvY2Vzc29yIiwidmlldyBtZXRhLWRhdGEtdGVtcGxhdGUiLCJtb2RpZnkgbWV0YS1kYXRhLXRlbXBsYXRlIiwidmlldyBoeWRyb2xvZ3kiLCJtb2RpZnkgaHlkcm9sb2d5IiwidmlldyBpZGFxIiwibW9kaWZ5IGlkYXEiLCJ2aWV3IGltYWdlcyIsIm1vZGlmeSBpbWFnZXMiLCJ2aWV3IHRvb2xzIiwibW9kaWZ5IHRvb2xzIiwidmlldyBjb25maWd1cmF0aW9ucyIsInZpZXcgZGF0YS1kZWxpdmVyeSJdLCJjbGllbnRpcCI6IjE5Mi4xNjguNC4xNTgiLCJpYXQiOjE3ODgzNDI1MzQsImV4cCI6MTc4ODQyODkzNH0.2AeM1V6VfJxnAWQqyDRC5qsdD785JOm9DB4WPm7S1U0"
API_URL = "https://alpha.wscada.net/api/station/791"
#-------------


#---------
headers = {
    "Accept": "application/json",
    "Control-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}


payload = {
    "id": 791,
    "identifier": "10000791",
    "name": "to delete mine",
    "folder_name": "Landslide Early Warning Testing @ RTS",
    # "longitude": null,
    # "latitude": null,
    # "elevation": null,
    "description": "to delete mine",
    "folder_id": "4",
    # "meta_data_template_id": null,
    # "location_id": null,
    # "station_type_id": null,
    # "meta_data": null,
    # "data_source": null,
    # "images": null,
    # "tags": null
}
# payload = {
    # "ids": [f"{ID}"]
# }

response = requests.delete(
    API_URL,
    headers = headers,
    json = payload
)

#-----------

print("Status:", response.status_code)
print("Response:")

try:
    print(response.json())
except ValueError:
    print(response.text)


