import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.', 'config.env'))

# Учетные данные Twilio
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
FROM_NUMBER = os.getenv('FROM_NUMBER')
