"""
Генератор тестовых данных для MS Access Data Processor
Создает тестовые .mdb файлы и CSV для демонстрации работы скрипта
"""

import csv
import random
import string
import os

# Для работы с Access файлами используем простой CSV для демонстрации
# В реальном проекте нужен pyodbc и MS Access Driver

def generate_random_id():
    """Генерирует случайный ID в формате: '8d 7d 2c_Ah9h'"""
    part1 = ''.join(random.choices('0123456789abcdef', k=2))
    part2 = ''.join(random.choices('0123456789abcdef', k=2))
    part3 = ''.join(random.choices('0123456789abcdef', k=2))
    part4 = ''.join(random.choices(string.ascii_letters + string.digits, k=2))
    part5 = ''.join(random.choices(string.ascii_letters + string.digits, k=2))
    
    return f"{part1} {part2} {part3}_{part4}{part5}"


def generate_id2_from_id(original_id):
    """Генерирует ID2 из ID (первые 9 символов одинаковые)"""
    # Берем первые 9 символов (например, '8d 7d 2c_')
    prefix = original_id[:9]
    # Добавляем 'P000'
    return f"{prefix}P000"


def create_input_files():
    """Создает тестовые входные файлы (имитация .mdb)"""
    print("📁 Создаю тестовые входные файлы...")
    
    # Создаем папку для input файлов
    input_dir = os.path.join('data', 'input')
    os.makedirs(input_dir, exist_ok=True)
    
    # Список файлов для создания
    test_files = [
        ('18%Ese21.csv', 'AF21'),
        ('19%Ese22.csv', 'BG22'),
        ('20%Ese23.csv', 'CH23'),
        ('21%Ese24.csv', 'DI24'),
        ('22%Ese25.csv', 'EJ25')
    ]
    
    all_ids = []
    
    for filename, code in test_files:
        filepath = os.path.join(input_dir, filename)
        
        # Генерируем 20 случайных записей для каждого файла
        ids = [generate_random_id() for _ in range(20)]
        all_ids.extend(ids)
        
        # Сохраняем в CSV (имитация таблицы из .mdb)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['RecordID', 'ID', 'SomeData'])
            
            for idx, record_id in enumerate(ids, 1):
                writer.writerow([idx, record_id, f'Data_{idx}'])
        
        print(f"  ✅ Создан: {filename} ({len(ids)} записей)")
    
    return all_ids, test_files


def create_correspondence_table(all_ids):
    """Создает таблицу соответствий ID → ID2"""
    print("\n📋 Создаю таблицу соответствий...")
    
    correspondence_file = os.path.join('data', 'correspondence.csv')
    
    with open(correspondence_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['id', 'ID2'])
        
        for original_id in all_ids:
            id2 = generate_id2_from_id(original_id)
            writer.writerow([original_id, id2])
    
    print(f"  ✅ Создана таблица соответствий: {len(all_ids)} записей")


def create_filename_codes(test_files):
    """Создает CSV с соответствием filename → code"""
    print("\n🏷️  Создаю файл filename_codes.csv...")
    
    codes_file = os.path.join('data', 'filename_codes.csv')
    
    with open(codes_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['filename', 'code'])
        
        for filename, code in test_files:
            writer.writerow([filename, code])
    
    print(f"  ✅ Создан файл кодов: {len(test_files)} записей")


def main():
    """Главная функция генерации тестовых данных"""
    print("\n" + "="*60)
    print("🔧 ГЕНЕРАТОР ТЕСТОВЫХ ДАННЫХ")
    print("="*60 + "\n")
    
    # Создаем входные файлы
    all_ids, test_files = create_input_files()
    
    # Создаем таблицу соответствий
    create_correspondence_table(all_ids)
    
    # Создаем файл кодов
    create_filename_codes(test_files)
    
    # Создаем пустую папку output
    output_dir = os.path.join('data', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("✅ ТЕСТОВЫЕ ДАННЫЕ СОЗДАНЫ УСПЕШНО!")
    print("="*60)
    print(f"\n📊 Статистика:")
    print(f"  • Входных файлов: {len(test_files)}")
    print(f"  • Всего ID записей: {len(all_ids)}")
    print(f"  • Таблица соответствий: {len(all_ids)} записей")
    print(f"  • Файлов кодов: {len(test_files)}")
    print(f"\n📁 Структура данных:")
    print(f"  • data/input/ - входные CSV файлы (имитация .mdb)")
    print(f"  • data/correspondence.csv - таблица ID → ID2")
    print(f"  • data/filename_codes.csv - соответствие filename → code")
    print(f"  • data/output/ - папка для результатов\n")


if __name__ == '__main__':
    main()

