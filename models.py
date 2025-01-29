from pydantic import BaseModel

class Reminder(BaseModel):
    phone_number: str
    reminder_text: str
    reminder_time: str