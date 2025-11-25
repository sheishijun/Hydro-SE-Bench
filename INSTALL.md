# Installation and Usage Guide

## Installation Steps

### 1. Install Python Package

Navigate to the `hydrobench-eval` directory and install:

```bash
cd hydrobench-eval
pip install -e .
```

Or install directly (without entering the directory):

```bash
pip install -e hydrobench-eval
```

### 2. Verify Installation

Run the following command to verify the installation was successful:

```python
python -c "from hydrobench import load_builtin_benchmark; print('Installation successful!')"
```

## Download Dataset Files

Dataset files are located in the `hydrobench-eval/hydrobench/data/` directory, available in the following formats:

- **hydrobench.json**: Complete dataset in JSON format
- **hydrobench.csv**: Dataset in CSV format (lighter weight, suitable for version control)

### Method 1: Download Using Python API

If the `hydrobench` Python package is installed, you can download using the following code:

```python
from hydrobench import download_hydrobench_data
from pathlib import Path

# Download JSON file to current directory
json_path = download_hydrobench_data("json")
print(f"JSON file downloaded to: {json_path}")

# Download CSV file to specified directory
csv_path = download_hydrobench_data("csv", Path("./data/hydrobench.csv"))
print(f"CSV file downloaded to: {csv_path}")

# Download Excel file (if available in package)
xlsx_path = download_hydrobench_data("xlsx", Path("./data/hydrobench.xlsx"))
```

### Method 2: Download Using Command Line

```bash
# Download all formats to current directory
python -m hydrobench download

# Download only JSON file
python -m hydrobench download --format json

# Download only CSV file (recommended, lighter weight)
python -m hydrobench download --format csv

# Download to specified directory
python -m hydrobench download --output ./data

# Download specified format to specified path
python -m hydrobench download --format csv --output ./my_data/hydrobench.csv
```

### Method 3: Direct File Access

Dataset files can also be accessed directly from the `hydrobench-eval/hydrobench/data/` directory without downloading.

### Run Download Example

You can run the example code to see how the download feature works:

```bash
cd examples
python example_0_download_data.py
```

## Running Examples

### Method 1: Run Example Files Directly

```bash
cd examples
python example_1_basic_evaluation.py
```

### Method 2: Run as Module

```bash
python -m examples.example_1_basic_evaluation
```

## Dependency Installation

If you encounter import errors, install the following dependencies:

```bash
pip install pandas>=2.0 openpyxl>=3.0
```

## Common Issues

### Issue 1: Cannot find hydrobench module

**Solution**: Ensure the package is installed, or check Python path settings.

### Issue 2: Cannot find data files

**Solution**: Data files are located in the `hydrobench-eval/hydrobench/data/` directory. Ensure this directory exists.

### Issue 3: Excel file read error

**Solution**: Ensure the `openpyxl` library is installed:
```bash
pip install openpyxl
```

## Next Steps

- Check `examples/README.md` for all examples
- Check `hydrobench-eval/README.md` for complete API documentation
