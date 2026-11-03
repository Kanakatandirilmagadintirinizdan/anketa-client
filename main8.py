import json
import os
from people import Student, Teacher, AnketaError
import client
import registry


def obrabotat_dannye(ankety, base_dir):
    """превращает словари с сервера в объекты, собирает брак"""
    prinyato = []
    brak = []

    for item in ankety:
        try:
            tip = item.get("tip")
            if tip == "s":
                obj = Student(item["fio"], item["mail"], item["phone"], item["gruppa"])
            elif tip == "t":
                obj = Teacher(item["fio"], item["mail"], item["phone"], item["kafedra"])
            else:
                raise AnketaError(f"неизвестный тип: {tip}")
            prinyato.append(obj)
        except AnketaError as e:
            nomer = item.get("nomer", "?")
            brak.append((nomer, str(item), str(e)))
    return prinyato, brak


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ankety = []
    source = ""

    print("--- ЗАГРУЗКА ДАННЫХ ---")
    try:
        ankety = client.vzyat_ankety()
        source = "сервер"
        print("данные успешно получены с сервера.")
    except client.ServerNedostupen as e:
        print(f"ошибка: сервер недоступен ({e})")
        print("перехожу на запасной источник (файл anketa.txt)...")

        file_path = os.path.join(base_dir, "anketa.txt")
        if os.path.exists(file_path):
            reg = registry.Registry()
            reg.load(file_path)
            for p in reg.people:
                ankety.append({
                    "tip": "s" if isinstance(p, Student) else "t",
                    "fio": p.fio, "mail": p.mail, "phone": p.phone,
                    "gruppa": p.group if isinstance(p, Student) else "",
                    "kafedra": p.department if isinstance(p, Teacher) else "",
                    "nomer": "-"
                })
            source = "файл"
            print("данные успешно загружены из файла.")
        else:
            print("критическая ошибка: нет ни сервера, ни файла anketa.txt")
            return

    prinyato, brak = obrabotat_dannye(ankety, base_dir)
    prinyato.sort(key=lambda x: x.fio)

    print(f"\n--- РЕЗУЛЬТАТЫ (источник: {source}) ---")
    print(f"{'№':<3} | {'ФИО':<25} | {'Роль':<15} | {'Телефон':<15}")
    print("-" * 65)
    for i, p in enumerate(prinyato, 1):
        print(f"{i:<3} | {p.fio:<25} | {p.role():<15} | {p.masked_phone():<15}")

    print(f"\nПринято: {len(prinyato)} | Отклонено: {len(brak)}")

    if brak:
        print("\nСписок отклоненных:")
        for num, line, reason in brak:
            print(f"  запись {num}: {reason}")

    # Статистика
    moja_stat = {}
    for p in prinyato:
        moja_stat[p.role()] = moja_stat.get(p.role(), 0) + 1
    print("\nМоя статистика по ролям:", moja_stat)

    server_stat = None
    if source == "сервер":
        try:
            server_stat = client.vzyat_statistiku()
            print("Статистика сервера:", server_stat)
        except client.ServerNedostupen:
            print("не удалось получить статистику сервера")

    # Отправка почты на проверку
    print("\n--- ПРОВЕРКА ПОЧТЫ НА СЕРВЕРЕ ---")
    for p in prinyato:
        if source == "сервер":
            try:
                res = client.proverit_pochtu(p.mail)
                print(f"{p.mail} -> сервер ответил: {res}")
            except client.ServerNedostupen:
                print(f"{p.mail} -> проверка не удалась (сервер недоступен)")
        else:
            print(f"{p.mail} -> проверка пропущена (сервер недоступен)")

    # Сохранение в JSON
    otchet = {
        "istochnik": source,
        "prinyato_kolvo": len(prinyato),
        "otkloneno_kolvo": len(brak),
        "moja_statistika": moja_stat,
        "statistika_servera": server_stat,
        "prinyatye_ankety": [{"fio": p.fio, "role": p.role()} for p in prinyato],
        "brak": [{"nomer": b[0], "prichina": b[2]} for b in brak]
    }

    json_path = os.path.join(base_dir, "otchet.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(otchet, f, ensure_ascii=False, indent=4)
    print(f"\nИтог сохранен в файл: otchet.json")


if __name__ == "__main__":
    main()