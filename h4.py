import requests

BASE = "http://127.0.0.1:5000"
r = requests.get(BASE + "/anketi", params={"tip": "t"})

print("адрес запроса:", r.url)
for a in r.json():
    print(f"фио: {a['fio']} | кафедра: {a['kafedra']}")