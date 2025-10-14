import json
from typing import List, Dict, Any


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON файл и возвращает список транзакций.

    Args:
        file_path: Путь к JSON файлу

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список при ошибке
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Убеждаемся что данные это список
        if isinstance(data, list):
            return data
        else:
            print(f"Предупреждение: JSON файл {file_path} не содержит список")
            return []

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {file_path} содержит некорректный JSON")
        return []
    except Exception as e:
        print(f"Ошибка чтения файла {file_path}: {e}")
        return []
