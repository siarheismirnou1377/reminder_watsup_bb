import sqlite3

# Функция для создания базы данных и таблицы
def create_database():
    conn = sqlite3.connect('reminders.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reminders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, phone_number TEXT, reminder_text TEXT, reminder_time TEXT)''')
    conn.commit()
    return conn, c


# Функция для сохранения напоминания в БД
def save_reminder(conn, c, reminder):
    c.execute("INSERT INTO reminders (phone_number, reminder_text, reminder_time) VALUES (?, ?, ?)",
              (reminder['phone_number'], reminder['reminder_text'], reminder['reminder_time']))
    conn.commit()

# Функция для получения всех напоминаний по номеру телефона
def get_reminders_by_phone_number(c, phone_number):
    c.execute("SELECT * FROM reminders WHERE phone_number=?", (phone_number,))
    return c.fetchall()


# Функция для удаления напоминания по ID
def delete_reminder_by_id(conn, c, reminder_id):
    c.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
    conn.commit()
