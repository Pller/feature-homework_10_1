import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.processing import filter_by_state, sort_by_date
# #class TestProcessingFunctions(unittest.TestCase):
#
#     def setUp(self):
#         self.test_data = [
#             {'id': 41428829, 'state': 'EXECUTED',
#              'date': '2019-07-03T18:35:29.512364'},
#             {'id': 939719570, 'state': 'EXECUTED',
#              'date': '2018-06-30T02:08:58.425572'},
#             {'id': 594226727, 'state': 'CANCELED',
#              'date': '2018-09-12T21:27:25.241689'},
#             {'id': 615064591, 'state': 'CANCELED',
#              'date': '2018-10-14T08:21:33.419441'}
#         ]
#
#     def test_filter_by_state_executed(self):
#         result = filter_by_state(self.test_data, 'EXECUTED')
#         self.assertEqual(len(result), 2)
#         self.assertTrue(all(op['state'] == 'EXECUTED' for op in result))
#         self.assertEqual(result[0]['id'], 41428829)
#         self.assertEqual(result[1]['id'], 939719570)
#
#     def test_filter_by_state_canceled(self):
#         result = filter_by_state(self.test_data, 'CANCELED')
#         self.assertEqual(len(result), 2)
#         self.assertTrue(all(op['state'] == 'CANCELED' for op in result))
#         self.assertEqual(result[0]['id'], 594226727)
#         self.assertEqual(result[1]['id'], 615064591)
#
#     def test_filter_by_state_default(self):
#         result = filter_by_state(self.test_data)
#         self.assertEqual(len(result), 2)
#         self.assertTrue(all(op['state'] == 'EXECUTED' for op in result))
#
#     def test_sort_by_date_descending(self):
#         result = sort_by_date(self.test_data, True)
#         dates = [op['date'] for op in result]
#         expected_dates = [
#             '2019-07-03T18:35:29.512364',
#             '2018-10-14T08:21:33.419441',
#             '2018-09-12T21:27:25.241689',
#             '2018-06-30T02:08:58.425572'
#         ]
#         self.assertEqual(dates, expected_dates)
#
#     def test_sort_by_date_ascending(self):
#         result = sort_by_date(self.test_data, False)
#         dates = [op['date'] for op in result]
#         expected_dates = [
#             '2018-06-30T02:08:58.425572',
#             '2018-09-12T21:27:25.241689',
#             '2018-10-14T08:21:33.419441',
#             '2019-07-03T18:35:29.512364'
#         ]
#         self.assertEqual(dates, expected_dates)
#
#     def test_empty_data(self):
#         self.assertEqual(filter_by_state([]), [])
#         self.assertEqual(sort_by_date([]
class TestProcessing:
    """Тесты для модуля processing."""

    def test_filter_by_state_executed(self):
        """Тестирование фильтрации по статусу EXECUTED."""
        operations = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},
            {"id": 2, "state": "CANCELED", "date": "2024-01-02T10:00:00"},
        ]
        result = filter_by_state(operations, "EXECUTED")
        assert len(result) == 1
        assert result[0]["state"] == "EXECUTED"

    def test_filter_by_state_canceled(self):
        """Тестирование фильтрации по статусу CANCELED."""
        operations = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},
            {"id": 2, "state": "CANCELED", "date": "2024-01-02T10:00:00"},
        ]
        result = filter_by_state(operations, "CANCELED")
        assert len(result) == 1
        assert result[0]["state"] == "CANCELED"

    def test_filter_by_state_default(self):
        """Тестирование фильтрации со статусом по умолчанию."""
        operations = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},
            {"id": 2, "state": "CANCELED", "date": "2024-01-02T10:00:00"},
        ]
        result = filter_by_state(operations)
        assert len(result) == 1
        assert result[0]["state"] == "EXECUTED"

    def test_filter_by_state_empty_list(self):
        """Тестирование фильтрации пустого списка."""
        result = filter_by_state([])
        assert result == []

    def test_filter_by_state_no_matching(self):
        """Тестирование фильтрации когда нет совпадений."""
        operations = [{"id": 1, "state": "PENDING", "date": "2024-01-01T10:00:00"}]
        result = filter_by_state(operations, "EXECUTED")
        assert result == []

    def test_sort_by_date_descending(self):
        """Тестирование сортировки по убыванию даты."""
        operations = [
            {"id": 1, "date": "2024-01-01T10:00:00"},
            {"id": 2, "date": "2024-01-02T10:00:00"},
        ]
        result = sort_by_date(operations, True)
        assert result[0]["date"] == "2024-01-02T10:00:00"
        assert result[1]["date"] == "2024-01-01T10:00:00"

    def test_sort_by_date_ascending(self):
        """Тестирование сортировки по возрастанию даты."""
        operations = [
            {"id": 1, "date": "2024-01-02T10:00:00"},
            {"id": 2, "date": "2024-01-01T10:00:00"},
        ]
        result = sort_by_date(operations, False)
        assert result[0]["date"] == "2024-01-01T10:00:00"
        assert result[1]["date"] == "2024-01-02T10:00:00"

    def test_sort_by_date_default(self):
        """Тестирование сортировки с порядком по умолчанию."""
        operations = [
            {"id": 1, "date": "2024-01-01T10:00:00"},
            {"id": 2, "date": "2024-01-02T10:00:00"},
        ]
        result = sort_by_date(operations)
        assert result[0]["date"] == "2024-01-02T10:00:00"

    def test_sort_by_date_empty_list(self):
        """Тестирование сортировки пустого списка."""
        result = sort_by_date([])
        assert result == []

    def test_sort_by_date_single_item(self):
        """Тестирование сортировки списка с одним элементом."""
        operations = [{"id": 1, "date": "2024-01-01T10:00:00"}]
        result = sort_by_date(operations)
        assert result == operations

    def test_sort_by_date_invalid_date(self):
        """Тестирование сортировки с некорректной датой."""
        operations = [
            {"id": 1, "date": "2024-01-01T10:00:00"},
            {"id": 2, "date": ""},
            {"id": 3, "date": "invalid-date"},
        ]
        result = sort_by_date(operations)
        # Функция должна обработать некорректные даты и поместить их в начало/конец
        assert len(result) == 3
        # Проверяем что валидная дата на своем месте
        valid_dates = [op for op in result if op["date"] == "2024-01-01T10:00:00"]
        assert len(valid_dates) == 1
