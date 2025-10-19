"""
Test Data Generator for MS Access Data Processor
Creates test .mdb files and CSV for script demonstration
"""

import csv
import random
import string
import os

# For working with Access files we use simple CSV for demonstration
# In real project need pyodbc and MS Access Driver

def generate_random_id():
    """Generates random ID in format: '8d 7d 2c_Ah9h'"""
    part1 = ''.join(random.choices('0123456789abcdef', k=2))
    part2 = ''.join(random.choices('0123456789abcdef', k=2))
    part3 = ''.join(random.choices('0123456789abcdef', k=2))
    part4 = ''.join(random.choices(string.ascii_letters + string.digits, k=2))
    part5 = ''.join(random.choices(string.ascii_letters + string.digits, k=2))
    
    return f"{part1} {part2} {part3}_{part4}{part5}"


def generate_id2_from_id(original_id):
    """Generates ID2 from ID (first 9 characters are the same)"""
    # Take first 9 characters (e.g., '8d 7d 2c_')
    prefix = original_id[:9]
    # Add 'P000'
    return f"{prefix}P000"


def create_input_files():
    """Creates test input files (simulating .mdb)"""
    print("📁 Creating test input files...")
    
    # Create folder for input files
    input_dir = os.path.join('data', 'input')
    os.makedirs(input_dir, exist_ok=True)
    
    # List of files to create
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
        
        # Generate 20 random records for each file
        ids = [generate_random_id() for _ in range(20)]
        all_ids.extend(ids)
        
        # Save to CSV (simulating table from .mdb)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['RecordID', 'ID', 'SomeData'])
            
            for idx, record_id in enumerate(ids, 1):
                writer.writerow([idx, record_id, f'Data_{idx}'])
        
        print(f"  ✅ Created: {filename} ({len(ids)} records)")
    
    return all_ids, test_files


def create_correspondence_table(all_ids):
    """Creates ID → ID2 correspondence table"""
    print("\n📋 Creating correspondence table...")
    
    correspondence_file = os.path.join('data', 'correspondence.csv')
    
    with open(correspondence_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['id', 'ID2'])
        
        for original_id in all_ids:
            id2 = generate_id2_from_id(original_id)
            writer.writerow([original_id, id2])
    
    print(f"  ✅ Created correspondence table: {len(all_ids)} records")


def create_filename_codes(test_files):
    """Creates CSV with filename → code mapping"""
    print("\n🏷️  Creating filename_codes.csv...")
    
    codes_file = os.path.join('data', 'filename_codes.csv')
    
    with open(codes_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['filename', 'code'])
        
        for filename, code in test_files:
            writer.writerow([filename, code])
    
    print(f"  ✅ Created codes file: {len(test_files)} records")


def main():
    """Main function for test data generation"""
    print("\n" + "="*60)
    print("🔧 TEST DATA GENERATOR")
    print("="*60 + "\n")
    
    # Create input files
    all_ids, test_files = create_input_files()
    
    # Create correspondence table
    create_correspondence_table(all_ids)
    
    # Create codes file
    create_filename_codes(test_files)
    
    # Create empty output folder
    output_dir = os.path.join('data', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("✅ TEST DATA CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📊 Statistics:")
    print(f"  • Input files: {len(test_files)}")
    print(f"  • Total ID records: {len(all_ids)}")
    print(f"  • Correspondence table: {len(all_ids)} records")
    print(f"  • Code files: {len(test_files)}")
    print(f"\n📁 Data structure:")
    print(f"  • data/input/ - input CSV files (simulating .mdb)")
    print(f"  • data/correspondence.csv - ID → ID2 table")
    print(f"  • data/filename_codes.csv - filename → code mapping")
    print(f"  • data/output/ - folder for results\n")


if __name__ == '__main__':
    main()
