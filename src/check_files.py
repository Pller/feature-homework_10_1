"""Скрипт для проверки структуры файлов."""
import sys

# Добавляем src в путь для импорта
sys.path.append('src')

from file_reader import read_csv_file, read_excel_file

print("=== ПРОВЕРКА СТРУКТУРЫ ФАЙЛОВ ===")

# Проверим CSV
try:
    csv_data = read_csv_file('data/transactions.csv')
    print(f"CSV файл: {len(csv_data)} записей")
    if csv_data:
        print("Первая запись CSV:", csv_data[0])
        print("Ключи CSV:", list(csv_data[0].keys()))
except Exception as e:
    print(f"Ошибка чтения CSV: {e}")

print("\n" + "="*50)

# Проверим Excel
try:
    excel_data = read_excel_file('data/transactions_excel.xlsx')
    print(f"Excel файл: {len(excel_data)} записей")
    if excel_data:
        print("Первая запись Excel:", excel_data[0])
        print("Ключи Excel:", list(excel_data[0].keys()))
except Exception as e:
    print(f"Ошибка чтения Excel: {e}")
