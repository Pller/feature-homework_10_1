"""Тесты для модуля external_api."""
import os
from unittest.mock import Mock, patch
from src.external_api import convert_currency


class TestExternalAPI:
    """Тестовые случаи для интеграции с внешними API."""

    def test_convert_currency_rub(self):
        """Тест конвертации когда транзакция уже в рублях."""
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
    def test_convert_currency_usd_with_api(self, mock_get):
        """Тест конвертации из USD в RUB с реальным API вызовом."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": 9050.0
        }
        mock_get.return_value = mock_response
        with patch.dict(os.environ, {'EXCHANGERATES_API_KEY': 'real_test_key'}, clear=True):
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

    def test_convert_currency_usd_without_api_key(self):
        """Тест конвертации без API ключа."""
        with patch.dict(os.environ, {}, clear=True):
            transaction = {
                "operationAmount": {
                    "amount": "100.0",
                    "currency": {
                        "code": "USD"
                    }
                }
            }
            result = convert_currency(transaction)
            assert result == 100.0
            assert isinstance(result, float)

    def test_convert_currency_eur_without_api_key(self):
        """Тест конвертации EUR без API ключа."""
        with patch.dict(os.environ, {}, clear=True):
            transaction = {
                "operationAmount": {
                    "amount": "50.0",
                    "currency": {
                        "code": "EUR"
                    }
                }
            }
            result = convert_currency(transaction)
            assert result == 50.0
            assert isinstance(result, float)

    def test_convert_currency_other_currency(self):
        """Тест конвертации с неподдерживаемой валютой."""
        transaction = {
            "operationAmount": {
                "amount": "1000.0",
                "currency": {
                    "code": "GBP"
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


if __name__ == "__main__":
    import pytest
    pytest.main()
