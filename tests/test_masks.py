import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.masks import get_mask_card_number, get_mask_account_number


class TestMasks:
    """Тесты для модуля masks."""

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            ("7000792289606361", "7000 79** **** 6361"),
            ("1596837868705199", "1596 83** **** 5199"),
            ("7158300734726758", "7158 30** **** 6758"),
            ("6831982476737658", "6831 98** **** 7658"),
            ("8990922113665229", "8990 92** **** 5229"),
        ],
    )
    def test_get_mask_card_number_valid(self, card_number: str, expected: str) -> None:
        """Тестирование маскирования номера карты с валидными данными."""
        assert get_mask_card_number(card_number) == expected

    def test_get_mask_card_number_invalid(self) -> None:
        """Тестирование маскирования номера карты с невалидными данными."""
        with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
            get_mask_card_number("1234567890")  # Слишком короткий номер

        with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
            get_mask_card_number("not_a_number")  # Не числа

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("73654108430135874305", "**4305"),
            ("64686473678894779589", "**9589"),
            ("35383033474447895560", "**5560"),
            ("12345678901234567890", "**7890"),
        ],
    )
    def test_get_mask_account_number_valid(self, account_number: str, expected: str) -> None:
        """Тестирование маскирования номера счета с валидными данными."""
        assert get_mask_account_number(account_number) == expected

    def test_get_mask_account_number_invalid(self) -> None:
        """Тестирование маскирования номера счета с невалидными данными."""
        with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр"):
            get_mask_account_number("1234567890")  # Слишком короткий номер

        with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр"):
            get_mask_account_number("not_a_number")