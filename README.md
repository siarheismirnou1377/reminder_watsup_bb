# Приложение для управления напоминаниями

Это приложение позволяет создавать, просматривать и удалять напоминания, которые отправляются через WhatsApp в указанное время. Оно использует FastAPI для REST API, Twilio для отправки сообщений и SQLite для хранения данных.

---

## Для чего это приложение?

Приложение предназначено для:

1. **Создания напоминаний**: Вы можете указать номер телефона, текст напоминания и время, когда оно должно быть отправлено.
2. **Отправки напоминаний через WhatsApp**: Напоминания отправляются через Twilio API.
3. **Управления напоминаниями**: Вы можете просматривать и удалять напоминания.

---

## Требования

- Docker
- Docker Compose (опционально)

---

## Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/ваш-репозиторий.git
cd ваш-репозиторий
```

### 2. Создайте файл `.env`

Создайте файл `.env` в корневой директории проекта и добавьте в него переменные окружения:

```plaintext
ACCOUNT_SID=ваш_account_sid
AUTH_TOKEN=ваш_auth_token
FROM_NUMBER=ваш_from_number
```

### 3. Соберите Docker-образ

```bash
docker build -t reminder-app .
```

### 4. Запустите контейнер

```bash
docker run -d -p 8000:8000 --name reminder-container reminder-app
```

### 5. Проверка работы приложения

Приложение будет доступно по адресу:

```
http://localhost:8000

```

---

## Использование Docker Compose (опционально)

Если вы хотите использовать Docker Compose, выполните следующие шаги:

1. Убедитесь, что у вас установлен Docker Compose.
2. Запустите проект:

```bash
docker-compose up -d
```

---

## API Endpoints

### Создание напоминания

- **Метод**: `POST`
- **URL**: `/reminder/`
- **Тело запроса**:

  ```json
  {
    "phone_number": "+79123456789",
    "reminder_text": "Позвонить маме",
    "reminder_time": "2023-10-01 12:00:00"
  }
  ```

- **Ответ**:

  ```json
  {
    "message": "Напоминание установлено успешно"
  }
  ```

### Получение напоминаний

- **Метод**: `GET`
- **URL**: `/reminders/?phone_number=+79123456789`
- **Ответ**:

  ```json
  {
    "reminders": [
      {
        "id": 1,
        "phone_number": "+79123456789",
        "reminder_text": "Позвонить маме",
        "reminder_time": "2023-10-01 12:00:00"
      }
    ]
  }
  ```

### Удаление напоминания

- **Метод**: `DELETE`
- **URL**: `/reminder/{reminder_id}`
- **Ответ**:

  ```json
  {
    "message": "Напоминание успешно удалено"
  }
  ```

---

## Остановка и удаление контейнера

### Остановка контейнера

```bash
docker stop reminder-container
```

### Удаление контейнера

```bash
docker rm reminder-container
```

### Удаление образа

```bash
docker rmi reminder-app
```

---

## Логирование

Логи приложения сохраняются в папке `logs` в файле `main_log.log`.

---

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

---
