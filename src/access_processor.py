"""
MS Access Data Processor - Основной модуль обработки
Обрабатывает Access файлы и создает таблицы соответствий ID
"""

import csv
import os
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('processor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AccessDataProcessor:
    """Класс для обработки данных из Access файлов"""
    
    def __init__(self, input_dir: str, correspondence_file: str, codes_file: str):
        """
        Инициализация процессора
        
        Args:
            input_dir: Папка с входными файлами
            correspondence_file: Файл с таблицей соответствий ID → ID2
            codes_file: Файл с соответствием filename → code
        """
        self.input_dir = Path(input_dir)
        self.correspondence_file = Path(correspondence_file)
        self.codes_file = Path(codes_file)
        
        # Словари для хранения данных
        self.id_to_id2: Dict[str, str] = {}
        self.filename_to_code: Dict[str, str] = {}
        self.processed_id3: Set[str] = set()
        
        logger.info("✅ AccessDataProcessor инициализирован")
    
    def load_correspondence_table(self):
        """Загружает таблицу соответствий ID → ID2"""
        logger.info(f"📖 Загружаю таблицу соответствий: {self.correspondence_file}")
        
        try:
            with open(self.correspondence_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    self.id_to_id2[row['id']] = row['ID2']
            
            logger.info(f"✅ Загружено {len(self.id_to_id2)} соответствий ID → ID2")
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки таблицы соответствий: {e}")
            raise
    
    def load_filename_codes(self):
        """Загружает соответствие filename → code"""
        logger.info(f"📖 Загружаю коды файлов: {self.codes_file}")
        
        try:
            with open(self.codes_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    self.filename_to_code[row['filename']] = row['code']
            
            logger.info(f"✅ Загружено {len(self.filename_to_code)} кодов файлов")
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки кодов файлов: {e}")
            raise
    
    def get_input_files(self) -> List[Path]:
        """Получает список всех входных файлов"""
        files = list(self.input_dir.glob('*.csv'))
        logger.info(f"📁 Найдено {len(files)} входных файлов")
        return files
    
    def process_file(self, filepath: Path) -> List[Tuple[str, str]]:
        """
        Обрабатывает один входной файл
        
        Args:
            filepath: Путь к файлу
            
        Returns:
            Список кортежей (ID3, ID4)
        """
        filename = filepath.name
        logger.info(f"📄 Обрабатываю файл: {filename}")
        
        # Получаем код для этого файла
        if filename not in self.filename_to_code:
            logger.warning(f"⚠️  Код для файла {filename} не найден, пропускаю")
            return []
        
        code = self.filename_to_code[filename]
        results = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                
                for row_num, row in enumerate(reader, 1):
                    original_id = row['ID']
                    
                    # Шаг 3: Поиск соответствующего ID2
                    if original_id not in self.id_to_id2:
                        logger.warning(f"⚠️  ID '{original_id}' не найден в таблице соответствий")
                        continue
                    
                    id2 = self.id_to_id2[original_id]
                    
                    # Шаг 4: Создание ID3
                    id3 = f"{code}_{id2}"
                    
                    # Шаг 5: Проверка на дубликаты
                    if id3 in self.processed_id3:
                        logger.debug(f"⏩ ID3 '{id3}' уже обработан, пропускаю")
                        continue
                    
                    # Шаг 6: Создание ID4
                    # ID4 = первые 14 символов ID3 + последние 4 символа original_id
                    id4 = id3[:14] + original_id[-4:]
                    
                    # Добавляем в результаты
                    results.append((id3, id4))
                    self.processed_id3.add(id3)
                    
                    logger.debug(f"✅ Обработана запись {row_num}: {id3} → {id4}")
            
            logger.info(f"✅ Файл {filename}: обработано {len(results)} новых записей")
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки файла {filename}: {e}")
            raise
        
        return results
    
    def process_all_files(self, output_file: str):
        """
        Обрабатывает все входные файлы и создает выходной CSV
        
        Args:
            output_file: Путь к выходному файлу
        """
        logger.info("\n" + "="*60)
        logger.info("🚀 НАЧАЛО ОБРАБОТКИ")
        logger.info("="*60 + "\n")
        
        # Загружаем справочные данные
        self.load_correspondence_table()
        self.load_filename_codes()
        
        # Получаем список файлов
        input_files = self.get_input_files()
        
        if not input_files:
            logger.warning("⚠️  Нет файлов для обработки")
            return
        
        # Создаем выходной файл
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"\n📝 Создаю выходной файл: {output_file}")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['ID3', 'ID4'])
            
            total_records = 0
            
            # Обрабатываем каждый файл
            for filepath in input_files:
                results = self.process_file(filepath)
                
                # Записываем результаты
                for id3, id4 in results:
                    writer.writerow([id3, id4])
                    total_records += 1
        
        logger.info("\n" + "="*60)
        logger.info("✅ ОБРАБОТКА ЗАВЕРШЕНА УСПЕШНО!")
        logger.info("="*60)
        logger.info(f"\n📊 Статистика:")
        logger.info(f"  • Обработано файлов: {len(input_files)}")
        logger.info(f"  • Уникальных записей: {total_records}")
        logger.info(f"  • Выходной файл: {output_file}")
        logger.info(f"  • Размер файла: {output_path.stat().st_size} байт\n")


def main():
    """Главная функция"""
    # Пути к файлам
    INPUT_DIR = 'data/input'
    CORRESPONDENCE_FILE = 'data/correspondence.csv'
    CODES_FILE = 'data/filename_codes.csv'
    OUTPUT_FILE = 'data/output/result.csv'
    
    # Создаем процессор
    processor = AccessDataProcessor(
        input_dir=INPUT_DIR,
        correspondence_file=CORRESPONDENCE_FILE,
        codes_file=CODES_FILE
    )
    
    # Обрабатываем все файлы
    processor.process_all_files(OUTPUT_FILE)


if __name__ == '__main__':
    main()

