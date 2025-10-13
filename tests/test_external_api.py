import os
import sys
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.external_api import convert_currency_to_rub, get_exchange_rate


class TestExternalApi:
    """Тесты для модуля external_api."""

    def test_convert_currency_to_rub_rub(self):
        """Тестирование конвертации RUB в RUB."""
        transaction = {
            "operationAmount": {
                "amount": "1000.0",
                "currency": {"code": "RUB"}
            }
        }
        result = convert_currency_to_rub(transaction)
        assert result == 1000.0

    def test_convert_currency_to_rub_invalid_amount(self):
        """Тестирование конвертации с невалидной суммой."""
        transaction = {
            "operationAmount": {
                "amount": "invalid",
                "currency": {"code": "RUB"}
            }
        }
        result = convert_currency_to_rub(transaction)
        assert result == 0.0

    def test_convert_currency_to_rub_missing_operation_amount(self):
        """Тестирование конвертации с отсутствующим operationAmount."""
        transaction = {}
        result = convert_currency_to_rub(transaction)
        assert result == 0.0

    @patch('src.external_api.get_exchange_rate')
    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'})
    def test_convert_currency_to_rub_usd(self, mock_get_rate):
        """Тестирование конвертации USD в RUB."""
        mock_get_rate.return_value = 90.0

        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "USD"}
            }
        }
        result = convert_currency_to_rub(transaction)
        assert result == 9000.0
        mock_get_rate.assert_called_once_with("USD", "RUB", "test_key")

    @patch('src.external_api.get_exchange_rate')
    @patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'})
    def test_convert_currency_to_rub_eur(self, mock_get_rate):
        """Тестирование конвертации EUR в RUB."""
        mock_get_rate.return_value = 100.0

        transaction = {
            "operationAmount": {
                "amount": "50.0",
                "currency": {"code": "EUR"}
            }
        }
        result = convert_currency_to_rub(transaction)
        assert result == 5000.0
        mock_get_rate.assert_called_once_with("EUR", "RUB", "test_key")

    @patch.dict(os.environ, {}, clear=True)
    def test_convert_currency_to_rub_no_api_key(self):
        """Тестирование конвертации без API ключа."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "USD"}
            }
        }
        with pytest.raises(ValueError, match="API key for exchange rates not found"):
            convert_currency_to_rub(transaction)

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        """Тестирование успешного получения курса валют."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "rates": {"RUB": 95.5}
        }
        mock_get.return_value = mock_response

        result = get_exchange_rate("USD", "RUB", "test_key")
        assert result == 95.5

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_fallback(self, mock_get):
        """Тестирование использования fallback курса при ошибке API."""
        mock_get.side_effect = Exception("API error")

        result = get_exchange_rate("USD", "RUB", "test_key")
        assert result == 90.0  # Fallback rate for USD
