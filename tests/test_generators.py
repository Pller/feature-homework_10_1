import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions():
    """Фикстура с примером транзакций для тестирования."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


class TestGenerators:
    """Тесты для модуля generators."""

    def test_filter_by_currency_usd(self, sample_transactions):
        """Тестирование фильтрации транзакций по USD."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 3
        assert all(
            tx["operationAmount"]["currency"]["code"] == "USD" for tx in usd_transactions
        )

    def test_filter_by_currency_rub(self, sample_transactions):
        """Тестирование фильтрации транзакций по RUB."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 2
        assert all(
            tx["operationAmount"]["currency"]["code"] == "RUB" for tx in rub_transactions
        )

    def test_filter_by_currency_empty(self):
        """Тестирование фильтрации пустого списка."""
        result = list(filter_by_currency([], "USD"))
        assert result == []

    def test_filter_by_currency_no_matches(self, sample_transactions):
        """Тестирование фильтрации когда нет совпадений."""
        result = list(filter_by_currency(sample_transactions, "EUR"))
        assert result == []

    def test_filter_by_currency_iterator(self, sample_transactions):
        """Тестирование что функция возвращает итератор."""
        result = filter_by_currency(sample_transactions, "USD")
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

        first_transaction = next(result)
        assert first_transaction["id"] == 939719570

    def test_transaction_descriptions(self, sample_transactions):
        """Тестирование генератора описаний транзакций."""
        descriptions = list(transaction_descriptions(sample_transactions))
        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
        assert descriptions == expected

    def test_transaction_descriptions_iterator(self, sample_transactions):
        """Тестирование что функция возвращает итератор."""
        result = transaction_descriptions(sample_transactions)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

        first_description = next(result)
        assert first_description == "Перевод организации"

    def test_transaction_descriptions_empty(self):
        """Тестирование генератора описаний с пустым списком."""
        result = list(transaction_descriptions([]))
        assert result == []

    @pytest.mark.parametrize(
        "start,end,expected",
        [
            (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
            (9999, 10001, ["0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001"]),
            (1, 1, ["0000 0000 0000 0001"]),
        ],
    )
    def test_card_number_generator(self, start, end, expected):
        """Тестирование генератора номеров карт с параметризацией."""
        result = list(card_number_generator(start, end))
        assert result == expected

    def test_card_number_generator_format(self):
        """Тестирование формата номеров карт."""
        result = list(card_number_generator(1234567890123456, 1234567890123456))
        assert result == ["1234 5678 9012 3456"]

    def test_card_number_generator_iterator(self):
        """Тестирование что функция возвращает итератор."""
        result = card_number_generator(1, 5)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

        first_number = next(result)
        assert first_number == "0000 0000 0000 0001"
