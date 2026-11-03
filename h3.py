import requests

BASE = "http://127.0.0.1:5000"
r = requests.get(BASE + "/anketi/99")

print("код ответа:", r.status_code)
print("r.ok:", r.ok)
print("текст ошибки:", r.json()["oshibka"])