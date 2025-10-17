"""Тесты для утилитарных функций."""
import json
import tempfile
import os
from src.utils import read_json_file


class TestUtils:
    """Тестовые случаи для утилитарных функций."""

    def test_read_json_file_valid(self):
        """Тест чтения корректного JSON файла."""
        test_data = [
            {"id": 1, "amount": 100, "currency": "RUB"},
            {"id": 2, "amount": 200, "currency": "USD"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name
        try:
            result = read_json_file(temp_path)
            assert result == test_data
        finally:
            os.unlink(temp_path)

    def test_read_json_file_not_found(self):
        """Тест чтения несуществующего файла."""
        result = read_json_file('nonexistent.json')
        assert result == []

    def test_read_json_file_invalid_json(self):
        """Тест чтения некорректного JSON файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('некорректное json содержимое')
            temp_path = f.name
        try:
            result = read_json_file(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_read_json_file_not_list(self):
        """Тест чтения JSON который не является списком."""
        test_data = {"id": 1, "amount": 100}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name
        try:
            result = read_json_file(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_read_json_file_empty(self):
        """Тест чтения пустого JSON файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('')
            temp_path = f.name
        try:
            result = read_json_file(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)
