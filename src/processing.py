from typing import List, Dict
from datetime import datetime


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Фильтрует список операций по статусу.

    Returns:
        Отфильтрованный список операций
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортирует список операций по дате.

    Returns:
        Отсортированный список операций
    """

    def get_date_key(operation: Dict) -> datetime:
        date_str = operation.get("date", "")
        return datetime.fromisoformat(date_str) if date_str else datetime.min

    return sorted(operations, key=get_date_key, reverse=reverse)
