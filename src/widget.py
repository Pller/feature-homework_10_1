from .masks import get_mask_card_number, get_mask_account_number
from datetime import datetime


def mask_account_card(data: str) -> str:
    """
    Маскирует номер банковской карты или счета в строке.

    Args:
        data: Строка с типом и номером карты/счета
            (например: "Visa Platinum 7000792289606361" или "Счет 73654108430135874305")

    Returns:
        Строка с замаскированным номером
    """
    parts = data.split()

    if len(parts) < 2:
        raise ValueError("Некорректный формат входных данных")

    card_type = " ".join(parts[:-1])
    number = parts[-1]

    if card_type.lower() == "счет":
        if len(number) != 20 or not number.isdigit():
            raise ValueError("Номер счета должен содержать 20 цифр")
        masked_number = get_mask_account_number(number)
    else:
        if len(number) != 16 or not number.isdigit():
            raise ValueError("Номер карты должен содержать 16 цифр")
        masked_number = get_mask_card_number(number)

    return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_string: Дата в формате "2024-03-11T02:26:18.671407"

    Returns:
        Дата в формате "11.03.2024"
    """
    try:
        # Проверяем что строка содержит 'T' (ISO format)
        if 'T' not in date_string:
            return "01.01.0001"

        date_part = date_string.split('T')[0]
        year, month, day = date_part.split('-')

        # Проверяем что все компоненты даты существуют
        if not all([year, month, day]):
            return "01.01.0001"

        return f"{day}.{month}.{year}"
    except (IndexError, ValueError, AttributeError):
        return "01.01.0001"
