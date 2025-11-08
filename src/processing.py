"""Модуль для обработки банковских транзакций."""
import re
from typing import List, Dict, Any, Optional


def search_transactions_by_description(data: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по строке в описании с использованием регулярных выражений.

    Args:
        data (List[Dict]): Список словарей с транзакциями
        search_string (str): Строка для поиска в описании

    Returns:
        List[Dict]: Список транзакций, у которых в описании есть искомая строка
    """
    try:
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)
        result = [
            transaction for transaction in data
            if transaction.get('description') and pattern.search(transaction['description'])
        ]
        return result
    except Exception as e:
        print(f"Ошибка при поиске транзакций: {e}")
        return []


def count_transactions_by_categories(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    Args:
        data (List[Dict]): Список словарей с транзакциями
        categories (List[str]): Список категорий для подсчета

    Returns:
        Dict[str, int]: Словарь с количеством операций по категориям
    """
    try:
        # Приводим категории к нижнему регистру для поиска без учета регистра
        categories_lower = [cat.lower() for cat in categories]

        # Собираем все описания
        descriptions = [
            transaction.get('description', '').lower()
            for transaction in data
            if transaction.get('description')
        ]

        # Подсчитываем вхождения каждой категории
        category_counts = {}
        for category in categories_lower:
            count = sum(1 for desc in descriptions if category in desc)
            category_counts[category] = count

        return category_counts
    except Exception as e:
        print(f"Ошибка при подсчете категорий: {e}")
        return {}


def filter_transactions_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.

    Args:
        data (List[Dict]): Список словарей с транзакциями
        status (str): Статус для фильтрации

    Returns:
        List[Dict]: Отфильтрованный список транзакций
    """
    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    status_upper = status.upper()

    if status_upper not in valid_statuses:
        return []

    return [
        transaction for transaction in data
        if transaction.get('state', '').upper() == status_upper
    ]


def sort_transactions_by_date(data: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Args:
        data (List[Dict]): Список словарей с транзакциями
        reverse (bool): Если True - по убыванию, False - по возрастанию

    Returns:
        List[Dict]: Отсортированный список транзакций
    """
    try:
        return sorted(data, key=lambda x: x.get('date', ''), reverse=reverse)
    except Exception:
        return data


def filter_rub_transactions(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует рублевые транзакции.

    Args:
        data (List[Dict]): Список словарей с транзакциями

    Returns:
        List[Dict]: Список рублевых транзакций
    """
    return [
        transaction for transaction in data
        if transaction.get('currency_code') == 'RUB' or
           transaction.get('currency_name', '').lower() in ['рубль', 'rub', 'rur']
    ]
