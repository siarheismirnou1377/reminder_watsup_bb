"""
Модуль `database.py` предназначен для работы с базой данных SQLite, которая хранит напоминания.

Основные функции:
- `create_database()`: Создает базу данных и таблицу для хранения напоминаний.
- `save_reminder(conn, c, reminder)`: Сохраняет напоминание в базу данных.
- `get_reminders_by_phone_number(c, phone_number)`: Возвращает все напоминания для указанного номера телефона.
- `delete_reminder_by_id(conn, c, reminder_id)`: Удаляет напоминание по его ID.

Описание:
    Этот модуль предоставляет функции для создания базы данных, добавления, получения и удаления напоминаний.
    База данных использует SQLite, а таблица `reminders` содержит следующие поля:
    - `id`: Уникальный идентификатор напоминания (автоинкремент).
    - `phone_number`: Номер телефона, на который отправляется напоминание.
    - `reminder_text`: Текст напоминания.
    - `reminder_time`: Время напоминания в формате строки.

Пример использования:
    >>> from database import create_database, save_reminder, get_reminders_by_phone_number, delete_reminder_by_id
    >>> conn, c = create_database()
    >>> reminder = {"phone_number": "+79123456789", "reminder_text": "Позвонить маме", "reminder_time": "2023-10-01 12:00:00"}
    >>> save_reminder(conn, c, reminder)
    >>> reminders = get_reminders_by_phone_number(c, "+79123456789")
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
