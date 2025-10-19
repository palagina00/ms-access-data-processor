# 💻 User Guide for MS Access Data Processor

Complete user guide with examples and best practices for using the project.

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Data Preparation](#data-preparation)
- [Running Processing](#running-processing)
- [Usage Examples](#usage-examples)
- [Logging Configuration](#logging-configuration)
- [FAQ](#faq)

---

## 🚀 Quick Start

### 1. Prepare Environment

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate
```

### 2. Navigate to Project Directory

```bash
cd ms-access-data-processor
```

### 3. Generate Test Data

```bash
# Generate sample data for testing
python tests/generate_test_data.py
```

### 4. Run Processing

```bash
# Process all files
python src/access_processor.py
```

### 5. Check Results

```bash
# View processed results
cat data/output/result.csv

# View processing log
cat processor.log
```

---

## 📊 Data Preparation

### Required File Structure:

```
data/
├── input/                    # Input files (CSV format)
│   ├── file1.csv
│   ├── file2.csv
│   └── ...
├── correspondence.csv        # ID → ID2 mapping
├── filename_codes.csv        # Filename → Code mapping
└── output/                   # Output directory (created automatically)
    └── result.csv           # Final results
```

### File Formats:

#### 1. Input Files (data/input/*.csv)

**Format**: CSV with semicolon separator

**Required Columns**:
- `ID`: Original identifier (e.g., "8d 7d 2c_Ah9h")

**Example**:
```csv
RecordID;ID;SomeData
1;8d 7d 2c_Ah9h;Data_1
2;3f 2a 1b_Xk5l;Data_2
3;5e 9c 4d_Bm3n;Data_3
```

#### 2. Correspondence Table (data/correspondence.csv)

**Format**: CSV with semicolon separator

**Columns**:
- `id`: Original ID
- `ID2`: Corresponding ID2

**Example**:
```csv
id;ID2
8d 7d 2c_Ah9h;8d 7d 2c_P000
3f 2a 1b_Xk5l;3f 2a 1b_P000
5e 9c 4d_Bm3n;5e 9c 4d_P000
```

#### 3. Filename Codes (data/filename_codes.csv)

**Format**: CSV with semicolon separator

**Columns**:
- `filename`: Input filename
- `code`: Corresponding code

**Example**:
```csv
filename;code
file1.csv;AF21
file2.csv;BG22
file3.csv;EJ25
```

---

## 🏃‍♂️ Running Processing

### Method 1: Command Line (Recommended)

```bash
# Process all files in data/input/
python src/access_processor.py
```

### Method 2: Python Script

```python
from src.access_processor import AccessDataProcessor

# Create processor instance
processor = AccessDataProcessor(
    input_dir='data/input',
    correspondence_file='data/correspondence.csv',
    codes_file='data/filename_codes.csv'
)

# Process all files
processor.process_all_files('data/output/result.csv')
```

### Method 3: Custom Configuration

```python
from src.access_processor import AccessDataProcessor

# Custom configuration
processor = AccessDataProcessor(
    input_dir='custom/input/path',
    correspondence_file='custom/correspondence.csv',
    codes_file='custom/codes.csv'
)

# Process specific file
processor.process_file('custom/input/specific_file.csv', 'custom/output/result.csv')
```

---

## 💡 Usage Examples

### Example 1: Basic Processing

```bash
# 1. Generate test data
python tests/generate_test_data.py

# 2. Run processing
python src/access_processor.py

# 3. Check results
head -10 data/output/result.csv
```

**Expected Output**:
```csv
ID3;ID4
AF21_8d 7d 2c_P000;AF21_8d 7d 2c_Ah9h
AF21_3f 2a 1b_P000;AF21_3f 2a 1b_Xk5l
BG22_5e 9c 4d_P000;BG22_5e 9c 4d_Bm3n
```

### Example 2: Custom Data Processing

```python
# Create custom processor
processor = AccessDataProcessor()

# Load custom correspondence table
processor.load_correspondence_table('custom_mapping.csv')

# Load custom filename codes
processor.load_filename_codes('custom_codes.csv')

# Process specific files
processor.process_file('data/input/special_file.csv', 'data/output/special_result.csv')
```

### Example 3: Batch Processing

```python
# Process multiple input directories
input_dirs = ['data/input1', 'data/input2', 'data/input3']

for input_dir in input_dirs:
    processor = AccessDataProcessor(input_dir=input_dir)
    output_file = f'data/output/results_{input_dir.split("/")[-1]}.csv'
    processor.process_all_files(output_file)
```

---

## ⚙️ Logging Configuration

### Log Levels:

The processor uses Python's logging module with different levels:

- **DEBUG**: Detailed processing information
- **INFO**: General processing steps
- **WARNING**: Non-critical issues
- **ERROR**: Processing errors

### Log File:

All logs are saved to `processor.log` with detailed information about:
- Processing start/end times
- File processing status
- Record counts
- Error messages

### Custom Logging:

```python
import logging

# Set custom log level
logging.getLogger().setLevel(logging.DEBUG)

# Or modify the processor directly
processor = AccessDataProcessor(...)
# Logs will be written to processor.log
```

---

## ❓ FAQ

### Q: What file formats are supported?

**A**: Currently supports CSV files with semicolon separators. MS Access .mdb files support is planned for future versions.

### Q: How do I handle large files?

**A**: The processor uses streaming processing, so it can handle files of any size. Memory usage remains constant regardless of file size.

### Q: What if I have missing IDs in correspondence table?

**A**: The processor will log warnings for missing IDs and skip those records. Check the log file for details.

### Q: Can I process files in parallel?

**A**: Currently, files are processed sequentially. Parallel processing is planned for future versions.

### Q: How do I customize the ID generation rules?

**A**: Modify the `process_file()` method in `src/access_processor.py` to change the ID3 and ID4 generation logic.

### Q: What if my CSV files use different separators?

**A**: Modify the `delimiter=';'` parameter in the `csv.DictReader()` calls in the processor code.

### Q: How do I add support for new file formats?

**A**: Extend the `process_file()` method to handle different file formats and extensions.

### Q: Can I run this on a schedule?

**A**: Yes, you can set up a cron job (Linux/macOS) or Task Scheduler (Windows) to run the processor automatically.

---

## 🔍 Troubleshooting

### Common Issues:

#### Issue 1: "File not found" errors

**Solution**:
- Check file paths in configuration
- Ensure all required files exist
- Verify file permissions

#### Issue 2: "No data processed" warnings

**Solution**:
- Check if input files contain data
- Verify CSV format and separators
- Check correspondence table completeness

#### Issue 3: Memory errors with large files

**Solution**:
- The processor should handle large files automatically
- Check available system memory
- Consider processing files in smaller batches

#### Issue 4: Duplicate ID3 warnings

**Solution**:
- This is normal behavior - duplicates are automatically skipped
- Check log file for details about skipped records

---

## 📈 Performance Tips

### Optimization Recommendations:

1. **Use SSD storage** for better I/O performance
2. **Ensure sufficient RAM** (2GB+ recommended)
3. **Close other applications** during processing
4. **Use virtual environment** to avoid package conflicts
5. **Monitor log files** for performance insights

### Expected Performance:

- **Small files** (< 1MB): ~1000 records/second
- **Medium files** (1-10MB): ~500 records/second  
- **Large files** (> 10MB): ~200 records/second

---

## 📞 Support

Need help or have questions?

* 📧 **Email**: palagina00@gmail.com
* 🐛 **Report Bug**: [GitHub Issues](https://github.com/palagina00/ms-access-data-processor/issues)
* 📖 **Documentation**: [INSTALLATION.md](INSTALLATION.md)

---

**Happy processing!** 🎉

For more examples and advanced usage, check the source code in `src/access_processor.py`
