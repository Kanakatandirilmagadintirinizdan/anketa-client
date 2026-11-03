import pytest
from people import Person, Student, Teacher, AnketaError

# --- Тесты ФИО ---
@pytest.mark.parametrize("raw, expected", [
    ("иванов иван", "Иванов Иван"),
    (" петров пётр ", "Петров Пётр"),
    ("СИДОРОВА АННА", "Сидорова Анна"),
    ("петров-водкин кузьма", "Петров-Водкин Кузьма") # Ошибка 1
])
def test_check_fio(raw, expected):
    assert Person.check_fio(raw) == expected

def test_check_fio_oshibka():
    with pytest.raises(AnketaError):
        Person.check_fio("Иванов")

# --- Тесты Почты ---
@pytest.mark.parametrize("raw, expected", [
    ("IVAnov@Mail.Ru", "ivanov@mail.ru"),
    ("test@yandex.ru", "test@yandex.ru")
])
def test_check_email(raw, expected):
    assert Person.check_email(raw) == expected

@pytest.mark.parametrize("bad_email", [
    "kuznetsov.mail.ru",
    "test@mail",
    "test@.ru",
    "test@mail.",
    "iv anov@mail.ru" # Ошибка 2
])
def test_check_email_oshibka(bad_email):
    with pytest.raises(AnketaError):
        Person.check_email(bad_email)

# --- Тесты Телефона ---
@pytest.mark.parametrize("raw, expected", [
    ("+7 (921) 111-22-33", "79211112233"),
    ("89217654321", "79217654321"), # <-- ИСПРАВИТЬ ЗДЕСЬ
    ("8 921 111 22 33", "79211112233"),
    ("79211112233", "79211112233")
])
def test_check_phone(raw, expected): # <-- добавили expected
    assert Person.check_phone(raw) == expected # <-- сравниваем с expected

@pytest.mark.parametrize("bad_phone", [
    "123",
    "99217654321",
    "+7 (921) 111-22-3"
])
def test_check_phone_oshibka(bad_phone):
    with pytest.raises(AnketaError):
        Person.check_phone(bad_phone)

# --- Тесты методов ---
def test_short_fio():
    p = Student("Иванов Иван Петрович", "ivanov@mail.ru", "79211112233", "09c33")
    assert p.short_fio() == "Иванов И. П." # <-- ИСПРАВИТЬ ЗДЕСЬ (пробел)

def test_short_fio():
    p = Student("Иванов Иван Петрович", "ivanov@mail.ru", "79211112233", "09c33")
    assert p.short_fio() == "Иванов И. П."  # <-- вот здесь нужен пробел!

def test_roles():
    s = Student("Иванов Иван", "ivanov@mail.ru", "79211112233", "09c33")
    t = Teacher("Петров Пётр", "petrov@voenmeh.ru", "79211112233", "Кафедра И9")
    assert s.role() == "студент"
    assert t.role() == "преподаватель"

def test_student_no_group():
    with pytest.raises(AnketaError):
        Student("Иванов Иван", "ivanov@mail.ru", "79211112233", " ")

# --- Ошибка 3: Сортировка по Ё ---
def test_sort_with_yo():
    s1 = Student("Ёлкин Иван", "e@mail.ru", "79211112233", "09c33")
    s2 = Student("Абрамов Пётр", "a@mail.ru", "79211112233", "09c33")
    s3 = Student("Яковлев Антон", "y@mail.ru", "79211112233", "09c33")
    people = sorted([s1, s2, s3])
    assert [p.fio for p in people] == ["Абрамов Пётр", "Ёлкин Иван", "Яковлев Антон"]