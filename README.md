## Декораторы

Модуль `decorators` предоставляет инструменты для логирования работы функций.

### Использование декоратора log

```python
from src.decorators import log

# Логирование в консоль
@log()
def add(a, b):
    return a + b

add(2, 3)  # Вывод в консоль: [timestamp] add ok

# Логирование в файл
@log(filename="operations.log")
def multiply(a, b):
    return a * b

multiply(4, 5)  # Запись в файл operations.log

# Логирование ошибок
@log()
def divide(a, b):
    return a / b