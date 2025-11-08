"""Основной модуль программы работы с банковскими транзакциями."""
from typing import List, Dict, Any
import os
from src.file_reader import read_csv_file, read_excel_file
from src.utils import read_json_file
from src.processing import (
    search_transactions_by_description,
    count_transactions_by_categories,
    filter_transactions_by_status,
    sort_transactions_by_date,
    filter_rub_transactions
)


def display_transaction(transaction: Dict[str, Any]) -> None:
    """Выводит информацию о транзакции в читаемом формате."""
    date = transaction.get('date', '')[:10]  # Берем только дату
    description = transaction.get('description', '')
    amount = transaction.get('amount', '')
    currency = transaction.get('currency_name', 'руб.')

    print(f"{date} {description}")
    print(f"Сумма: {amount} {currency}")
    print()


def get_user_choice(options: List[str], prompt: str) -> str:
    """Получает выбор пользователя из доступных опций."""
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        try:
            choice = input("Ваш выбор: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice) - 1]
            else:
                print("Пожалуйста, введите корректный номер пункта.")
        except ValueError:
            print("Пожалуйста, введите число.")


def get_yes_no_choice(prompt: str) -> bool:
    """Получает ответ Да/Нет от пользователя."""
    while True:
        choice = input(prompt + " (Да/Нет): ").strip().lower()
        if choice in ['да', 'д', 'yes', 'y']:
            return True
        elif choice in ['нет', 'н', 'no', 'n']:
            return False
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'.")


def get_status_choice() -> str:
    """Получает статус операции от пользователя."""
    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']

    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтрации статусы: {', '.join(valid_statuses)}")
        status = input("Статус: ").strip().upper()

        if status in valid_statuses:
            return status
        else:
            print(f'Статус операции "{status}" недоступен.\n')


def main() -> None:
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбор типа файла
    file_type = get_user_choice(
        ["Получить информацию о транзакциях из JSON-файла",
         "Получить информацию о транзакциях из CSV-файла",
         "Получить информацию о транзакциях из XLSX-файла"],
        "Выберите необходимый пункт меню:"
    )

    # Загрузка данных
    transactions = []
    if "JSON" in file_type:
        print("Для обработки выбран JSON-файл.")
        file_path = "data/operations.json"
        if os.path.exists(file_path):
            transactions = read_json_file(file_path)
        else:
            print(f"Файл {file_path} не найден.")
            return
    elif "CSV" in file_type:
        print("Для обработки выбран CSV-файл.")
        transactions = read_csv_file("data/transactions.csv")
    elif "XLSX" in file_type:
        print("Для обработки выбран XLSX-файл.")
        transactions = read_excel_file("data/transactions_excel.xlsx")

    if not transactions:
        print("Не удалось загрузить транзакции или файл пуст.")
        return

    # Фильтрация по статусу
    status = get_status_choice()
    filtered_transactions = filter_transactions_by_status(transactions, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    if get_yes_no_choice("Отсортировать операции по дате?"):
        sort_order = get_user_choice(
            ["по возрастанию", "по убыванию"],
            "Отсортировать по возрастанию или по убыванию?"
        )
        reverse = sort_order == "по убыванию"
        filtered_transactions = sort_transactions_by_date(filtered_transactions, reverse)

    # Фильтрация рублевых транзакций
    if get_yes_no_choice("Выводить только рублевые транзакции?"):
        filtered_transactions = filter_rub_transactions(filtered_transactions)

    # Поиск по описанию
    if get_yes_no_choice("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            filtered_transactions = search_transactions_by_description(filtered_transactions, search_word)

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    if filtered_transactions:
        for transaction in filtered_transactions:
            display_transaction(transaction)
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


if __name__ == "__main__":
    main()
