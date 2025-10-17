"""Тесты для модуля masks."""
from src.masks import get_mask_card_number, get_mask_account


class TestMasks:
    """Тестовые случаи для функций масок."""

    def test_get_mask_card_number_valid(self):
        """Тест маски номера карты с корректным номером."""
        result = get_mask_card_number("1234567890123456")
        assert result == "1234 56** **** 3456"

    def test_get_mask_card_number_invalid(self):
        """Тест маски номера карты с некорректным номером."""
        result = get_mask_card_number("1234")
        assert result == "Некорректный номер карты"

    def test_get_mask_account_valid(self):
        """Тест маски номера счета с корректным номером."""
        result = get_mask_account("12345678901234567890")
        assert result == "**7890"

    def test_get_mask_account_invalid(self):
        """Тест маски номера счета с некорректным номером."""
        result = get_mask_account("1234")
        assert result == "Некорректный номер счета"


if __name__ == "__main__":
    import pytest
    pytest.main()
