"""
Модуль `models.py` содержит модели данных, используемые в приложении.

Основные классы:
- `Reminder`: Модель для хранения данных о напоминании.

Описание:
    Этот модуль использует библиотеку Pydantic для создания моделей данных с валидацией.
    Модель `Reminder` используется для передачи данных о напоминании между компонентами приложения.

Пример использования:
    >>> from models import Reminder
    >>> reminder = Reminder(phone_number="+79123456789", reminder_text="Позвонить маме", reminder_time="2023-10-01 12:00:00")
"""

from pydantic import BaseModel

class Reminder(BaseModel):
    """
    Модель для хранения данных о напоминании.

    Атрибуты:
        phone_number (str): Номер телефона, на который отправляется напоминание.
        reminder_text (str): Текст напоминания.
        reminder_time (str): Время напоминания в формате строки (YYYY-MM-DD HH:MM:SS).
    """
    phone_number: str
    reminder_text: str
    reminder_time: str
