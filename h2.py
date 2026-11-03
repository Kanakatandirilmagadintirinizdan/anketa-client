import requests

BASE = "http://127.0.0.1:5000"
r = requests.get(BASE + "/anketi")
ankety = r.json()

print("пришло анкет:", len(ankety))
print("фио первой:", ankety[0]["fio"])