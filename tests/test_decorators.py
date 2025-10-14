import os
import sys
import tempfile

import pytest

# Добавляем корневую директорию в Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.decorators import log  # noqa: E402


class TestDecorators:
    """Тесты для модуля decorators."""

    def test_log_to_console_success(self, capsys):
        """Тестирование логирования успешной операции в консоль."""

        @log()
        def add(a: int, b: int) -> int:
            return a + b

        result = add(2, 3)

        # Проверяем результат
        assert result == 5

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "add ok" in captured.out

    def test_log_to_console_error(self, capsys):
        """Тестирование логирования ошибки в консоль."""

        @log()
        def divide(a: int, b: int) -> float:
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError" in captured.out
        assert "Inputs: (10, 0), {}" in captured.out

    def test_log_to_file_success(self):
        """Тестирование логирования успешной операции в файл."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
            temp_filename = temp_file.name

        try:
            @log(filename=temp_filename)
            def multiply(a: int, b: int) -> int:
                return a * b

            result = multiply(4, 5)

            # Проверяем результат
            assert result == 20

            # Проверяем запись в файл
            with open(temp_filename, "r", encoding="utf-8") as file:
                content = file.read()
                assert "multiply ok" in content

        finally:
            # Удаляем временный файл
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_log_to_file_error(self):
        """Тестирование логирования ошибки в файл."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
            temp_filename = temp_file.name

        try:
            @log(filename=temp_filename)
            def failing_function():
                raise ValueError("Test error")

            with pytest.raises(ValueError):
                failing_function()

            # Проверяем запись в файл
            with open(temp_filename, "r", encoding="utf-8") as file:
                content = file.read()
                assert "failing_function error: ValueError" in content
                assert "Inputs: (), {}" in content

        finally:
            # Удаляем временный файл
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_log_with_arguments(self, capsys):
        """Тестирование логирования функции с аргументами."""

        @log()
        def greet(name: str, age: int = 25) -> str:
            return f"Hello {name}, age {age}"

        result = greet("Alice", age=30)

        # Проверяем результат
        assert result == "Hello Alice, age 30"

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "greet ok" in captured.out

    def test_log_preserves_function_metadata(self):
        """Тестирование что декоратор сохраняет метаданные функции."""

        @log()
        def sample_function(x: int) -> int:
            """Тестовая функция."""
            return x * 2

        # Проверяем что имя и документация сохранились
        assert sample_function.__name__ == "sample_function"
        assert sample_function.__doc__ == "Тестовая функция."

    def test_log_with_keyword_arguments(self, capsys):
        """Тестирование логирования функции с keyword аргументами."""

        @log()
        def create_person(name: str, **kwargs) -> dict:
            person = {"name": name}
            person.update(kwargs)
            return person

        result = create_person("Bob", age=25, city="Moscow")

        # Проверяем результат
        assert result == {"name": "Bob", "age": 25, "city": "Moscow"}

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "create_person ok" in captured.out
