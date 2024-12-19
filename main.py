import json
from datetime import datetime, timedelta

FILE_PATH = "phonebook.json"

def load_phonebook():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_phonebook(phonebook):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(phonebook, file, ensure_ascii=False, indent=4)

def validate_name(name):
    return all(x.isalnum() or x.isspace() for x in name) and name.istitle()

def validate_phone(phone):
    if phone.startswith("+7"):
        phone = "8" + phone[2:]
    return phone.isdigit() and len(phone) == 11

def validate_date(date):
    try:
        datetime.strptime(date, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def add_record(phonebook):
    print("Введите запись в формате: Name;Surname;DD.MM.YYYY;XXXXXXXXXXX")
    record = input("Запись: ").strip()
    try:
        first_name, last_name, dob, phone = record.split(";")
        first_name, last_name = first_name.strip().capitalize(), last_name.strip().capitalize()

        if not validate_name(first_name) or not validate_name(last_name):
            print("Некорректные имя или фамилия.")
            return

        if not validate_phone(phone.strip()):
            print("Некорректный номер телефона.")
            return

        if dob.strip() and not validate_date(dob.strip()):
            print("Некорректная дата рождения.")
            return

        if any(record["Имя"] == first_name and record["Фамилия"] == last_name for record in phonebook):
            print("Такая запись уже существует.")
            return

        phonebook.append({
            "Имя": first_name,
            "Фамилия": last_name,
            "Номер телефона": phone.strip(),
            "Дата рождения": dob.strip() or None
        })
        print("Запись добавлена.")
    except ValueError:
        print("Некорректный формат записи.")

def update_record(phonebook):
    print("Введите имя и фамилию для изменения записи (формат: Name;Surname):")
    try:
        first_name, last_name = input().split(";")
        first_name, last_name = first_name.strip().capitalize(), last_name.strip().capitalize()

        for record in phonebook:
            if record["Имя"] == first_name and record["Фамилия"] == last_name:
                print("Введите новое значение записи в формате: Name;Surname;DD.MM.YYYY;XXXXXXXXXXX")
                new_record = input("Новая запись: ").strip()
                try:
                    new_first_name, new_last_name, dob, phone = new_record.split(";")
                    if not validate_name(new_first_name) or not validate_name(new_last_name):
                        print("Некорректные имя или фамилия.")
                        return
                    if not validate_phone(phone.strip()):
                        print("Некорректный номер телефона.")
                        return
                    if dob.strip() and not validate_date(dob.strip()):
                        print("Некорректная дата рождения.")
                        return
                    record.update({
                        "Имя": new_first_name.strip().capitalize(),
                        "Фамилия": new_last_name.strip().capitalize(),
                        "Номер телефона": phone.strip(),
                        "Дата рождения": dob.strip() or None
                    })
                    print("Запись обновлена.")
                    return
                except ValueError:
                    print("Некорректный формат новой записи.")
                    return
        print("Запись не найдена.")
    except ValueError:
        print("Некорректный формат ввода.")

def delete_record(phonebook):
    print("Введите имя и фамилию для удаления записи (формат: Name;Surname):")
    try:
        first_name, last_name = input().split(";")
        first_name, last_name = first_name.strip().capitalize(), last_name.strip().capitalize()

        for record in phonebook:
            if record["Имя"] == first_name and record["Фамилия"] == last_name:
                phonebook.remove(record)
                print("Запись удалена.")
                return
        print("Запись не найдена.")
    except ValueError:
        print("Некорректный формат ввода.")

def view_records(phonebook):
    if not phonebook:
        print("Справочник пуст.")
    else:
        for record in phonebook:
            print(record)

def search_records(phonebook):
    query = input("Введите данные для поиска: ").strip()
    results = [record for record in phonebook if query.lower() in str(record).lower()]
    if results:
        print("Найденные записи:")
        for record in results:
            print(record)
    else:
        print("Записи не найдены.")

def show_next_birthday(phonebook):
    today = datetime.now()
    closest_birthday = None
    closest_record = None

    for record in phonebook:
        dob = record.get("Дата рождения")
        if dob:
            birth_date = datetime.strptime(dob, "%d.%m.%Y")
            this_year_birthday = birth_date.replace(year=today.year)

            if this_year_birthday < today:
                this_year_birthday = this_year_birthday.replace(year=today.year + 1)

            days_until_birthday = (this_year_birthday - today).days
            if closest_birthday is None or days_until_birthday < closest_birthday:
                closest_birthday = days_until_birthday
                closest_record = record

    if closest_record:
        print(f"Ближайший день рождения у {closest_record['Имя']} {closest_record['Фамилия']} через {closest_birthday} дней.")
    else:
        print("Нет записей с указанной датой рождения.")

def menu():
    print("Телефонный справочник. Доступные команды:")
    print("1: Добавить запись")
    print("2: Изменить запись")
    print("3: Удалить запись")
    print("4: Просмотреть все записи")
    print("5: Поиск записи")
    print("6: Ближайший день рождения")
    print("quit: Выйти")


def main():
    phonebook = load_phonebook()
    commands = {
        "1": add_record,
        "2": update_record,
        "3": delete_record,
        "4": view_records,
        "5": search_records,
        "6": show_next_birthday,
        "quit": lambda pb: exit()
    }

    menu()

    while True:
        command = input("Введите номер команды: ").strip().lower()
        if command in commands:
            commands[command](phonebook)
            save_phonebook(phonebook)
        else:
            print("Неизвестная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()
