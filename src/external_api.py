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
        return float(amount)  # Явное преобразование в float

    # Если USD или EUR, конвертируем через внешнее API
    if currency in ['USD', 'EUR']:
        return _convert_via_api(amount, currency)

    # Для других валют возвращаем исходную сумму
    return float(amount)  # Явное преобразование в float


def _load_env() -> None:
    """Загружает переменные окружения из .env файла."""
    try:
        # Простая загрузка .env без сторонних библиотек
        env_path = '.env'
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    except Exception:
        # Если не получилось загрузить .env, используем системные переменные
        pass


def _convert_via_api(amount: float, from_currency: str) -> float:
    """
    Конвертирует валюту используя внешнее API.

    Args:
        amount: Сумма для конвертации
        from_currency: Исходная валюта

    Returns:
        float: Конвертированная сумма в рублях
    """
    # Загружаем переменные окружения
    _load_env()

    api_key = os.getenv('EXCHANGERATES_API_KEY')

    if not api_key:
        # Без API ключа не можем конвертировать, возвращаем исходную сумму
        return float(amount)

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
            return float(amount)

    except (requests.RequestException, ValueError, KeyError):
        return float(amount)
