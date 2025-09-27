from typing import Dict, List, Iterator, Any

def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    """
        Фильтрует транзакции по валюте и возвращает итератор.
    """

    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})
        if currency_info.get("code") == currency:
            yield transaction

def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
        Генератор описаний транзакций.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
        Генератор номеров банковских карт.
    """
    for number in range(start, end + 1):
        # Форматируем номер с ведущими нулями
        card_number = str(number).zfill(16)
        # Разбиваем на группы по 4 цифры
        formatted_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"
        yield formatted_number
