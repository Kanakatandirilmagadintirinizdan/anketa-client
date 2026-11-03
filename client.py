import requests

BASE = "http://127.0.0.1:5000"


class ServerNedostupen(Exception):
    """исключение при недоступности сервера или ошибке 500"""
    pass

def _zapros(metod, adres, **kwargs):
    """внутренняя функция для всех запросов к серверу"""
    try:
        r = requests.request(metod, BASE + adres, timeout=3, **kwargs)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        raise ServerNedostupen("сервер не отвечает или превышено время ожидания")

    if r.status_code >= 500:
        raise ServerNedostupen(f"ошибка на сервере: код {r.status_code}")
    return r

def vzyat_ankety():
    """запрашивает все анкеты с сервера"""
    r = _zapros("GET", "/anketi")
    return r.json()

def vzyat_anketu(nomer):
    """запрашивает одну анкету по номеру"""
    r = _zapros("GET", f"/anketi/{nomer}")
    if r.status_code == 404:
        return None
    return r.json()

def proverit_pochtu(mail):
    """отправляет почту на проверку серверу"""
    r = _zapros("POST", "/proverka", json={"mail": mail})
    return r.json().get("prinyato", False)

def vzyat_statistiku():
    """запрашивает статистику сервера"""
    r = _zapros("GET", "/statistika")
    return r.json()