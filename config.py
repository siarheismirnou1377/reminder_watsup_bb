"""
Модуль `config.py` предназначен для загрузки конфигурационных переменных из файла `.env`.

Основные переменные:
- `ACCOUNT_SID`: Идентификатор аккаунта Twilio.
- `AUTH_TOKEN`: Токен аутентификации Twilio.
- `FROM_NUMBER`: Номер телефона, с которого будут отправляться сообщения.

Описание:
    Этот модуль загружает переменные окружения из файла `config.env`, который должен находиться
    в корневой директории проекта. Переменные используются для настройки клиента Twilio.

Пример использования:
    >>> from config import ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER
    >>> print(ACCOUNT_SID)
"""

import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.', 'config.env'))

# Идентификатор аккаунта Twilio
ACCOUNT_SID = os.getenv('ACCOUNT_SID')

# Токен аутентификации Twilio
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

# Номер телефона для отправки сообщений
FROM_NUMBER = os.getenv('FROM_NUMBER')
