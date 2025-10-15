import os
from unittest.mock import Mock, patch
import pytest
from src.external_api import convert_currency


class TestExternalAPI:
    """Тесты для функций работы с внешними API."""

    def test_convert_currency_rub(self):
        """Тест конвертации RUB в RUB."""
        transaction = {
            "operationAmount": {
                "amount": "1000.0",
                "currency": {
                    "code": "RUB"
                }
            }
        }
        result = convert_currency(transaction)
        assert result == 1000.0
        assert isinstance(result, float)

    @patch('src.external_api.requests.get')
    def test_convert_currency_usd(self, mock_get):
        """Тест конвертации USD в RUB с моком API."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": 9050.0
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'EXCHANGERATES_API_KEY': 'test_key'}):
            transaction = {
                "operationAmount": {
                    "amount": "100.0",
                    "currency": {
                        "code": "USD"
                    }
                }
            }
            result = convert_currency(transaction)
            assert result == 9050.0
            assert isinstance(result, float)

    @patch('src.external_api.requests.get')
    def test_convert_currency_eur(self, mock_get):
        """Тест конвертации EUR в RUB с моком API."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": 5010.0
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'EXCHANGERATES_API_KEY': 'test_key'}):
            transaction = {
                "operationAmount": {
                    "amount": "50.0",
                    "currency": {
                        "code": "EUR"
                    }
                }
            }
            result = convert_currency(transaction)
            assert result == 5010.0
            assert isinstance(result, float)

    def test_convert_currency_no_api_key(self):
        """Тест конвертации без API ключа."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {
                    "code": "USD"
                }
            }
        }
        result = convert_currency(transaction)
        assert result == 100.0  # Без API ключа возвращает исходную сумму
        assert isinstance(result, float)

    def test_convert_currency_other_currency(self):
        """Тест конвертации неподдерживаемой валюты."""
        transaction = {
            "operationAmount": {
                "amount": "1000.0",
                "currency": {
                    "code": "GBP"  # Не USD или EUR
                }
            }
        }
        result = convert_currency(transaction)
        assert result == 1000.0
        assert isinstance(result, float)

    def test_convert_currency_invalid_amount(self):
        """Тест конвертации с некорректной суммой."""
        transaction = {
            "operationAmount": {
                "amount": "invalid",
                "currency": {
                    "code": "USD"
                }
            }
        }
        result = convert_currency(transaction)
        assert result == 0.0
        assert isinstance(result, float)
