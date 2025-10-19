"""
MS Access Data Processor - Main Processing Module
Processes Access files and creates ID correspondence tables
"""

import csv
import os
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Setup logging
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
    """Class for processing data from Access files"""
    
    def __init__(self, input_dir: str, correspondence_file: str, codes_file: str):
        """
        Initialize processor
        
        Args:
            input_dir: Directory with input files
            correspondence_file: File with ID → ID2 correspondence table
            codes_file: File with filename → code mapping
        """
        self.input_dir = Path(input_dir)
        self.correspondence_file = Path(correspondence_file)
        self.codes_file = Path(codes_file)
        
        # Dictionaries for storing data
        self.id_to_id2: Dict[str, str] = {}
        self.filename_to_code: Dict[str, str] = {}
        self.processed_id3: Set[str] = set()
        
        logger.info("✅ AccessDataProcessor initialized")
    
    def load_correspondence_table(self):
        """Load ID → ID2 correspondence table"""
        logger.info(f"📖 Loading correspondence table: {self.correspondence_file}")
        
        try:
            with open(self.correspondence_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    self.id_to_id2[row['id']] = row['ID2']
            
            logger.info(f"✅ Loaded {len(self.id_to_id2)} ID → ID2 correspondences")
        except Exception as e:
            logger.error(f"❌ Error loading correspondence table: {e}")
            raise
    
    def load_filename_codes(self):
        """Load filename → code mapping"""
        logger.info(f"📖 Loading file codes: {self.codes_file}")
        
        try:
            with open(self.codes_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    self.filename_to_code[row['filename']] = row['code']
            
            logger.info(f"✅ Loaded {len(self.filename_to_code)} file codes")
        except Exception as e:
            logger.error(f"❌ Error loading file codes: {e}")
            raise
    
    def get_input_files(self) -> List[Path]:
        """Get list of all input files"""
        files = list(self.input_dir.glob('*.csv'))
        logger.info(f"📁 Found {len(files)} input files")
        return files
    
    def process_file(self, filepath: Path) -> List[Tuple[str, str]]:
        """
        Process one input file
        
        Args:
            filepath: Path to file
            
        Returns:
            List of tuples (ID3, ID4)
        """
        filename = filepath.name
        logger.info(f"📄 Processing file: {filename}")
        
        # Get code for this file
        if filename not in self.filename_to_code:
            logger.warning(f"⚠️  Code for file {filename} not found, skipping")
            return []
        
        code = self.filename_to_code[filename]
        results = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                
                for row_num, row in enumerate(reader, 1):
                    original_id = row['ID']
                    
                    # Step 3: Find corresponding ID2
                    if original_id not in self.id_to_id2:
                        logger.warning(f"⚠️  ID '{original_id}' not found in correspondence table")
                        continue
                    
                    id2 = self.id_to_id2[original_id]
                    
                    # Step 4: Create ID3
                    id3 = f"{code}_{id2}"
                    
                    # Step 5: Check for duplicates
                    if id3 in self.processed_id3:
                        logger.debug(f"⏩ ID3 '{id3}' already processed, skipping")
                        continue
                    
                    # Step 6: Create ID4
                    # ID4 = first 14 characters of ID3 + last 4 characters of original_id
                    id4 = id3[:14] + original_id[-4:]
                    
                    # Add to results
                    results.append((id3, id4))
                    self.processed_id3.add(id3)
                    
                    logger.debug(f"✅ Processed record {row_num}: {id3} → {id4}")
            
            logger.info(f"✅ File {filename}: processed {len(results)} new records")
            
        except Exception as e:
            logger.error(f"❌ Error processing file {filename}: {e}")
            raise
        
        return results
    
    def process_all_files(self, output_file: str):
        """
        Process all input files and create output CSV
        
        Args:
            output_file: Path to output file
        """
        logger.info("\n" + "="*60)
        logger.info("🚀 STARTING PROCESSING")
        logger.info("="*60 + "\n")
        
        # Load reference data
        self.load_correspondence_table()
        self.load_filename_codes()
        
        # Get file list
        input_files = self.get_input_files()
        
        if not input_files:
            logger.warning("⚠️  No files to process")
            return
        
        # Create output file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"\n📝 Creating output file: {output_file}")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['ID3', 'ID4'])
            
            total_records = 0
            
            # Process each file
            for filepath in input_files:
                results = self.process_file(filepath)
                
                # Write results
                for id3, id4 in results:
                    writer.writerow([id3, id4])
                    total_records += 1
        
        logger.info("\n" + "="*60)
        logger.info("✅ PROCESSING COMPLETED SUCCESSFULLY!")
        logger.info("="*60)
        logger.info(f"\n📊 Statistics:")
        logger.info(f"  • Files processed: {len(input_files)}")
        logger.info(f"  • Unique records: {total_records}")
        logger.info(f"  • Output file: {output_file}")
        logger.info(f"  • File size: {output_path.stat().st_size} bytes\n")


def main():
    """Main function"""
    # File paths
    INPUT_DIR = 'data/input'
    CORRESPONDENCE_FILE = 'data/correspondence.csv'
    CODES_FILE = 'data/filename_codes.csv'
    OUTPUT_FILE = 'data/output/result.csv'
    
    # Create processor
    processor = AccessDataProcessor(
        input_dir=INPUT_DIR,
        correspondence_file=CORRESPONDENCE_FILE,
        codes_file=CODES_FILE
    )
    
    # Process all files
    processor.process_all_files(OUTPUT_FILE)


if __name__ == '__main__':
    main()

