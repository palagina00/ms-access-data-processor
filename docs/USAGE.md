# 💻 Руководство пользователя MS Access Data Processor

Полное руководство по использованию проекта с примерами и best practices.

---

## 📋 Содержание

- [Быстрый старт](#быстрый-старт)
- [Подготовка данных](#подготовка-данных)
- [Запуск обработки](#запуск-обработки)
- [Примеры использования](#примеры-использования)
- [Настройка логирования](#настройка-логирования)
- [FAQ](#faq)

---

## 🚀 Быстрый старт

### 1. Подготовка среды

```bash
# Активируйте виртуальное окружение
# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate
```

### 2. Генерация тестовых данных

```bash
python tests/generate_test_data.py
```

### 3. Запуск обработки

```bash
python src/access_processor.py
```

### 4. Просмотр результатов

```bash
# Windows
type data\output\result.csv

# Linux/macOS
cat data/output/result.csv
```

---

## 📁 Подготовка данных

### Структура входных данных

Для работы скрипта необходимо подготовить 3 типа файлов:

#### 1. Входные файлы (data/input/)

**Формат**: CSV с разделителем `;`

**Обязательные колонки**:
- `RecordID` - уникальный номер записи
- `ID` - идентификатор для обработки
- `SomeData` - дополнительные данные (опционально)

**Пример (18%Ese21.csv)**:
```csv
RecordID;ID;SomeData
1;8d 7d 2c_Ah9h;Data_1
2;3f 2a 1b_Xk5l;Data_2
3;5e 9c 4d_Bm3n;Data_3
```

#### 2. Таблица соответствий (data/correspondence.csv)

**Формат**: CSV с разделителем `;`

**Обязательные колонки**:
- `id` - исходный ID
- `ID2` - соответствующий ID2

**Правило**: Первые 9 символов `id` и `ID2` должны совпадать

**Пример**:
```csv
id;ID2
8d 7d 2c_Ah9h;8d 7d 2c_P000
3f 2a 1b_Xk5l;3f 2a 1b_P000
5e 9c 4d_Bm3n;5e 9c 4d_P000
```

#### 3. Коды файлов (data/filename_codes.csv)

**Формат**: CSV с разделителем `;`

**Обязательные колонки**:
- `filename` - имя файла из data/input/
- `code` - код для генерации ID3

**Пример**:
```csv
filename;code
18%Ese21.csv;AF21
19%Ese22.csv;BG22
20%Ese23.csv;CH23
```

---

## ⚙️ Запуск обработки

### Базовое использование

```bash
python src/access_processor.py
```

### Использование в коде

```python
from src.access_processor import AccessDataProcessor

# Создаем процессор
processor = AccessDataProcessor(
    input_dir='data/input',
    correspondence_file='data/correspondence.csv',
    codes_file='data/filename_codes.csv'
)

# Обрабатываем файлы
processor.process_all_files('data/output/result.csv')
```

### С кастомными путями

```python
processor = AccessDataProcessor(
    input_dir='my_data/inputs',
    correspondence_file='my_data/mappings.csv',
    codes_file='my_data/codes.csv'
)

processor.process_all_files('my_data/outputs/custom_result.csv')
```

---

## 📊 Примеры использования

### Пример 1: Базовая обработка

**Входные данные**:

`data/input/test.csv`:
```csv
RecordID;ID;SomeData
1;8d 7d 2c_Ah9h;Product A
```

`data/correspondence.csv`:
```csv
id;ID2
8d 7d 2c_Ah9h;8d 7d 2c_P000
```

`data/filename_codes.csv`:
```csv
filename;code
test.csv;AF21
```

**Команда**:
```bash
python src/access_processor.py
```

**Результат** (`data/output/result.csv`):
```csv
ID3;ID4
AF21_8d 7d 2c_P000;AF21_8d 7d 2c_Ah9h
```

### Пример 2: Множественные файлы

**Файлы**:
- `data/input/file1.csv` (10 записей)
- `data/input/file2.csv` (15 записей)
- `data/input/file3.csv` (20 записей)

**Команда**:
```bash
python src/access_processor.py
```

**Результат**:
- Обработано 3 файла
- Создано 45 уникальных записей
- Время обработки: ~1 секунда

### Пример 3: Обработка дубликатов

**Сценарий**: Один и тот же ID встречается в разных файлах

`file1.csv`:
```csv
RecordID;ID;SomeData
1;8d 7d 2c_Ah9h;Data_1
```

`file2.csv`:
```csv
RecordID;ID;SomeData
1;8d 7d 2c_Ah9h;Data_2
```

**Результат**:
```csv
ID3;ID4
AF21_8d 7d 2c_P000;AF21_8d 7d 2c_Ah9h
```

⚠️ **Дубликат не добавлен** - ID3 уже существует в выходном файле

---

## 📝 Настройка логирования

### Уровни логирования

Логирование настраивается в файле `src/access_processor.py`:

```python
logging.basicConfig(
    level=logging.INFO,  # Измените на DEBUG для подробного лога
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('processor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
```

### Доступные уровни:

- `DEBUG` - максимально подробный лог (каждая запись)
- `INFO` - основные события (по умолчанию)
- `WARNING` - только предупреждения и ошибки
- `ERROR` - только ошибки

### Пример вывода лога:

```
2025-10-19 16:00:00 - INFO - ✅ AccessDataProcessor инициализирован
2025-10-19 16:00:01 - INFO - 📖 Загружаю таблицу соответствий: data\correspondence.csv
2025-10-19 16:00:01 - INFO - ✅ Загружено 100 соответствий ID → ID2
2025-10-19 16:00:02 - INFO - 📁 Найдено 5 входных файлов
2025-10-19 16:00:03 - INFO - ✅ ОБРАБОТКА ЗАВЕРШЕНА УСПЕШНО!
```

---

## 🎯 Понимание результатов

### Формат выходного файла

**result.csv**:
```csv
ID3;ID4
AF21_8d 7d 2c_P000;AF21_8d 7d 2c_Ah9h
```

### Расшифровка полей:

| Поле | Описание | Пример | Формула |
|------|----------|--------|---------|
| **ID3** | Комбинированный ID | `AF21_8d 7d 2c_P000` | `CODE + "_" + ID2` |
| **ID4** | Финальный ID | `AF21_8d 7d 2c_Ah9h` | `ID3[:14] + original_ID[-4:]` |

### Логика генерации:

```python
# Исходные данные
filename = "18%Ese21.csv"
original_id = "8d 7d 2c_Ah9h"

# Шаг 1: Получаем код
code = "AF21"  # из filename_codes.csv

# Шаг 2: Получаем ID2
id2 = "8d 7d 2c_P000"  # из correspondence.csv

# Шаг 3: Генерируем ID3
id3 = f"{code}_{id2}"  # "AF21_8d 7d 2c_P000"

# Шаг 4: Генерируем ID4
id4 = id3[:14] + original_id[-4:]  # "AF21_8d 7d 2c_" + "Ah9h"
```

---

## ❓ FAQ

### Q: Можно ли обрабатывать реальные .mdb файлы?

**A**: Да, но требуется установка MS Access Driver (см. [INSTALLATION.md](INSTALLATION.md)). Текущая версия работает с CSV для демонстрации.

### Q: Что делать, если ID не найден в таблице соответствий?

**A**: Скрипт пропустит эту запись и запишет предупреждение в лог:
```
⚠️  ID 'unknown_id' не найден в таблице соответствий
```

### Q: Сколько файлов можно обработать за раз?

**A**: Нет ограничений. Скрипт обрабатывает файлы потоково, поэтому может работать с любым количеством.

### Q: Как изменить разделитель CSV?

**A**: В файле `src/access_processor.py` найдите:
```python
reader = csv.DictReader(f, delimiter=';')
```
Замените `;` на нужный разделитель (`,`, `\t`, и т.д.)

### Q: Можно ли экспортировать в Excel?

**A**: Текущая версия экспортирует в CSV. Для Excel добавьте:
```python
import pandas as pd

df = pd.read_csv('data/output/result.csv', delimiter=';')
df.to_excel('data/output/result.xlsx', index=False)
```

### Q: Как обработать файлы из другой папки?

**A**: Укажите путь при создании процессора:
```python
processor = AccessDataProcessor(
    input_dir='/path/to/your/files',
    correspondence_file='/path/to/correspondence.csv',
    codes_file='/path/to/codes.csv'
)
```

---

## 🐛 Troubleshooting

### Проблема: "Файл не найден"

```bash
FileNotFoundError: [Errno 2] No such file or directory: 'data/input'
```

**Решение**:
```bash
# Создайте папки
mkdir -p data/input data/output

# Сгенерируйте тестовые данные
python tests/generate_test_data.py
```

### Проблема: "Пустой результат"

**Причины**:
1. Нет входных файлов в `data/input/`
2. Файлы не указаны в `filename_codes.csv`
3. ID не найдены в `correspondence.csv`

**Решение**: Проверьте логи в `processor.log`

### Проблема: "Кодировка не читается"

```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```

**Решение**: Конвертируйте файлы в UTF-8 или измените кодировку:
```python
with open(file, 'r', encoding='windows-1251') as f:
```

---

## 📈 Best Practices

### 1. Всегда проверяйте входные данные

```bash
# Проверьте формат CSV
head data/input/file.csv

# Проверьте кодировку
file data/input/file.csv
```

### 2. Используйте логи для отладки

```python
# Включите DEBUG режим
logging.basicConfig(level=logging.DEBUG)
```

### 3. Делайте бэкапы

```bash
# Скопируйте результаты
cp data/output/result.csv data/output/result_backup_$(date +%Y%m%d).csv
```

### 4. Валидация данных

```python
# Проверьте результаты
import pandas as pd

df = pd.read_csv('data/output/result.csv', delimiter=';')
print(f"Обработано записей: {len(df)}")
print(f"Уникальных ID3: {df['ID3'].nunique()}")
```

---

## 📞 Поддержка

Нужна помощь?

- 📧 **Email**: palagina00@gmail.com
- 🐛 **Issues**: [GitHub Issues](../../issues)
- 📚 **Документация**: [README](../README.md)

---

<div align="center">

**Счастливой обработки данных! 🚀**

[⬅️ Назад к README](../README.md)

</div>

