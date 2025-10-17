"""Модуль утилит для работы с файлами."""
import json
import logging
import os
from typing import List, Dict, Any

# Настройка логера для модуля utils
def setup_utils_logger() -> logging.Logger:
    """Настраивает и возвращает логер для модуля utils."""
    logger = logging.getLogger('utils')
    logger.setLevel(logging.DEBUG)
    
    # Создаем папку logs если ее нет
    os.makedirs('logs', exist_ok=True)
    
    # File handler с перезаписью файла при каждом запуске
    file_handler = logging.FileHandler('logs/utils.log', mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Форматер логов
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Добавляем handler к логеру
    logger.addHandler(file_handler)
    
    return logger

# Создаем логер
utils_logger = setup_utils_logger()

def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON файл и возвращает список словарей с данными о транзакциях.
    
    Args:
        file_path: Путь к JSON файлу
        
    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список при ошибке
    """
    try:
        # Используем переданный путь как есть
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        if isinstance(data, list):
            utils_logger.info(f"Успешно прочитан файл {file_path}. Записей: {len(data)}")
            return data
        else:
            utils_logger.warning(f"Файл {file_path} не содержит список. Тип данных: {type(data)}")
            return []
            
    except FileNotFoundError:
        utils_logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        utils_logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        utils_logger.error(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []
