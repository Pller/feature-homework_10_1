"""Тесты для модуля masks."""
import os
import pytest
from src.masks import mask_account_number, mask_card_number


class TestMasks:
    """Тесты для функций маскировки."""
    
    def test_mask_account_number_valid(self):
        """Тест маскировки корректного номера счета."""
        result = mask_account_number("12345678901234567890")
        assert result == "**7890"
        
    def test_mask_account_number_short(self):
        """Тест маскировки короткого номера счета."""
        result = mask_account_number("123")
        assert result is None
        
    def test_mask_account_number_empty(self):
        """Тест маскировки пустого номера счета."""
        result = mask_account_number("")
        assert result is None
        
    def test_mask_card_number_valid(self):
        """Тест маскировки корректного номера карты."""
        result = mask_card_number("1234567890123456")
        assert result == "1234 56** **** 3456"
        
    def test_mask_card_number_invalid(self):
        """Тест маскировки некорректного номера карты."""
        result = mask_card_number("1234567890")
        assert result is None
