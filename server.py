"""Учебный сервер анкет. Запускается локально, интернет не нужен.

Запуск:  python server.py
Адрес:   http://127.0.0.1:5000

Эндпоинты:
  GET  /                      короткая справка
  GET  /anketi                все анкеты списком
  GET  /anketi?tip=s          только студенты (или tip=t — преподаватели)
  GET  /anketi/<nomer>        одна анкета по номеру
  GET  /statistika            сводка по ролям
  POST /proverka              принять анкету на проверку, вернуть результат
  GET  /slomannyy             намеренно отвечает кодом 500
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

ANKETI = [
    {"nomer": 1, "tip": "s", "fio": "Иванов Иван Петрович",
     "mail": "ivanov@mail.ru", "phone": "79211112233", "gruppa": "09с33"},
    {"nomer": 2, "tip": "t", "fio": "Петров Пётр Сергеевич",
     "mail": "petrov@voenmeh.ru", "phone": "79217654321", "kafedra": "И9"},
    {"nomer": 3, "tip": "s", "fio": "Сидорова Анна Олеговна",
     "mail": "sidorova@yandex.ru", "phone": "79219998877", "gruppa": "09с34"},
    {"nomer": 4, "tip": "s", "fio": "Кузнецов Павел Егорович",
     "mail": "kuznetsov.mail.ru", "phone": "79211234567", "gruppa": "09с34"},
    {"nomer": 5, "tip": "t", "fio": "Смирнова Ольга",
     "mail": "smirnova@inbox.ru", "phone": "7921123", "kafedra": "И4"},
    {"nomer": 6, "tip": "s", "fio": "Морозова Екатерина Игоревна",
     "mail": "morozova@mail.ru", "phone": "79215554433", "gruppa": "09с35"},
]


@app.route("/")
def spravka():
    return jsonify({
        "servis": "учебный сервер анкет",
        "adresa": ["/anketi", "/anketi/<nomer>", "/statistika",
                   "/proverka (POST)", "/slomannyy"],
    })


@app.route("/anketi")
def spisok():
    tip = request.args.get("tip")
    if tip is None:
        return jsonify(ANKETI)
    if tip not in ("s", "t"):
        return jsonify({"oshibka": "tip может быть только s или t"}), 400
    return jsonify([a for a in ANKETI if a["tip"] == tip])


@app.route("/anketi/<int:nomer>")
def odna(nomer):
    for a in ANKETI:
        if a["nomer"] == nomer:
            return jsonify(a)
    return jsonify({"oshibka": "анкета не найдена", "nomer": nomer}), 404


@app.route("/statistika")
def statistika():
    stat = {}
    for a in ANKETI:
        rol = "студент" if a["tip"] == "s" else "преподаватель"
        stat[rol] = stat.get(rol, 0) + 1
    return jsonify({"vsego": len(ANKETI), "po_rolyam": stat})


@app.route("/proverka", methods=["POST"])
def proverka():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"oshibka": "ожидался JSON"}), 400
    mail = data.get("mail", "")
    if mail.count("@") == 1 and "." in mail.split("@")[-1]:
        return jsonify({"prinyato": True, "mail": mail}), 201
    return jsonify({"prinyato": False, "prichina": "почта неверная"}), 200


@app.route("/slomannyy")
def slomannyy():
    raise RuntimeError("так выглядит ошибка на стороне сервера")


if __name__ == "__main__":
    app.run(port=5000)
