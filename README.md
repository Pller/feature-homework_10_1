## Тестирование

Проект использует pytest для тестирования. Для запуска тестов:


# Все тесты
pytest

# Генерация отчета покрытия
pytest --cov=src --cov-report=html tests/

# Конкретный модуль
pytest tests/test_processing.py -v