"""Модуль утилит для работы с файлами."""
import json
import logging
from typing import List, Dict, Any


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON файл и возвращает список словарей с данными о транзакциях.

    Args:
        file_path: Путь к JSON файлу

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список при ошибке
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        else:
            return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception:
        return []


# Настройка логгера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("utils.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def read_json_file_with_log(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON файл с логированием.

    Args:
        file_path: Путь к JSON файлу

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список при ошибке
    """
    try:
        result = read_json_file(file_path)
        if result:
            logger.debug(f"Успешно прочитан файл: {file_path}, записей: {len(result)}")
        else:
            logger.warning(f"Файл пуст или содержит ошибки: {file_path}")
        return result
    except Exception as e:
        logger.error(f"Ошибка чтения файла {file_path}: {e}")
        return []
