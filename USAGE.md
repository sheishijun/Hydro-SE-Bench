# Usage Guide

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [FAQ](#faq)

## Installation

### Method 1: Using requirements.txt (Recommended)

```bash
cd hydrobench-package
pip install -r requirements.txt
cd hydrobench-eval
pip install -e .
```

### Method 2: Manual Installation

```bash
pip install pandas>=2.0 openpyxl>=3.0
cd hydrobench-eval
pip install -e .
```

## Basic Usage

### 1. Single Model Evaluation

```python
from hydrobench import load_builtin_benchmark, load_predictions_from_excel

# Load benchmark
benchmark = load_builtin_benchmark("hydrobench")

# Load predictions
predictions = load_predictions_from_excel(
    "model_output.xlsx",
    id_col="ID",
    answer_col="Model Answer"
)

# Calculate scores
report = benchmark.score(predictions)
print(report.summary())
```

### 2. Batch Evaluation

```python
from hydrobench import evaluate_all_models, create_summary_excel
from pathlib import Path

# Batch evaluation
summary = evaluate_all_models(
    "test.xlsx",
    benchmark_name="hydrobench",
    output_dir="./results"
)

# Generate summary report
from hydrobench import load_builtin_benchmark
benchmark = load_builtin_benchmark("hydrobench")
create_summary_excel(summary, Path("./results"), benchmark)
```

### 3. Sampling Functionality

```python
from hydrobench import load_builtin_benchmark, sample_benchmark_by_category

# Load benchmark
benchmark = load_builtin_benchmark("hydrobench")

# Sampling (auto-save, format automatically selected based on input)
sampled = sample_benchmark_by_category(
    benchmark,
    per_category=5,
    output_path="sampled.json"  # Auto-saved as JSON
)
```

## Advanced Features

### Custom Benchmark

```python
from hydrobench import load_benchmark_from_file

# Load custom benchmark from Excel
benchmark = load_benchmark_from_file(
    "custom_benchmark.xlsx",
    level_col="Level",  # Difficulty column
    type_col="Type"     # Question type column
)
```

### Automatic Format Matching

The sampling functionality automatically selects output format based on input format:

- **JSON input** → JSON output (maintains original JSON format)
- **Excel input** → Excel output

```python
# Load from JSON, output JSON
benchmark = load_builtin_benchmark("hydrobench")
sampled = sample_benchmark_by_category(
    benchmark,
    per_category=5,
    output_path="sampled.json"  # Output JSON
)

# Load from Excel, output Excel
excel_benchmark = load_benchmark_from_file("benchmark.xlsx")
sampled = sample_benchmark_by_category(
    excel_benchmark,
    per_category=5,
    output_path="sampled.xlsx"  # Output Excel
)
```

## FAQ

### Q: How to modify output format?

A: The sampling functionality auto-detects, but you can also specify manually:

```python
from hydrobench import save_benchmark

save_benchmark(benchmark, "output.xlsx", format="excel")
save_benchmark(benchmark, "output.json", format="json")
```

### Q: No Level and Type columns in Excel report?

A: Ensure the Excel file contains `Level` and `Type` columns, and specify them when loading:

```python
benchmark = load_benchmark_from_file(
    "benchmark.xlsx",
    level_col="Level",  # Modify here if column name differs
    type_col="Type"     # Modify here if column name differs
)
```

### Q: How to view all available functions?

A: Check the package's `__init__.py` or run:

```python
from hydrobench import *
help(load_builtin_benchmark)  # View function help
```

## Additional Resources

- Complete API Documentation: `hydrobench-eval/README.md`
- Example Code: `examples/`
- Quick Start: `QUICKSTART.md`
