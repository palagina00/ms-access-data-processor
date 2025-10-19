# 📦 Installation Guide for MS Access Data Processor

Detailed step-by-step installation and setup instructions for the project on different operating systems.

---

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Python Installation](#python-installation)
- [Project Installation](#project-installation)
- [MS Access Driver Installation](#ms-access-driver-installation)
- [Installation Verification](#installation-verification)
- [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements:

- **Python**: 3.6.8 or higher (recommended 3.8+)
- **RAM**: 512 MB (recommended 2 GB)
- **Disk Space**: 100 MB
- **OS**: Windows 7+, Ubuntu 18.04+, macOS 10.14+

### Additional (Optional):

- **MS Access Driver** - for working with real .mdb files
- **Git** - for cloning repository

---

## 🐍 Python Installation

### Windows:

#### Method 1: Official Installer (Recommended)

1. **Download Python**:
   - Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Download Python 3.8+ (latest stable version)
   - Choose "Windows installer (64-bit)"

2. **Install Python**:
   - Run the downloaded installer
   - **IMPORTANT**: Check "Add Python to PATH" checkbox
   - Choose "Install Now" or "Customize installation"
   - Complete the installation

3. **Verify Installation**:
   ```cmd
   python --version
   pip --version
   ```

#### Method 2: Microsoft Store

1. Open Microsoft Store
2. Search for "Python 3.11" (or latest version)
3. Click "Install"

### Linux (Ubuntu/Debian):

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

### macOS:

#### Method 1: Official Installer

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download macOS installer
3. Run the installer

#### Method 2: Homebrew

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Verify installation
python3 --version
pip3 --version
```

---

## 📁 Project Installation

### 1. Download Project

#### Option A: Clone from GitHub (Recommended)

```bash
# Clone repository
git clone https://github.com/palagina00/ms-access-data-processor.git
cd ms-access-data-processor
```

#### Option B: Download ZIP

1. Go to [https://github.com/palagina00/ms-access-data-processor](https://github.com/palagina00/ms-access-data-processor)
2. Click "Code" → "Download ZIP"
3. Extract ZIP file
4. Navigate to extracted folder

### 2. Create Virtual Environment

#### Windows:

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (you should see (venv) in prompt)
```

#### Linux/macOS:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (you should see (venv) in prompt)
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Check if all packages installed correctly
pip list

# Test basic functionality
python -c "import pandas; print('Pandas version:', pandas.__version__)"
```

---

## 🗄️ MS Access Driver Installation

**Note**: This step is optional if you're only working with CSV files.

### Windows:

1. **Download Microsoft Access Database Engine**:
   - Go to [Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=54920)
   - Download "Microsoft Access Database Engine 2016 Redistributable"
   - Choose appropriate version (32-bit or 64-bit)

2. **Install Driver**:
   - Run downloaded installer
   - Follow installation wizard
   - Restart computer if prompted

### Linux:

```bash
# Install unixodbc and Microsoft ODBC drivers
sudo apt update
sudo apt install unixodbc unixodbc-dev

# Install Microsoft ODBC Driver for SQL Server
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt update
sudo apt install msodbcsql17
```

### macOS:

```bash
# Install using Homebrew
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql17 mssql-tools
```

---

## ✅ Installation Verification

### 1. Test Python Environment

```bash
# Check Python version (should be 3.6.8+)
python --version

# Check installed packages
pip list | grep -E "(pandas|openpyxl)"
```

### 2. Test Project Files

```bash
# Check if main script exists
ls src/access_processor.py

# Check if test data generator exists
ls tests/generate_test_data.py
```

### 3. Run Test

```bash
# Generate test data
python tests/generate_test_data.py

# Run main processor
python src/access_processor.py

# Check output
ls data/output/
cat data/output/result.csv
```

### 4. Expected Output

You should see:
- Test data files in `data/input/`
- Processed results in `data/output/result.csv`
- Log file `processor.log` with processing details

---

## 🔧 Troubleshooting

### Common Issues:

#### Issue 1: "python is not recognized"

**Solution**:
- Make sure Python is added to PATH
- Try using `python3` instead of `python`
- Restart command prompt/terminal

#### Issue 2: "pip is not recognized"

**Solution**:
```bash
# Try pip3 instead
pip3 install -r requirements.txt

# Or use python -m pip
python -m pip install -r requirements.txt
```

#### Issue 3: "Permission denied" (Linux/macOS)

**Solution**:
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use sudo (not recommended)
sudo pip install -r requirements.txt
```

#### Issue 4: "No module named 'pandas'"

**Solution**:
```bash
# Make sure virtual environment is activated
# Check if you see (venv) in your prompt

# Reinstall packages
pip install -r requirements.txt
```

#### Issue 5: MS Access Driver Issues

**Solution**:
- Make sure you have correct driver version (32-bit vs 64-bit)
- Check if driver is properly installed
- For CSV-only usage, driver is not required

### Getting Help:

1. **Check Log Files**: Look at `processor.log` for detailed error messages
2. **Verify File Paths**: Make sure all file paths are correct
3. **Check Permissions**: Ensure you have read/write access to data directories
4. **Python Version**: Ensure you're using Python 3.6.8 or higher

---

## 📞 Support

If you encounter issues not covered in this guide:

* 📧 **Email**: palagina00@gmail.com
* 🐛 **Report Bug**: [GitHub Issues](https://github.com/palagina00/ms-access-data-processor/issues)
* 📖 **Documentation**: [USAGE.md](USAGE.md)

---

**Installation completed successfully!** 🎉

Next step: [USAGE.md](USAGE.md) - Learn how to use the project
