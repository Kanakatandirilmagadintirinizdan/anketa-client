import requests

BASE = "http://127.0.0.1:5000"
r = requests.get(BASE + "/")

print("код ответа:", r.status_code)
print("тип r.text:", type(r.text))
print("тип r.json():", type(r.json()))
print("название сервиса:", r.json()["servis"])