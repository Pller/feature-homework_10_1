import json
from src.utils import read_json_file

# Читаем файл и смотрим структуру
transactions = read_json_file('data/operations.json')
print(f"Всего транзакций: {len(transactions)}")

# Покажем первую транзакцию для примера
if transactions:
    print("Первая транзакция:")
    print(json.dumps(transactions[0], indent=2, ensure_ascii=False))

    # Покажем все ключи всех транзакций
    print("\nВсе ключи в транзакциях:")
    all_keys = set()
    for transaction in transactions:
        all_keys.update(transaction.keys())
    print(f"Ключи: {all_keys}")