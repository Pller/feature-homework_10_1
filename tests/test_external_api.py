# -*- coding: utf-8 -*-
import os
from unittest.mock import Mock, patch
import pytest
from src.external_api import convert_currency


class TestExternalAPI:
    """Тестовые случаи для интеграции с внешними API."""

    def test_convert_currency_rub(self):
        """Тест конвертации когда транзакция уже в рублях."""
        transaction = {
            "amount": 1000.0,
            "currency": "RUB"
        }

        result = convert_currency(transaction)

        assert result == 1000.0
        assert isinstance(result, float)

    @patch('src.external_api.requests.get')
    def test_convert_currency_usd_with_api(self, mock_get):
        """Тест конвертации из USD в RUB с реальным API вызовом."""
        # Мок ответа API
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": 9050.0
        }
        mock_get.return_value = mock_response

        # Устанавливаем тестовый API ключ
        with patch.dict(os.environ, {'EXCHANGERATES_API_KEY': 'real_test_key'}, clear=True):
            transaction = {
                "amount": 100.0,
                "currency": "USD"
            }

            result = convert_currency(transaction)

            assert result == 9050.0
            assert isinstance(result, float)

    def test_convert_currency_usd_without_api_key(self):
        """Тест конвертации без API ключа (должен использовать mock значения)."""
        # Убеждаемся, что переменная окружения не установлена
        with patch.dict(os.environ, {}, clear=True):
            transaction = {
                "amount": 100.0,
                "currency": "USD"
            }

            result = convert_currency(transaction)

            # Должен вернуть mock значение (100 * 90.0 = 9000.0)
            assert result == 9000.0
            assert isinstance(result, float)

    def test_convert_currency_eur_without_api_key(self):
        """Тест конвертации EUR без API ключа."""
        with patch.dict(os.environ, {}, clear=True):
            transaction = {
                "amount": 50.0,
                "currency": "EUR"
            }

            result = convert_currency(transaction)

            # Должен вернуть mock значение (50 * 100.0 = 5000.0)
            assert result == 5000.0
            assert isinstance(result, float)

    def test_convert_currency_other_currency(self):
        """Тест конвертации с неподдерживаемой валютой."""
        transaction = {
            "amount": 1000.0,
            "currency": "GBP"  # Не USD или EUR
        }

        result = convert_currency(transaction)

        assert result == 1000.0
        assert isinstance(result, float)


if __name__ == "__main__":
    pytest.main()