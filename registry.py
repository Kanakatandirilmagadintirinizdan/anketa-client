import os
from people import Student, Teacher, AnketaError


class Registry:
    def __init__(self):
        self.people = []
        self.rejected = []

    def parse_line(self, line_num, line):
        fields = [f.strip() for f in line.split(";")]
        if len(fields) != 5:
            raise AnketaError(f"неверное количество полей ({len(fields)} вместо 5)")

        role_type, fio, mail, phone, extra = fields
        if role_type == "s":
            return Student(fio, mail, phone, extra)
        elif role_type == "t":
            return Teacher(fio, mail, phone, extra)
        else:
            raise AnketaError(f"неизвестный тип: {role_type}")

    def load(self, filename):
        if not os.path.exists(filename):
            return False
        with open(filename, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                try:
                    person = self.parse_line(line_num, clean_line)
                    self.people.append(person)
                except AnketaError as e:
                    self.rejected.append((line_num, clean_line, str(e)))
        return True

    def __len__(self):
        return len(self.people)

    def print_table(self):
        print(f"\n{'№':<3} {'ФИО':<25} {'Роль':<15} {'Группа/Каф':<12} {'Телефон':<20}")
        print("-" * 80)
        for i, p in enumerate(sorted(self.people), 1):
            print(f"{i:<3} {p.fio:<25} {p.role():<15} {p.extra():<12} {p.masked_phone():<20}")
        print("-" * 80)

    def print_stats(self):
        print(f"\nОтклонено строк: {len(self.rejected)}")
        for line_num, src, reason in self.rejected:
            print(f"  строка {line_num}: {reason}")
            print(f"      {src}")

        print(f"\nПринято: {len(self.people)} | Отклонено: {len(self.rejected)}")

        roles = {}
        groups = {}
        for p in self.people:
            roles[p.role()] = roles.get(p.role(), 0) + 1
            if p.role() == "студент":
                groups[p.extra()] = groups.get(p.extra(), 0) + 1

        print("\nПо ролям:")
        for r, count in roles.items():
            print(f"  {r}: {count}")
        if groups:
            print("По группам:")
            for g, count in groups.items():
                print(f"  {g}: {count}")

    def save(self, ok_file, err_file):
        with open(ok_file, "w", encoding="utf-8") as f:
            for p in self.people:
                f.write(f"{p.fio};{p.mail};{p.phone};{p.role()};{p.extra()}\n")
        with open(err_file, "w", encoding="utf-8") as f:
            for line_num, src, reason in self.rejected:
                f.write(f"строка {line_num};причина: {reason};исходник: {src}\n")
        print(f"\nСохранено: {ok_file} и {err_file}")