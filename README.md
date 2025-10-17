## Работа с данными и API

### Чтение JSON файлов

Модуль `utils` предоставляет функции для работы с файлами данных.

```python
from src.utils import read_json_file

# Чтение данных из JSON файла
transactions = read_json_file("data/operations.json")
print(f"Загружено {len(transactions)} транзакций")