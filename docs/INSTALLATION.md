# 📦 Руководство по установке MS Access Data Processor

Подробная пошаговая инструкция по установке и настройке проекта на различных операционных системах.

---

## 📋 Содержание

- [Системные требования](#системные-требования)
- [Установка Python](#установка-python)
- [Установка проекта](#установка-проекта)
- [Установка MS Access Driver](#установка-ms-access-driver)
- [Проверка установки](#проверка-установки)
- [Решение проблем](#решение-проблем)

---

## 💻 Системные требования

### Минимальные требования:

- **Python**: 3.6.8 или выше (рекомендуется 3.8+)
- **RAM**: 512 MB (рекомендуется 2 GB)
- **Disk Space**: 100 MB
- **OS**: Windows 7+, Ubuntu 18.04+, macOS 10.14+

### Дополнительно (опционально):

- **MS Access Driver** - для работы с реальными .mdb файлами
- **Git** - для клонирования репозитория

---

## 🐍 Установка Python

### Windows:

#### Вариант 1: Официальный установщик (Рекомендуется)

1. **Скачайте Python**:
   - Перейдите на [python.org/downloads](https://www.python.org/downloads/)
   - Скачайте Python 3.8+ (или минимум 3.6.8)

2. **Запустите установщик**:
   ```
   ⚠️ ВАЖНО: Поставьте галочку "Add Python to PATH"
   ```

3. **Проверьте установку**:
   ```bash
   python --version
   ```
   Должно показать: `Python 3.x.x`

#### Вариант 2: Microsoft Store

```bash
# Откройте Microsoft Store
# Найдите "Python 3.10" или новее
# Нажмите "Установить"
```

### Linux (Ubuntu/Debian):

```bash
# Обновите пакеты
sudo apt update

# Установите Python 3 и pip
sudo apt install python3 python3-pip python3-venv

# Проверьте установку
python3 --version
pip3 --version
```

### macOS:

#### Вариант 1: Homebrew (Рекомендуется)

```bash
# Установите Homebrew (если еще нет)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установите Python
brew install python

# Проверьте установку
python3 --version
```

#### Вариант 2: Официальный установщик

1. Скачайте с [python.org/downloads](https://www.python.org/downloads/)
2. Откройте .pkg файл и следуйте инструкциям

---

## 🚀 Установка проекта

### Шаг 1: Получите исходный код

#### Вариант A: С помощью Git (Рекомендуется)

```bash
# Клонируйте репозиторий
git clone https://github.com/palagina00/ms-access-data-processor.git

# Перейдите в папку проекта
cd ms-access-data-processor
```

#### Вариант B: Скачать ZIP

1. Перейдите на [GitHub репозиторий](https://github.com/palagina00/ms-access-data-processor)
2. Нажмите "Code" → "Download ZIP"
3. Распакуйте архив
4. Откройте командную строку в папке проекта

### Шаг 2: Создайте виртуальное окружение

#### Windows:

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте окружение
venv\Scripts\activate

# Вы увидите (venv) в начале строки
```

#### Linux/macOS:

```bash
# Создайте виртуальное окружение
python3 -m venv venv

# Активируйте окружение
source venv/bin/activate

# Вы увидите (venv) в начале строки
```

### Шаг 3: Установите зависимости

```bash
# Обновите pip (опционально)
pip install --upgrade pip

# Установите зависимости проекта
pip install -r requirements.txt
```

**Должны установиться:**
- `pyodbc>=4.0.30` - для работы с MS Access
- `pandas>=1.1.5` - для обработки данных (опционально)

---

## 🗄️ Установка MS Access Driver

### Windows:

#### Для 64-bit систем:

1. **Скачайте драйвер**:
   - [Microsoft Access Database Engine 2016 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=54920)
   - Выберите `AccessDatabaseEngine_X64.exe`

2. **Установите**:
   ```bash
   # Запустите установщик
   AccessDatabaseEngine_X64.exe
   ```

3. **Проверьте установку**:
   ```python
   import pyodbc
   print(pyodbc.drivers())
   # Должен быть 'Microsoft Access Driver (*.mdb, *.accdb)'
   ```

#### Для 32-bit систем:

- Скачайте `AccessDatabaseEngine.exe` (32-bit версию)

### Linux:

```bash
# Установите ODBC драйвер
sudo apt-get install unixodbc unixodbc-dev

# Для работы с .mdb используйте mdbtools
sudo apt-get install mdbtools
```

### macOS:

```bash
# Установите через Homebrew
brew install unixodbc
```

⚠️ **Примечание**: На Linux/macOS полноценная работа с .mdb ограничена. Рекомендуется конвертировать .mdb в CSV на Windows.

---

## ✅ Проверка установки

### Проверьте Python и зависимости:

```bash
# Проверьте Python
python --version

# Проверьте pip
pip --version

# Проверьте установленные пакеты
pip list
```

### Сгенерируйте тестовые данные:

```bash
python tests/generate_test_data.py
```

**Ожидаемый результат:**
```
================================================================
🔧 ГЕНЕРАТОР ТЕСТОВЫХ ДАННЫХ
================================================================

📁 Создаю тестовые входные файлы...
  ✅ Создан: 18%Ese21.csv (20 записей)
  ✅ Создан: 19%Ese22.csv (20 записей)
  ...

================================================================
✅ ТЕСТОВЫЕ ДАННЫЕ СОЗДАНЫ УСПЕШНО!
================================================================
```

### Запустите обработку:

```bash
python src/access_processor.py
```

**Ожидаемый результат:**
```
================================================================
🚀 НАЧАЛО ОБРАБОТКИ
================================================================

📖 Загружаю таблицу соответствий: data\correspondence.csv
✅ Загружено 100 соответствий ID → ID2
...

================================================================
✅ ОБРАБОТКА ЗАВЕРШЕНА УСПЕШНО!
================================================================
```

### Проверьте результат:

```bash
# Windows
type data\output\result.csv

# Linux/macOS
cat data/output/result.csv
```

---

## 🐛 Решение проблем

### Проблема: "python не является внутренней командой"

**Решение (Windows):**
1. Добавьте Python в PATH:
   - `Панель управления` → `Система` → `Дополнительные параметры системы`
   - `Переменные среды` → `Path` → `Изменить`
   - Добавьте: `C:\Users\YOUR_USER\AppData\Local\Programs\Python\Python3X`

2. Или используйте:
   ```bash
   py --version
   ```

### Проблема: "pip install" не работает

**Решение:**
```bash
# Windows
python -m pip install -r requirements.txt

# Linux/macOS
python3 -m pip install -r requirements.txt
```

### Проблема: "No module named 'pyodbc'"

**Решение:**
```bash
# Убедитесь, что виртуальное окружение активно
# Должно быть (venv) в начале строки

# Установите pyodbc отдельно
pip install pyodbc

# Если ошибка компиляции на Linux:
sudo apt-get install python3-dev
pip install pyodbc
```

### Проблема: "MS Access Driver not found"

**Решение:**
1. Проверьте установленные драйверы:
   ```python
   import pyodbc
   print(pyodbc.drivers())
   ```

2. Установите драйвер (см. раздел "Установка MS Access Driver")

3. Используйте CSV файлы вместо .mdb (для тестирования)

### Проблема: Ошибка при запуске на Linux

**Решение:**
```bash
# Дайте права на выполнение
chmod +x src/access_processor.py

# Запустите с python3
python3 src/access_processor.py
```

---

## 📞 Поддержка

Если у вас возникли проблемы:

1. Проверьте [Issues на GitHub](../../issues)
2. Создайте новый Issue с описанием проблемы
3. Напишите на palagina00@gmail.com

---

## ✅ Чек-лист установки

- [ ] Python 3.6.8+ установлен
- [ ] Виртуальное окружение создано
- [ ] Зависимости установлены (requirements.txt)
- [ ] MS Access Driver установлен (опционально)
- [ ] Тестовые данные сгенерированы
- [ ] Скрипт успешно запущен
- [ ] Результат создан в data/output/

---

<div align="center">

**Готово! Проект установлен и готов к использованию! 🎉**

[⬅️ Назад к README](../README.md)

</div>

