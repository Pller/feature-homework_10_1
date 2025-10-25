"""Тесты для модуля чтения файлов."""
from src.file_reader import read_csv_file, read_excel_file


class TestRealFiles:
    """Тесты с реальными файлами транзакций."""

    def test_read_real_csv_file(self):
        """Тест чтения реального CSV файла."""
        result = read_csv_file('data/transactions.csv')

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(item, dict) for item in result)

        # Проверяем что есть ожидаемые ключи (реальная структура)
        first_transaction = result[0]
        expected_keys = [
            'id', 'state', 'date', 'amount', 'currency_name',
            'currency_code', 'from', 'to', 'description'
        ]
        for key in expected_keys:
            assert key in first_transaction

    def test_read_real_excel_file(self):
        """Тест чтения реального Excel файла."""
        result = read_excel_file('data/transactions_excel.xlsx')

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(item, dict) for item in result)

        # Проверяем что есть ожидаемые ключи (реальная структура)
        first_transaction = result[0]
        expected_keys = [
            'id', 'state', 'date', 'amount', 'currency_name',
            'currency_code', 'from', 'to', 'description'
        ]
        for key in expected_keys:
            assert key in first_transaction

    def test_csv_and_excel_have_same_structure(self):
        """Тест что CSV и Excel файлы имеют одинаковую структуру."""
        csv_data = read_csv_file('data/transactions.csv')
        excel_data = read_excel_file('data/transactions_excel.xlsx')

        # Проверяем что оба файла содержат данные
        assert len(csv_data) > 0
        assert len(excel_data) > 0

        # Проверяем что структура одинаковая
        csv_keys = set(csv_data[0].keys())
        excel_keys = set(excel_data[0].keys())

        assert csv_keys == excel_keys, f"Разные ключи: CSV {csv_keys} vs Excel {excel_keys}"
