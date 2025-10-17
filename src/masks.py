"""Модуль для работы с масками карт и счетов."""
import logging


def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает маску номера карты.

    Args:
        card_number: Номер карты

    Returns:
        str: Маска номера карты
    """
    if len(card_number) != 16 or not card_number.isdigit():
        return "Некорректный номер карты"

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера счета.

    Args:
        account_number: Номер счета

    Returns:
        str: Маска номера счета
    """
    if len(account_number) != 20 or not account_number.isdigit():
        return "Некорректный номер счета"

    return f"**{account_number[-4:]}"


# Настройка логгера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("masks.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def mask_card_number_with_log(card_number: str) -> str:
    """
    Возвращает маску номера карты с логированием.

    Args:
        card_number: Номер карты

    Returns:
        str: Маска номера карты
    """
    try:
        result = get_mask_card_number(card_number)
        logger.debug(f"Успешное создание маски карты: {card_number} -> {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка создания маски карты: {card_number} - {e}")
        return "Ошибка создания маски"


def mask_account_number_with_log(account_number: str) -> str:
    """
    Возвращает маску номера счета с логированием.

    Args:
        account_number: Номер счета

    Returns:
        str: Маска номера счета
    """
    try:
        result = get_mask_account(account_number)
        logger.debug(f"Успешное создание маски счета: {account_number} -> {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка создания маски счета: {account_number} - {e}")
        return "Ошибка создания маски"
