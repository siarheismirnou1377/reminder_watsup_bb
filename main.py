import datetime

from fastapi import FastAPI
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler

from database import (
    create_database,
    delete_reminder_by_id,
    get_reminders_by_phone_number,
    save_reminder
    )
from logger import setup_logger
from config import ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER
from models import Reminder

app = FastAPI()
# Инициализация логера
logger = setup_logger("main_log", "main_logger")

# Инициализация клиента
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Инициализация планировщика
scheduler = BackgroundScheduler()
scheduler.start()

# Создание БД
CONN, C = create_database()

def send_reminder(phone_number: str, reminder_text: str):
    try:
        client.messages.create(
            body=reminder_text,
            from_=f'whatsapp:{FROM_NUMBER}',
            to=f'whatsapp:{phone_number}'
        )
        logger.info("Напоминание, отправленно на %s : %s",  phone_number, reminder_text)
    except Exception as e:
        logger.error("Напоминание не отправлено. Ошибка в функции send_reminder -\n %s", e)

@app.post("/reminder/")
async def create_reminder(reminder: Reminder):
    try:
        # Сохранение напоминания в БД
        save_reminder(CONN, C, reminder)
        # Планирование напоминания
        reminder_time = datetime.datetime.strptime(reminder.reminder_time, "%Y-%m-%d %H:%M:%S")
        scheduler.add_job(
            send_reminder,
            'date',
            run_date=reminder_time,
            args=[reminder.phone_number, reminder.reminder_text]
            )
        return {"message": "Напоминание установлено успешно"}
    except Exception as e:
        logger.error("Ошибка в функции create_reminder - \n %s", e)

@app.get("/reminders/")
async def get_reminders(phone_number: str):
    try:
        reminders = get_reminders_by_phone_number(C, phone_number)
        return {"reminders": reminders}
    except Exception as e:
        logger.error("Ошибка в функции get_reminders - \n %s", e)


@app.delete("/reminder/{reminder_id}")
async def delete_reminder(reminder_id: int):
    try:
        delete_reminder_by_id(CONN, C, reminder_id)
        return {"message": "Напоминание успешно удалено"}
    except Exception as e:
        logger.error("Ошибка в функции delete_reminder - \n %s", e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
