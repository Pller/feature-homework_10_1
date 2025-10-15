import os
from typing import Dict, Any
import requests


def convert_currency(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли, если валюта USD или EUR.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        float: Сумма в рублях
    """
    # Получаем данные из структуры operationAmount
    operation_amount = transaction.get('operationAmount', {})
    amount_str = operation_amount.get('amount', '0.0')
    currency_data = operation_amount.get('currency', {})
    currency = currency_data.get('code', 'RUB')

    # Конвертируем строку в float
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        amount = 0.0

    # Если уже в рублях, возвращаем как есть
    if currency == 'RUB':
        return amount

    # Если USD или EUR, конвертируем через внешнее API
    if currency in ['USD', 'EUR']:
        return _convert_via_api(amount, currency)

    # Для других валют возвращаем исходную сумму
    return amount


def _convert_via_api(amount: float, from_currency: str) -> float:
    """
    Конвертирует валюту используя внешнее API.

    Args:
        amount: Сумма для конвертации
        from_currency: Исходная валюта

    Returns:
        float: Конвертированная сумма в рублях
    """
    api_key = os.getenv('EXCHANGERATES_API_KEY')

    if not api_key:
        # Без API ключа не можем конвертировать, возвращаем исходную сумму
        return amount

    # Правильный endpoint согласно документации API
    url = "https://api.apilayer.com/exchangerates_data/convert"

    params = {
        "from": from_currency,
        "to": "RUB",
        "amount": amount
    }

    headers = {
        "apikey": api_key
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()

        # Проверяем успешность запроса и наличие ключа "result"
        if data.get('success') and 'result' in data:
            return float(data['result'])
        else:
            # Если API fails, return original amount
            return amount

    except (requests.RequestException, ValueError, KeyError):
        return amount
