from .masks import get_mask_card_number, get_mask_account
from datetime import datetime


def mask_account_card(data: str) -> str:
    """Маскирует карту или счет."""
    parts = data.split()
    if len(parts) < 2:
        raise ValueError("Некорректный формат")

    card_type = " ".join(parts[:-1])
    number = parts[-1]

    if card_type.lower() == "счет":
        return f"{card_type} {get_mask_account(number)}"
    else:
        return f"{card_type} {get_mask_card_number(number)}"


def get_date(date_string: str) -> str:
    """Форматирует дату."""
    date_part = date_string.split('T')[0]
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"