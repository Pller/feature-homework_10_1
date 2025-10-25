import pandas as pd
from typing import List, Dict, Any
import logging


# Настройка логгера
logger = logging.getLogger("file_reader")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler("file_reader.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из CSV файла.

    Args:
        file_path (str): Путь к CSV файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями или пустой список при ошибке
    """
    try:
        logger.debug(f"Чтение CSV файла: {file_path}")
        # Указываем разделитель точка с запятой и кодировку
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')

        # Конвертируем NaN в None для корректной работы с JSON
        df = df.where(pd.notnull(df), None)

        transactions = df.to_dict('records')
        logger.debug(f"Успешно прочитано {len(transactions)} транзакций из CSV")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка чтения CSV файла {file_path}: {e}")
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из Excel файла.

    Args:
        file_path (str): Путь к Excel файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями или пустой список при ошибке
    """
    try:
        logger.debug(f"Чтение Excel файла: {file_path}")
        df = pd.read_excel(file_path)

        # Конвертируем NaN в None для корректной работы с JSON
        df = df.where(pd.notnull(df), None)

        transactions = df.to_dict('records')
        logger.debug(f"Успешно прочитано {len(transactions)} транзакций из Excel")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка чтения Excel файла {file_path}: {e}")
        return []
