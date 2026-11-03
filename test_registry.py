import pytest
from registry import Registry

# Данные для фикстуры: 3 правильные и 3 бракованные строки
STROKI = """s;иванов иван;ivanov@mail.ru;+79211112233;09c33
t;петров пётр;petrov@voenmeh.ru;89217654321;Кафедра И9
s;петрова анна;petrova@yandex.ru;89217654321;09c33
s;сидоров;sidorov@mail.ru;+79210000000;09c34
x;непонятный тип;a@b.ru;89211112233;что-то
t;орлов игорь;orlov@voenmeh.ru;89219990811;"""

@pytest.fixture
def reg(tmp_path):
    # Создаем временный файл и загружаем в него данные
    f = tmp_path / "anketa.txt"
    f.write_text(STROKI, encoding="utf-8")
    r = Registry()
    r.load(f)
    return r

def test_empty_registry():
    assert len(Registry()) == 0

def test_load_count(reg):
    assert len(reg) == 3

def test_rejected_count(reg):
    assert len(reg.rejected) == 3

def test_file_not_found():
    # Проверка, что если файла нет, возвращается False
    assert Registry().load("net.txt") is False

def test_roles_stats(reg):
    stats = {}
    for p in reg.people:
        stats[p.role()] = stats.get(p.role(), 0) + 1
    assert stats == {"студент": 2, "преподаватель": 1}

def test_save_ok(reg, tmp_path):
    out_file = tmp_path / "ok.txt"
    # Сохраняем, игнорируя файл ошибок
    reg.save(out_file, tmp_path / "err.txt")
    # Проверяем, что записалось ровно 3 строки (по одной на человека)
    assert len(out_file.read_text(encoding="utf-8").strip().split("\n")) == 3

def test_sorting(reg):
    # Проверяем, что сортировка по ФИО работает (Иванов идет первым)
    names = [p.fio for p in sorted(reg.people)]
    assert names[0] == "Иванов Иван"