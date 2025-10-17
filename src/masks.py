"""Модуль для работы с масками карт и счетов."""
import logging
import os
from typing import Optional

# Настройка логера для модуля masks
def setup_masks_logger() -> logging.Logger:
    """Настраивает и возвращает логер для модуля masks."""
    logger = logging.getLogger('masks')
    logger.setLevel(logging.DEBUG)
    
    # Создаем папку logs если ее нет
    os.makedirs('logs', exist_ok=True)
    
    # File handler с перезаписью файла при каждом запуске
    file_handler = logging.FileHandler('logs/masks.log', mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Форматер логов
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Добавляем handler к логеру
    logger.addHandler(file_handler)
    
    return logger

# Создаем логер
masks_logger = setup_masks_logger()

def mask_account_number(account_number: str) -> Optional[str]:
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.
    
    Args:
        account_number: Номер счета
        
    Returns:
        str: Замаскированный номер счета или None при ошибке
    """
    try:
        if not account_number or len(account_number) < 4:
            masks_logger.error(f"Некорректный номер счета: {account_number}")
            return None
            
        masked = f"**{account_number[-4:]}"
        masks_logger.info(f"Успешно замаскирован номер счета: {account_number} -> {masked}")
        return masked
        
    except Exception as e:
        masks_logger.error(f"Ошибка при маскировке счета {account_number}: {e}")
        return None

def mask_card_number(card_number: str) -> Optional[str]:
    """
    Маскирует номер карты, оставляя видимыми первые 6 и последние 4 цифры.
    
    Args:
        card_number: Номер карты
        
    Returns:
        str: Замаскированный номер карты или None при ошибке
    """
    try:
        if not card_number or len(card_number) != 16:
            masks_logger.error(f"Некорректный номер карты: {card_number}")
            return None
            
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        masks_logger.info(f"Успешно замаскирован номер карты: {card_number} -> {masked}")
        return masked
        
    except Exception as e:
        masks_logger.error(f"Ошибка при маскировке карты {card_number}: {e}")
        return None
