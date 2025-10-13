import os
import sys
import tempfile
import json


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import read_json_file


class TestUtils:
    """Тесты для модуля utils."""

    def test_read_json_file_valid(self):
        """Тестирование чтения валидного JSON файла."""
        # Создаем временный JSON файл
        test_data = [
            {"id": 1, "name": "Test 1"},
            {"id": 2, "name": "Test 2"}
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(test_data, temp_file)
            temp_filename = temp_file.name

        try:
            result = read_json_file(temp_filename)
            assert result == test_data
        finally:
            os.unlink(temp_filename)

    def test_read_json_file_not_list(self):
        """Тестирование чтения JSON файла который не содержит список."""
        test_data = {"id": 1, "name": "Test"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(test_data, temp_file)
            temp_filename = temp_file.name

        try:
            result = read_json_file(temp_filename)
            assert result == []
        finally:
            os.unlink(temp_filename)

    def test_read_json_file_not_found(self):
        """Тестирование чтения несуществующего файла."""
        result = read_json_file("nonexistent_file.json")
        assert result == []

    def test_read_json_file_invalid_json(self):
        """Тестирование чтения файла с невалидным JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write("invalid json content")
            temp_filename = temp_file.name

        try:
            result = read_json_file(temp_filename)
            assert result == []
        finally:
            os.unlink(temp_filename)

    def test_read_json_file_empty(self):
        """Тестирование чтения пустого файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write("")
            temp_filename = temp_file.name

        try:
            result = read_json_file(temp_filename)
            assert result == []
        finally:
            os.unlink(temp_filename)
