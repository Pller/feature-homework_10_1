## 🔄 Генераторы данных

Модуль `generators` предоставляет инструменты для работы с большими объемами данных через генераторы.

### Использование генераторов

```python
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Пример данных транзакций
transactions = [
    {
        "id": 939719570,
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод организации"
    }
]

# Фильтрация транзакций по валюте
usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))

# Генератор описаний транзакций
descriptions = transaction_descriptions(transactions)
for _ in range(3):
    print(next(descriptions))

# Генератор номеров карт
for card_number in card_number_generator(1, 5):
    print(card_number)
# Output: 
# 0000 0000 0000 0001
# 0000 0000 0000 0002