import requests

BASE = "http://127.0.0.1:5000"
mails = ["ivanov@mail.ru", "kuznetsov.mail.ru"]

for m in mails:
    r = requests.post(BASE + "/proverka", json={"mail": m})
    print(f"почта: {m} | код: {r.status_code} | принято: {r.json().get('prinyato')}")