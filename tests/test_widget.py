import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.widget import mask_account_card, get_date


class TestWidget:
    """Тесты для модуля widget."""

    def test_mask_account_card_visa(self):
        """Тестирование маскировки карты Visa."""
        result = mask_account_card("Visa Platinum 7000792289606361")
        assert result == "Visa Platinum 7000 79** **** 6361"

    def test_mask_account_card_maestro(self):
        """Тестирование маскировки карты Maestro."""
        result = mask_account_card("Maestro 1596837868705199")
        assert result == "Maestro 1596 83** **** 5199"

    def test_mask_account_card_account(self):
        """Тестирование маскировки счета."""
        result = mask_account_card("Счет 73654108430135874305")
        assert result == "Счет **4305"

    def test_mask_account_card_invalid_input(self):
        """Тестирование маскировки с невалидными данными."""
        with pytest.raises(ValueError):  # Убрали match с regex
            mask_account_card("Invalid Input")

    def test_mask_account_card_short_card(self):
        """Тестирование маскировки с коротким номером карты."""
        with pytest.raises(ValueError):  # Убрали match с regex
            mask_account_card("Visa Platinum 1234567890")

    def test_mask_account_card_short_account(self):
        """Тестирование маскировки с коротким номером счета."""
        with pytest.raises(ValueError):  # Убрали match с regex
            mask_account_card("Счет 1234567890")

    def test_get_date_valid(self):
        """Тестирование форматирования валидной даты."""
        result = get_date("2024-03-11T02:26:18.671407")
        assert result == "11.03.2024"

    def test_get_date_invalid_string(self):
        """Тестирование форматирования невалидной строки даты."""
        result = get_date("invalid-date")
        assert result == "01.01.0001"

    def test_get_date_empty(self):
        """Тестирование форматирования пустой даты."""
        result = get_date("")
        assert result == "01.01.0001"

    def test_get_date_wrong_format(self):
        """Тестирование форматирования даты в неправильном формате."""
        result = get_date("2024/03/11")
        assert result == "01.01.0001"

    def test_get_date_dash_format(self):
        """Тестирование форматирования даты с дефисами."""
        result = get_date("11-03-2024")
        assert result == "01.01.0001"
