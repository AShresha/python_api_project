import requests

#-------------

API_URL = "https://aws.wscada.net/daq/origin-parameter-template"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjcyIiwicm9sZV9pZCI6MSwidXNlcm5hbWUiOiJhbmltYS5zaHJlc3RoYUBydHMuY29tLm5wIiwibmFtZSI6IkFuaW1hIFNocmVzdGhhIiwiZGVzaWduYXRpb24iOm51bGwsImVtYWlsIjoiYW5pbWEuc2hyZXN0aGFAcnRzLmNvbS5ucCIsInBlcm1pc3Npb25zIjpbInZpZXcgdW5pdCIsIm1vZGlmeSB1bml0IiwidmlldyBxYy1ydWxlIiwibW9kaWZ5IHFjLXJ1bGUiLCJ2aWV3IG1ldGEtZGF0YSIsIm1vZGlmeSBtZXRhLWRhdGEiLCJ2aWV3IGRhdGEtc291cmNlIiwibW9kaWZ5IGRhdGEtc291cmNlIiwidmlldyB1c2VyIiwibW9kaWZ5IHVzZXIiLCJ2aWV3IGVkaXQtb2JzZXJ2YXRpb24iLCJtb2RpZnkgZWRpdC1vYnNlcnZhdGlvbiIsInZpZXcgZGF0YS1vcmlnaW4tcGFyYW1ldGVyIiwibW9kaWZ5IGRhdGEtb3JpZ2luLXBhcmFtZXRlciIsInZpZXcgZm9sZGVyIiwibW9kaWZ5IGZvbGRlciIsInZpZXcgc3RhdGlvbiIsIm1vZGlmeSBzdGF0aW9uIiwidmlldyBwZXJtaXNzaW9uIiwibW9kaWZ5IHBlcm1pc3Npb24iLCJ2aWV3IGRhdGEtc2VyaWVzIiwibW9kaWZ5IGRhdGEtc2VyaWVzIiwidmlldyBwYXJhbWV0ZXItdHlwZSIsIm1vZGlmeSBwYXJhbWV0ZXItdHlwZSIsInZpZXcgcGFyYW1ldGVyIiwibW9kaWZ5IHBhcmFtZXRlciIsInZpZXcgZGF0YS1vcmlnaW4iLCJtb2RpZnkgZGF0YS1vcmlnaW4iLCJ2aWV3IHJvbGUiLCJtb2RpZnkgcm9sZSIsInZpZXcgcWMtY2hlY2siLCJtb2RpZnkgcWMtY2hlY2siLCJ2aWV3IHRhZyIsIm1vZGlmeSB0YWciLCJ2aWV3IGludmVudG9yeSIsIm1vZGlmeSBpbnZlbnRvcnkiLCJ2aWV3IGFuYWx5c2lzIiwibW9kaWZ5IGFuYWx5c2lzIiwidmlldyBkYXEiLCJtb2RpZnkgZGFxIiwidmlldyBkYXEtcHJvY2Vzc29yIiwibW9kaWZ5IGRhcS1wcm9jZXNzb3IiXSwiY2xpZW50aXAiOiIxNzIuMTkuMC4xIiwiaWF0IjoxNzg4MjM2MjAzLCJleHAiOjE3ODgzMjI2MDN9.EQWQhEUEti4Nn4KBv5Mt5R9no6FyX8z2i1u3kE-2x94"
new_template_name = "Displacement sensor with CDCP"

#-------------
"""
parameters = [
    {"parameter_id": 583, "code": "131"},
    {"parameter_id": 586, "code": "133"},
    {"parameter_id": 453, "code": "1"},
    {"parameter_id": 28, "code": "14"},
    {"parameter_id": 696, "code": "FV"},
    {"parameter_id": 695, "code": "IMEI"},
    {"parameter_id": 48, "code": "71"},
    {"parameter_id": 46, "code": "73"},
    {"parameter_id": 527, "code": "786"},
    {"parameter_id": 528, "code": "755"},
    {"parameter_id": 784, "code": "860"},
    {"parameter_id": 783, "code": "920"},
    {"parameter_id": 529, "code": "791"},
    {"parameter_id": 530, "code": "760"},
    {"parameter_id": 531, "code": "796"},
    {"parameter_id": 532, "code": "765"},
    {"parameter_id": 533, "code": "781"},
    {"parameter_id": 534, "code": "750"},
    {"parameter_id": 535, "code": "831"},
    {"parameter_id": 536, "code": "770"},
    {"parameter_id": 516, "code": "788"},
    {"parameter_id": 515, "code": "757"},
    {"parameter_id": 780, "code": "862"},
    {"parameter_id": 779, "code": "922"},
    {"parameter_id": 517, "code": "762"},
    {"parameter_id": 518, "code": "793"},
    {"parameter_id": 519, "code": "798"},
    {"parameter_id": 520, "code": "767"},
    {"parameter_id": 521, "code": "752"},
    {"parameter_id": 522, "code": "783"},
    {"parameter_id": 524, "code": "833"},
    {"parameter_id": 523, "code": "772"},
    {"parameter_id": 852, "code": "15"},
    {"parameter_id": 694, "code": "SYS"},
    {"parameter_id": 330, "code": "101"},
    {"parameter_id": 366, "code": "89"}, 
    {"parameter_id": 693, "code": "UDI"}   

]
"""

parameters = [
    {"parameter_id": 649, "code": "480"},
    {"parameter_id": 28, "code": "14"},
    {"parameter_id": 696, "code": "FV"},
    {"parameter_id": 695, "code": "IMEI"},
    {"parameter_id": 48, "code": "71"},
    {"parameter_id": 46, "code": "73"},
    {"parameter_id": 852, "code": "15"},
    {"parameter_id": 694, "code": "SYS"},
    {"parameter_id": 330, "code": "101"},
    {"parameter_id": 366, "code": "89"}, 
    {"parameter_id": 693, "code": "UDI"}   

]


#---------
headers = {
    "Accept": "application/json",
    "Control-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}


payload = {
    "name": new_template_name,
    "parameters": parameters
}

response = requests.post(
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