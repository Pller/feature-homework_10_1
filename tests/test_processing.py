import unittest
from src.processing import filter_by_state, sort_by_date


class TestProcessingFunctions(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            {'id': 41428829, 'state': 'EXECUTED',
             'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED',
             'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED',
             'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED',
             'date': '2018-10-14T08:21:33.419441'}
        ]

    def test_filter_by_state_executed(self):
        result = filter_by_state(self.test_data, 'EXECUTED')
        self.assertEqual(len(result), 2)
        self.assertTrue(all(op['state'] == 'EXECUTED' for op in result))
        self.assertEqual(result[0]['id'], 41428829)
        self.assertEqual(result[1]['id'], 939719570)

    def test_filter_by_state_canceled(self):
        result = filter_by_state(self.test_data, 'CANCELED')
        self.assertEqual(len(result), 2)
        self.assertTrue(all(op['state'] == 'CANCELED' for op in result))
        self.assertEqual(result[0]['id'], 594226727)
        self.assertEqual(result[1]['id'], 615064591)

    def test_filter_by_state_default(self):
        result = filter_by_state(self.test_data)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(op['state'] == 'EXECUTED' for op in result))

    def test_sort_by_date_descending(self):
        result = sort_by_date(self.test_data, True)
        dates = [op['date'] for op in result]
        expected_dates = [
            '2019-07-03T18:35:29.512364',
            '2018-10-14T08:21:33.419441',
            '2018-09-12T21:27:25.241689',
            '2018-06-30T02:08:58.425572'
        ]
        self.assertEqual(dates, expected_dates)

    def test_sort_by_date_ascending(self):
        result = sort_by_date(self.test_data, False)
        dates = [op['date'] for op in result]
        expected_dates = [
            '2018-06-30T02:08:58.425572',
            '2018-09-12T21:27:25.241689',
            '2018-10-14T08:21:33.419441',
            '2019-07-03T18:35:29.512364'
        ]
        self.assertEqual(dates, expected_dates)

    def test_empty_data(self):
        self.assertEqual(filter_by_state([]), [])
        self.assertEqual(sort_by_date([]), [])
