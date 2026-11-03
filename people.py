class AnketaError(Exception):
    """Анкета не прошла проверку."""
    pass

class Person:
    def __init__(self, fio, mail, phone):
        self.fio = self.check_fio(fio)
        self.mail = self.check_email(mail)
        self.phone = self.check_phone(phone)

    @staticmethod
    def check_fio(raw_fio):
        parts = raw_fio.split()
        if len(parts) < 2:
            raise AnketaError("в ФИО меньше двух слов")
        res_parts = []
        for p in parts:
            res_parts.append("-".join([word.capitalize() for word in p.split("-")]))
        return " ".join(res_parts)

    @staticmethod
    def check_email(raw_email):
        email = raw_email.strip().lower()
        if " " in email:
            raise AnketaError(f"неверный формат почты: {raw_email}")
        if email.count("@") != 1:
            raise AnketaError(f"неверный формат почты: {raw_email}")
        name, domain = email.split("@")
        if not name or not domain or "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise AnketaError(f"неверный формат почты: {raw_email}")
        return email

    @staticmethod
    def check_phone(raw_phone):
        digits = "".join(ch for ch in raw_phone if ch.isdigit())
        if len(digits) != 11 or digits[0] not in ["7", "8"]:
            raise AnketaError(f"неверный формат телефона: {raw_phone}")
        return f"7{digits[1:]}"

    def masked_phone(self):
        return f"+7 ({self.phone[0:3]}) ***-**-{self.phone[-2:]}"

    def short_fio(self):
        parts = self.fio.split()
        result = parts[0]
        for p in parts[1:]:
            result += " " + p[0].upper() + "."
        return result

    def role(self):
        return "—"

    def extra(self):
        return "—"

    def __str__(self):
        return f"{self.fio} ({self.role()})"

    def __lt__(self, other):
        return self.fio.replace("ё", "е").replace("Ё", "Е") < other.fio.replace("ё", "е").replace("Ё", "Е")

class Student(Person):
    def __init__(self, fio, mail, phone, group):
        super().__init__(fio, mail, phone)
        if not group.strip():
            raise AnketaError("пустое поле группы")
        self.group = group.strip().lower()

    def role(self):
        return "студент"

    def extra(self):
        return self.group


class Teacher(Person):
    def __init__(self, fio, mail, phone, department):
        super().__init__(fio, mail, phone)
        if not department.strip():
            raise AnketaError("пустое поле кафедры")
        self.department = department.strip()

    def role(self):
        return "преподаватель"

    def extra(self):
        return self.department