"""Тесты для модуля обработки транзакций."""
from src.processing import (
    search_transactions_by_description,
    count_transactions_by_categories,
    filter_transactions_by_status,
    sort_transactions_by_date,
    filter_rub_transactions
)


class TestProcessing:
    """Тесты функций обработки транзакций."""

    def setup_method(self):
        """Подготовка тестовых данных."""
        self.sample_data = [
            {
                'id': 1,
                'state': 'EXECUTED',
                'date': '2023-01-01',
                'amount': 100.0,
                'currency_name': 'рубль',
                'currency_code': 'RUB',
                'description': 'Перевод организации'
            },
            {
                'id': 2,
                'state': 'CANCELED',
                'date': '2023-01-02',
                'amount': 200.0,
                'currency_name': 'USD',
                'currency_code': 'USD',
                'description': 'Покупка в магазине'
            },
            {
                'id': 3,
                'state': 'EXECUTED',
                'date': '2023-01-03',
                'amount': 300.0,
                'currency_name': 'евро',
                'currency_code': 'EUR',
                'description': 'Перевод другу'
            }
        ]

    def test_search_transactions_by_description(self):
        """Тест поиска транзакций по описанию."""
        result = search_transactions_by_description(self.sample_data, 'перевод')
        assert len(result) == 2
        assert all('перевод' in transaction['description'].lower() for transaction in result)

    def test_search_transactions_case_insensitive(self):
        """Тест поиска без учета регистра."""
        result = search_transactions_by_description(self.sample_data, 'ПЕРЕВОД')
        assert len(result) == 2

    def test_count_transactions_by_categories(self):
        """Тест подсчета операций по категориям."""
        categories = ['перевод', 'покупка']
        result = count_transactions_by_categories(self.sample_data, categories)
        assert result['перевод'] == 2
        assert result['покупка'] == 1

    def test_filter_transactions_by_status(self):
        """Тест фильтрации по статусу."""
        result = filter_transactions_by_status(self.sample_data, 'EXECUTED')
        assert len(result) == 2
        assert all(transaction['state'] == 'EXECUTED' for transaction in result)

    def test_filter_invalid_status(self):
        """Тест фильтрации по неверному статусу."""
        result = filter_transactions_by_status(self.sample_data, 'INVALID')
        assert result == []

    def test_sort_transactions_by_date(self):
        """Тест сортировки по дате."""
        result_asc = sort_transactions_by_date(self.sample_data, reverse=False)
        result_desc = sort_transactions_by_date(self.sample_data, reverse=True)

        assert result_asc[0]['date'] == '2023-01-01'
        assert result_desc[0]['date'] == '2023-01-03'

    def test_filter_rub_transactions(self):
        """Тест фильтрации рублевых транзакций."""
        result = filter_rub_transactions(self.sample_data)
        assert len(result) == 1
        assert result[0]['currency_code'] == 'RUB'
