import os
from typing import Dict, Any
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


def convert_currency_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        Сумма транзакции в рублях (float)
    """
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount", "0")
    currency_info = operation_amount.get("currency", {})
    currency_code = currency_info.get("code", "RUB")

    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        return 0.0

    # Если валюта уже в рублях, возвращаем как есть
    if currency_code == "RUB":
        return amount

    # Конвертируем USD и EUR
    if currency_code in ["USD", "EUR"]:
        api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if not api_key:
            raise ValueError("API key for exchange rates not found in environment variables")

        # Получаем курс валют
        exchange_rate = get_exchange_rate(currency_code, "RUB", api_key)
        return amount * exchange_rate

    # Для других валют возвращаем оригинальную сумму
    return amount


def get_exchange_rate(from_currency: str, to_currency: str, api_key: str) -> float:
    """
    Получает текущий курс валют от внешнего API.

    Args:
        from_currency: Исходная валюта
        to_currency: Целевая валюта
        api_key: API ключ для сервиса курсов валют

    Returns:
        Курс обмена
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={from_currency}&symbols={to_currency}"

    headers = {
        "apikey": api_key
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data["rates"][to_currency]

    except (requests.RequestException, KeyError, ValueError) as:
        # В случае ошибки API используем фиксированные курсы для тестирования
        fallback_rates = {
            "USD": 90.0,
            "EUR": 100.0
        }
        return fallback_rates.get(from_currency, 1.0)
