"""
Модуль `database.py` предназначен для работы с базой данных SQLite, которая хранит напоминания.

Основные функции:
- `create_database()`: Создает базу данных и таблицу для хранения напоминаний.
- `save_reminder(conn, c, reminder)`: Сохраняет напоминание в базу данных.
- `get_reminders_by_phone_number(c, phone_number)`: Возвращает все напоминания для указанного номера телефона.
- `get_reminder_by_id(cursor, reminder_id, phone_number)`: Возвращает напоминание по его ID и номеру телефона.
- `get_reminder_by_id_for_phone(cursor, reminder_id, phone_number)`: Возвращает напоминание по его ID и номеру телефона или сообщение об ошибке.
- `delete_reminder_by_id(conn, c, reminder_id)`: Удаляет напоминание по его ID.

Описание:
    Этот модуль предоставляет функции для создания базы данных, добавления, получения и удаления напоминаний.
    База данных использует SQLite, а таблица `reminders` содержит следующие поля:
    - `id`: Уникальный идентификатор напоминания (автоинкремент).
    - `phone_number`: Номер телефона, на который отправляется напоминание.
    - `reminder_text`: Текст напоминания.
    - `reminder_time`: Время напоминания в формате строки.

    Модуль также поддерживает проверку принадлежности напоминания определенному номеру телефона,
    что позволяет избежать несанкционированного доступа к чужим напоминаниям.

Пример использования:
    >>> from database import create_database, save_reminder, get_reminders_by_phone_number, delete_reminder_by_id
    >>> conn, c = create_database()
    >>> reminder = {"phone_number": "+79123456789", "reminder_text": "Позвонить маме", "reminder_time": "2023-10-01 12:00:00"}
    >>> save_reminder(conn, c, reminder)
    >>> reminders = get_reminders_by_phone_number(c, "+79123456789")
    >>> reminder = get_reminder_by_id(c, 1, "+79123456789")
    >>> delete_reminder_by_id(conn, c, 1)
"""

import sqlite3

def create_database():
    """
    Создает базу данных и таблицу для хранения напоминаний.

    Возвращает:
        tuple: Кортеж из двух элементов:
            - conn: Объект соединения с базой данных.
            - c: Объект курсора для выполнения SQL-запросов.
    """
    conn = sqlite3.connect('reminders.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reminders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, phone_number TEXT, reminder_text TEXT, reminder_time TEXT)''')
    conn.commit()
    return conn, c

def save_reminder(conn, c, reminder):
    """
    Сохраняет напоминание в базу данных.

    Параметры:
        conn: Объект соединения с базой данных.
        c: Объект курсора для выполнения SQL-запросов.
        reminder (dict): Словарь с данными напоминания:
            - phone_number (str): Номер телефона.
            - reminder_text (str): Текст напоминания.
            - reminder_time (str): Время напоминания в формате строки.
    """
    c.execute("INSERT INTO reminders (phone_number, reminder_text, reminder_time) VALUES (?, ?, ?)",
              (reminder['phone_number'], reminder['reminder_text'], reminder['reminder_time']))
    conn.commit()

def get_reminders_by_phone_number(c, phone_number):
    """
    Возвращает все напоминания для указанного номера телефона.

    Параметры:
        c: Объект курсора для выполнения SQL-запросов.
        phone_number (str): Номер телефона.

    Возвращает:
        list: Список напоминаний, где каждое напоминание представлено в виде кортежа.
    """
    c.execute("SELECT * FROM reminders WHERE phone_number=?", (phone_number,))
    return c.fetchall()

def get_reminder_by_id(cursor, reminder_id: int, phone_number: str):
    """
    Возвращает напоминание по его ID и номеру телефона.

    Параметры:
        cursor: Курсор базы данных.
        reminder_id (int): ID напоминания.
        phone_number (str): Номер телефона.

    Возвращает:
        dict: Напоминание, если найдено и принадлежит указанному номеру, иначе None.
    """
    cursor.execute("SELECT * FROM reminders WHERE id = ? AND phone_number = ?", (reminder_id, phone_number))
    reminder = cursor.fetchone()
    if reminder:
        return {
            "id": reminder[0],
            "phone_number": reminder[1],
            "reminder_text": reminder[2],
            "reminder_time": reminder[3]
        }
    return None

def get_reminder_by_id_for_phone(cursor, reminder_id: int, phone_number: str):
    """
    Возвращает напоминание по его ID и номеру телефона или сообщение об ошибке.

    Параметры:
        cursor: Курсор базы данных.
        reminder_id (int): ID напоминания.
        phone_number (str): Номер телефона.

    Возвращает:
        dict: Напоминание, если найдено и принадлежит указанному номеру, иначе сообщение об ошибке.
    """
    reminder = get_reminder_by_id(cursor, reminder_id, phone_number)
    if reminder:
        return {"reminder": reminder}
    else:
        return {"message": "Напоминание не найдено или не принадлежит указанному номеру телефона"}

def delete_reminder_by_id(conn, c, reminder_id):
    """
    Удаляет напоминание по его ID.

    Параметры:
        conn: Объект соединения с базой данных.
        c: Объект курсора для выполнения SQL-запросов.
        reminder_id (int): ID напоминания.
    """
    c.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
    conn.commit()
