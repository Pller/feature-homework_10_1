import datetime
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функций.

    Args:
        filename: Имя файла для записи логов. Если None, логи выводятся в консоль.

    Returns:
        Декорированную функцию
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Получаем текущее время
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                success_message = f"{current_time} {func_name} ok\n"

                # Логируем в файл или консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(success_message)
                else:
                    print(success_message, end="")

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = f"{current_time} {func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"

                # Логируем в файл или консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(error_message)
                else:
                    print(error_message, end="")

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator
