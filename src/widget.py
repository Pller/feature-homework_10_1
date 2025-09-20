def get_mask_card_number(card_number: str) -> str:
    """

    Args:
        card_number: Номер карты (16 цифр)

    Returns:
        Замаскированный номер в формате XXXX XX** **** XXXX
    """
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account_number(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    Args:
        account_number: Номер счета (20 цифр)

    Returns:
        Замаскированный номер в формате **XXXX
    """
    if len(account_number) != 20 or not account_number.isdigit():
        raise ValueError("Номер счета должен содержать 20 цифр")

    return f"**{account_number[-4:]}"
