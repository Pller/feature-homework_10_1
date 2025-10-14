import os
from typing import Dict, Any
import requests

try:
    from dotenv import load_dotenv

    # Пытаемся загрузить .env, но не падаем если его нет
    load_dotenv()
except ImportError:
    print("python-dotenv не установлен, используем переменные окружения системы")
except Exception as e:
    print(f"Ошибка загрузки .env файла: {e}")


def convert_currency(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли, если валюта USD или EUR.

    Args:
        transaction: Словарь с данными транзакции, содержащий
                    ключи 'amount' и 'currency'

    Returns:
        float: Сумма в рублях
    """
    amount = transaction.get('amount', 0.0)
    currency = transaction.get('currency', 'RUB')

    # Если уже в рублях, возвращаем как есть
    if currency == 'RUB':
        return float(amount)

    # Если USD или EUR, конвертируем через внешнее API
    if currency in ['USD', 'EUR']:
        return _convert_via_api(amount, currency)

    # Для других валют возвращаем исходную сумму
    return float(amount)


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

    # Если API ключ не найден, используем mock-конвертацию для тестов
    if not api_key:
        print("API ключ не найден, используется mock-конвертация")
        mock_rates = {'USD': 90.0, 'EUR': 100.0}
        return float(amount) * mock_rates.get(from_currency, 1.0)

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
            error_info = data.get('error', {}).get('info', 'Неизвестная ошибка API')
            print(f"Ошибка API: {error_info}")
            return float(amount)

    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"Ошибка при конвертации валюты: {e}")
        return float(amount)
