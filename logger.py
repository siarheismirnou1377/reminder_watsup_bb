"""
Модуль `logger.py` предназначен для настройки и управления логированием в приложении.

Основная функция:
- `setup_logger(name_file, name_logger)`: Настраивает логгер с ротацией файлов.

Описание:
    Этот модуль позволяет создавать логгеры, которые
    записывают сообщения в файлы с ограничением размера
    и автоматической ротацией. Логи сохраняются в папке `logs`,
    а старые файлы архивируются.

Пример использования:
    >>> from logger import setup_logger
    >>> logger = setup_logger("my_app_log", "my_app_logger")
    >>> logger.info("Это тестовое сообщение.")
"""

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name_file, name_logger):
    """
    Настраивает и возвращает логгер с ротацией файлов.

    Параметры:
        name_file (str): Имя файла для логов (без расширения). Файл будет создан в папке `logs`.
        name_logger (str): Имя логгера, которое будет отображаться в логах.

    Возвращает:
        logging.Logger: Настроенный логгер.

    Пример использования:
        logger = setup_logger("parser_main_log", "parser_main_logger")
        logger.info("Это тестовое сообщение.")
    """
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Настройка базовой конфигурации логирования
    logging.basicConfig(level=logging.INFO)

    # Установка размера файла логов в 8 МБ
    max_bytes = 8 * 1024 * 1024  # 8 МБ в байтах

    # Создание обработчика файлов с ограничением размера и ротацией
    file_handler = RotatingFileHandler(
        f"logs/{name_file}.log",  # Путь к файлу логов
        maxBytes=max_bytes,  # Максимальный размер файла логов
        backupCount=30,  # Количество файлов логов, которые будут храниться
        encoding="utf-8",  # Кодировка файла
    )

    # Формат сообщений
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Создание и настройка логгера
    logger = logging.getLogger(f'{name_logger}')
    logger.addHandler(file_handler)

    return logger
