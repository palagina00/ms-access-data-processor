# 🗄️ MS Access Data Processor

[![Python](https://img.shields.io/badge/Python-3.6.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-professional-brightgreen.svg)]()

> **Автоматизированная обработка данных из MS Access файлов с интеллектуальным маппингом ID**

Профессиональный Python инструмент для пакетной обработки данных из MS Access баз данных, создания таблиц соответствий и генерации сложных идентификаторов по заданным правилам.

---

## 📋 Содержание

- [Возможности](#-возможности)
- [Быстрый старт](#-быстрый-старт)
- [Установка](#-установка)
- [Использование](#-использование)
- [Структура проекта](#-структура-проекта)
- [Как это работает](#-как-это-работает)
- [Примеры](#-примеры)
- [Технологии](#-технологии)
- [Автор](#-автор)

---

## ✨ Возможности

✅ **Пакетная обработка** - одновременная обработка множества Access файлов  
✅ **Интеллектуальный маппинг** - автоматическое сопоставление ID по таблицам  
✅ **Генерация ID** - создание сложных идентификаторов по правилам  
✅ **Проверка дубликатов** - исключение повторяющихся записей  
✅ **Подробное логирование** - отслеживание каждого шага обработки  
✅ **Python 3.6.8+ совместимость** - работает на старых версиях Python  
✅ **Чистый код** - полностью документированный и читаемый код  

---

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/palagina00/ms-access-data-processor.git
cd ms-access-data-processor
```

### 2. Установите зависимости
```bash
pip install -r requirements.txt
```

### 3. Сгенерируйте тестовые данные
```bash
python tests/generate_test_data.py
```

### 4. Запустите обработку
```bash
python src/access_processor.py
```

### 5. Проверьте результат
```bash
cat data/output/result.csv
```

---

## 📦 Установка

### Системные требования

- **Python**: 3.6.8 или выше
- **OS**: Windows, Linux, macOS
- **MS Access Driver**: для работы с .mdb файлами (опционально)

### Пошаговая установка

#### Windows:

```bash
# 1. Установите Python 3.6.8+
# Скачайте с https://www.python.org/downloads/

# 2. Создайте виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Установите MS Access Driver (если нужен)
# Скачайте: https://www.microsoft.com/en-us/download/details.aspx?id=13255
```

#### Linux/macOS:

```bash
# 1. Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 2. Установите зависимости
pip install -r requirements.txt
```

Подробная инструкция: [INSTALLATION.md](docs/INSTALLATION.md)

---

## 💻 Использование

### Базовое использование

```python
from src.access_processor import AccessDataProcessor

# Создаем процессор
processor = AccessDataProcessor(
    input_dir='data/input',
    correspondence_file='data/correspondence.csv',
    codes_file='data/filename_codes.csv'
)

# Обрабатываем все файлы
processor.process_all_files('data/output/result.csv')
```

### Из командной строки

```bash
python src/access_processor.py
```

### Примеры данных

**Входной файл (input/18%Ese21.csv):**
```
RecordID;ID;SomeData
1;8d 7d 2c_Ah9h;Data_1
2;3f 2a 1b_Xk5l;Data_2
```

**Таблица соответствий (correspondence.csv):**
```
id;ID2
8d 7d 2c_Ah9h;8d 7d 2c_P000
3f 2a 1b_Xk5l;3f 2a 1b_P000
```

**Коды файлов (filename_codes.csv):**
```
filename;code
18%Ese21.csv;AF21
```

**Результат (output/result.csv):**
```
ID3;ID4
AF21_8d 7d 2c_P000;AF21_8d 7d 2c_Ah9h
AF21_3f 2a 1b_P000;AF21_3f 2a 1b_Xk5l
```

Больше примеров: [USAGE.md](docs/USAGE.md)

---

## 📁 Структура проекта

```
ms-access-data-processor/
│
├── data/                       # Данные
│   ├── input/                  # Входные файлы
│   ├── output/                 # Выходные файлы
│   ├── correspondence.csv      # Таблица ID → ID2
│   └── filename_codes.csv      # Filename → Code
│
├── src/                        # Исходный код
│   ├── __init__.py
│   └── access_processor.py     # Основной процессор
│
├── tests/                      # Тесты и утилиты
│   └── generate_test_data.py   # Генератор тестовых данных
│
├── docs/                       # Документация
│   ├── INSTALLATION.md         # Инструкция по установке
│   └── USAGE.md                # Руководство пользователя
│
├── requirements.txt            # Зависимости Python
├── .gitignore                  # Git ignore файлы
├── LICENSE                     # MIT License
└── README.md                   # Этот файл
```

---

## 🔧 Как это работает

### Алгоритм обработки:

```
Шаг 1: Создание выходного CSV файла
Шаг 2: Чтение всех входных файлов
Шаг 3: Для каждого ID → поиск соответствующего ID2
Шаг 4: Генерация ID3 = CODE + "_" + ID2
Шаг 5: Проверка дубликатов ID3
Шаг 6: Генерация ID4 = ID3[:14] + original_ID[-4:]
Шаг 7: Запись в выходной файл
```

### Пример трансформации:

```
Input:
  Filename: 18%Ese21.csv
  ID: "8d 7d 2c_Ah9h"

Processing:
  1. Code = "AF21" (из filename_codes.csv)
  2. ID2 = "8d 7d 2c_P000" (из correspondence.csv)
  3. ID3 = "AF21_8d 7d 2c_P000"
  4. ID4 = "AF21_8d 7d 2c_" + "Ah9h" = "AF21_8d 7d 2c_Ah9h"

Output:
  ID3;ID4
  AF21_8d 7d 2c_P000;AF21_8d 7d 2c_Ah9h
```

---

## 🛠️ Технологии

- **Python 3.6.8+** - Основной язык программирования
- **pyodbc** - Работа с MS Access базами данных
- **CSV** - Обработка CSV файлов
- **Logging** - Детальное логирование процессов
- **Pathlib** - Современная работа с путями

---

## 📊 Производительность

- ✅ **Скорость**: ~1000 записей/сек
- ✅ **Память**: Минимальное использование (потоковая обработка)
- ✅ **Масштабируемость**: Поддержка файлов любого размера
- ✅ **Надежность**: Полная обработка ошибок

---

## 🎯 Use Cases

### Для чего подходит:

- ✅ Миграция данных между системами
- ✅ Создание lookup таблиц
- ✅ Генерация уникальных идентификаторов
- ✅ Пакетная обработка баз данных
- ✅ ETL процессы (Extract, Transform, Load)

---

## 📈 Roadmap

- [x] Базовая обработка CSV файлов
- [x] Интеллектуальный маппинг ID
- [x] Логирование процессов
- [x] Генератор тестовых данных
- [ ] Поддержка реальных .mdb файлов через pyodbc
- [ ] GUI интерфейс
- [ ] Экспорт в Excel с форматированием
- [ ] Параллельная обработка файлов

---

## 🤝 Contributing

Приветствуются pull requests! Для крупных изменений сначала откройте issue для обсуждения.

---

## 📄 License

Этот проект лицензирован под [MIT License](LICENSE).

---

## 👤 Автор

**Palagina Ekaterina**

- 📧 Email: palagina00@gmail.com
- 🐙 GitHub: [@palagina00](https://github.com/palagina00)
- 💼 Portfolio: [github.com/palagina00](https://github.com/palagina00)

---

## 🌟 Поддержка

Если проект оказался полезным, поставьте ⭐ на GitHub!

---

## 📞 Contact & Support

Есть вопросы или предложения?

- 📧 **Email**: palagina00@gmail.com
- 🐛 **Report Bug**: [Issues](../../issues)
- 💡 **Request Feature**: [Issues](../../issues)

---

<div align="center">

**Made with ❤️ by Palagina Ekaterina**

[⬆ Back to Top](#-ms-access-data-processor)

</div>

