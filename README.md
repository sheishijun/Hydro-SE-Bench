# HydroBench Dataset

HydroBench is a professional evaluation dataset specifically designed for the water conservancy and hydropower field, aimed at comprehensively assessing models' capabilities in water engineering expertise, engineering applications, and reasoning calculations.

## 📊 Dataset Overview

The HydroBench dataset contains **4,000** questions covering nine core professional directions in water conservancy and hydropower. All questions are in Chinese, making it suitable for evaluating Chinese language models' professional capabilities in the water engineering domain.

### Overall Statistics

- **Total Questions**: 4,000
- **Single-Choice Questions**: 2,696 (67.4%)
- **Multiple-Choice Questions**: 1,304 (32.6%)

### Difficulty Distribution

The dataset is divided into three difficulty levels, balancing fundamental knowledge and advanced reasoning capabilities:

- **Basic Conceptual Knowledge**: 1,651 questions (41.3%)
- **Engineering Applications**: 1,651 questions (41.3%)
- **Reasoning and Calculation**: 698 questions (17.4%)

> Note: The total number of questions across all difficulty levels is 4,000. The percentages above are rounded approximations.

### Category Distribution

The dataset covers the following nine professional directions, each containing a different number of questions:

| Category Code | Category Name | Total | Single-Choice | Multiple-Choice | Basic Conceptual Knowledge | Engineering Applications | Reasoning and Calculation |
|---------------|---------------|-------|---------------|-----------------|---------------------------|--------------------------|---------------------------|
| **BK** | Background Knowledge | 250 | 217 | 33 | 250 | 0 | 0 |
| **IS** | Industry Standard | 250 | 160 | 90 | 0 | 250 | 0 |
| **HWR** | Hydrology and Water Resources | 500 | 311 | 189 | 200 | 200 | 100 |
| **GE** | Geotechnical Engineering | 500 | 297 | 203 | 200 | 200 | 100 |
| **HSE** | Hydraulic Structures and Equipment | 500 | 336 | 164 | 200 | 200 | 100 |
| **ESM** | Engineering Safety and Management | 500 | 318 | 182 | 200 | 200 | 100 |
| **HRD** | Hydraulics and River Dynamic | 500 | 358 | 142 | 200 | 200 | 100 |
| **M** | Meteorology | 500 | 336 | 164 | 200 | 200 | 100 |
| **PS** | Power System | 500 | 363 | 137 | 200 | 200 | 100 |

> Note: Detailed statistics can be obtained by running the `final_stats.py` or `calc_and_save.py` scripts. After running the script, copy the output results into the table above.

## ✨ Dataset Features

1. **Comprehensive Coverage**: Covers core knowledge domains in water conservancy and hydropower engineering, from basic concepts to engineering practice
2. **Difficulty Levels**: Balances fundamental knowledge and advanced reasoning to comprehensively assess model capabilities
3. **Diverse Question Types**: Includes both single-choice and multiple-choice questions, closer to real-world application scenarios
4. **Chinese Context**: All questions are in Chinese, optimized for Chinese language models and water engineering domain knowledge
5. **Professional Quality**: Questions are reviewed by water engineering experts through multiple rounds, ensuring professionalism and accuracy

## 📥 Getting the Dataset

Dataset files are located in the `hydrobench-eval/hydrobench/data/` directory, available in the following formats:

- **hydrobench.json**: Complete dataset in JSON format
- **hydrobench.csv**: Dataset in CSV format (lighter weight, suitable for version control)

For detailed download and installation instructions, see: 📖 **[Installation Guide](INSTALL.md#download-dataset-files)**

## 🔧 Using the Evaluation Tools

We provide a dedicated Python package for evaluating model performance on the HydroBench dataset. The evaluation tools support:

- ✅ Batch evaluation of multiple models
- ✅ Automatic generation of detailed evaluation reports (Excel, JSON, Markdown)
- ✅ Statistical analysis by category, difficulty, and question type
- ✅ Support for custom benchmarks
- ✅ Flexible answer format support

### Quick Start with Evaluation Tools

For detailed installation and usage instructions, see:

- 📖 **[Complete Evaluation Tool Documentation](hydrobench-eval/README.md)** - Complete API documentation, usage examples, and command-line tool instructions
- 🔧 **[Installation Instructions](hydrobench-eval/README.md#安装)** - Package installation steps
- 🚀 **[Quick Start](hydrobench-eval/README.md#快速开始)** - Quick start example code

## 📁 Project Structure

```
hydrobench-package/
├── hydrobench-eval/          # HydroBench evaluation toolkit
│   ├── hydrobench/           # Core modules
│   │   └── data/             # Built-in dataset
│   │       ├── hydrobench.json
│   │       └── hydrobench.csv
│   └── README.md             # Complete evaluation tool documentation
├── examples/                  # Usage example code
│   ├── example_0_download_data.py
│   ├── example_1_basic_evaluation.py
│   └── ...
└── README.md                 # This file (dataset introduction)
```

## 📚 Additional Resources

- **Evaluation Tool Documentation**: [hydrobench-eval/README.md](hydrobench-eval/README.md) - Complete API documentation and usage guide for evaluation tools
- **Example Code**: [examples/](examples/) - Detailed usage examples and code demonstrations
- **Example Documentation**: [examples/README.md](examples/README.md) - Detailed explanation of all examples

## 📄 Data Format

The dataset uses standard JSON and CSV formats, containing the following fields:

- **ID**: Unique question identifier (e.g., "BK-1", "HWR-1")
- **Question**: Question content (including options)
- **Answer**: Correct answer (e.g., "C" or "A,B")
- **Category**: Category code (BK, IS, HWR, GE, HSE, ESM, HRD, M, PS)
- **Level**: Difficulty level (Basic Conceptual Knowledge, Engineering Applications, Reasoning and Calculation)
- **Type**: Question type (Single-choice, Multiple-choice)

For detailed format specifications, see [Evaluation Tool Documentation](hydrobench-eval/README.md#文件格式要求).

## 🤝 Contributing

Contributions and improvements are welcome! If you have questions or suggestions, please submit an Issue or Pull Request.

## 📝 License

[Add license information here]

---

**HydroBench** - Professional Evaluation Dataset for Water Conservancy and Hydropower Domain
