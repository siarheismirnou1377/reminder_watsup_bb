"""
Модуль `main.py` является основным модулем приложения для управления напоминаниями.

Основные функции:
- `send_reminder(phone_number: str, reminder_text: str)`: Отправляет напоминание через WhatsApp.
- `create_reminder(reminder: Reminder)`: Создает и сохраняет напоминание в базе данных.
- `get_reminders(phone_number: str)`: Возвращает все напоминания для указанного номера телефона.
- `get_reminder(reminder_id: int, phone_number: str):`: Возвращает напоминание по id для указанного номера телефона.
- `delete_reminder(reminder_id: int)`: Удаляет напоминание по его ID.

Описание:
    Этот модуль использует FastAPI для создания REST API, Twilio для отправки сообщений
    и APScheduler для планирования напоминаний. Логирование осуществляется через модуль `logger.py`.

Пример использования:
    Запуск приложения:
    >>> uvicorn main:app --host 0.0.0.0 --port 8000

    Пример запроса на создание напоминания:
    >>> POST /reminder/
    >>> Body: {"phone_number": "+79123456789", "reminder_text": "Позвонить маме", "reminder_time": "2023-10-01 12:00:00"}
"""

import datetime
import uvicorn
from fastapi import FastAPI
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler

from database import (
    create_database,
    delete_reminder_by_id,
    get_reminders_by_phone_number,
    save_reminder,
    get_reminder_by_id_for_phone
)
from logger import setup_logger
from config import ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER
from models import Reminder

# Инициализация FastAPI
app = FastAPI()

# Инициализация логгера
logger = setup_logger("main_log", "main_logger")

# Инициализация клиента Twilio
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Инициализация планировщика
scheduler = BackgroundScheduler()
scheduler.start()

# Создание базы данных
CONN, C = create_database()

def send_reminder(phone_number: str, reminder_text: str):
    """
    Отправляет напоминание через WhatsApp.

    Параметры:
        phone_number (str): Номер телефона получателя.
        reminder_text (str): Текст напоминания.
    """
    try:
        client.messages.create(
            body=reminder_text,
            from_=f'whatsapp:{FROM_NUMBER}',
            to=f'whatsapp:{phone_number}'
        )
        logger.info("Напоминание, отправленно на %s : %s", phone_number, reminder_text)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Напоминание не отправлено. Ошибка в функции send_reminder -\n %s", e)

@app.post("/reminder/")
async def create_reminder(reminder: Reminder):
    """
    Создает и сохраняет напоминание в базе данных.

    Параметры:
        reminder (Reminder): Объект напоминания, содержащий номер телефона, текст и время.

    Возвращает:
        dict: Сообщение об успешном создании напоминания.
    """
    try:
        save_reminder(CONN, C, reminder)
        reminder_time = datetime.datetime.strptime(reminder.reminder_time, "%Y-%m-%d %H:%M:%S")
        scheduler.add_job(
            send_reminder,
            'date',
            run_date=reminder_time,
            args=[reminder.phone_number, reminder.reminder_text]
        )
        return {"message": "Напоминание установлено успешно"}
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Ошибка в функции create_reminder - \n %s", e)

@app.get("/reminders/")
async def get_reminders(phone_number: str):
    """
    Возвращает все напоминания для указанного номера телефона.

    Параметры:
        phone_number (str): Номер телефона.

    Возвращает:
        dict: Список напоминаний.
    """
    try:
        reminders = get_reminders_by_phone_number(C, phone_number)
        return {"reminders": reminders}
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Ошибка в функции get_reminders - \n %s", e)

@app.get("/reminder/{reminder_id}")
async def get_reminder(reminder_id: int, phone_number: str):
    """
    Возвращает напоминание по его ID и номеру телефона.

    Параметры:
        reminder_id (int): ID напоминания.
        phone_number (str): Номер телефона.

    Возвращает:
        dict: Напоминание, если найдено и принадлежит указанному номеру, иначе сообщение об ошибке.
    """
    try:
        result = get_reminder_by_id_for_phone(C, reminder_id, phone_number)
        return result
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Ошибка в функции get_reminder - \n %s", e)
        return {"message": "Произошла ошибка при получении напоминания"}

@app.delete("/reminder/{reminder_id}")
async def delete_reminder(reminder_id: int):
    """
    Удаляет напоминание по его ID.

    Параметры:
        reminder_id (int): ID напоминания.

    Возвращает:
        dict: Сообщение об успешном удалении напоминания.
    """
    try:
        delete_reminder_by_id(CONN, C, reminder_id)
        return {"message": "Напоминание успешно удалено"}
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Ошибка в функции delete_reminder - \n %s", e)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
