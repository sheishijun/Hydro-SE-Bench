# HydroBench 评估库示例

本目录包含了使用 HydroBench 评估库的完整示例，展示了库的各种功能。

## 示例列表

### 示例 0: 下载 HydroBench 数据文件 (`example_0_download_data.py`)
展示如何使用 HydroBench 库下载内置的 hydrobench.json 和 hydrobench.xlsx 文件。

**主要功能：**
- 使用 Python API 下载数据文件
- 下载 JSON 和 Excel 格式的数据文件
- 下载到当前目录或指定路径
- 使用命令行工具下载数据文件
- 验证下载的文件

**运行方式：**
```bash
python examples/example_0_download_data.py
```

**代码示例：**

使用 Python API 下载：
```python
from hydrobench import download_hydrobench_data
from pathlib import Path

# 下载 JSON 文件到当前目录
json_path = download_hydrobench_data("json")

# 下载 Excel 文件到当前目录
xlsx_path = download_hydrobench_data("xlsx")

# 下载到指定路径
download_hydrobench_data("json", Path("./data/hydrobench.json"))
download_hydrobench_data("xlsx", Path("./data/hydrobench.xlsx"))
```

使用命令行工具下载：
```bash
# 下载 JSON 和 Excel 文件到当前目录
python -m hydrobench download

# 只下载 JSON 文件
python -m hydrobench download --format json

# 只下载 Excel 文件
python -m hydrobench download --format xlsx

# 下载到指定目录
python -m hydrobench download --output ./my_data

# 下载到指定文件路径
python -m hydrobench download --format json --output ./my_data/hydrobench.json
```

### 示例 1: 基础评估功能 (`example_1_basic_evaluation.py`)
展示如何使用 HydroBench 库进行单个模型的评估。

**主要功能：**
- 加载内置测评集
- 从 Excel 文件加载模型预测结果
- 计算得分并生成报告

**运行方式：**
```bash
python examples/example_1_basic_evaluation.py
```

### 示例 2: 批量评估多个模型 (`example_2_batch_evaluation.py`)
展示如何批量评估 Excel 文件中的多个模型。

**主要功能：**
- 自动识别 Excel 文件中的所有模型列
- 批量评估所有模型
- 生成每个模型的详细报告
- 生成模型对比汇总 Excel

**运行方式：**
```bash
python examples/example_2_batch_evaluation.py
```

### 示例 3: 使用自定义测评集 (`example_3_custom_benchmark.py`)
展示如何从 Excel 文件加载自定义测评集并进行评估。

**主要功能：**
- 从 Excel 文件加载自定义测评集
- 使用自定义测评集进行评估
- 显示按类别和难度的统计

**运行方式：**
```bash
python examples/example_3_custom_benchmark.py
```

### 示例 4: 采样功能 (`example_4_sampling.py`)
展示如何从测评集中按类别采样题目。

**主要功能：**
- 按类别采样题目
- 创建采样后的测评集
- 保存采样结果

**运行方式：**
```bash
python examples/example_4_sampling.py
```

### 示例 5: 完整工作流程 (`example_5_complete_workflow.py`)
展示从加载数据到生成完整报告的完整工作流程。

**主要功能：**
- 预览 Excel 文件结构
- 识别模型列
- 批量评估
- 生成汇总报告
- 结果分析

**运行方式：**
```bash
python examples/example_5_complete_workflow.py
```

## 依赖要求

运行这些示例需要安装以下依赖：

```bash
pip install pandas openpyxl
```

如果只需要基础功能（不使用 Excel 报告），可以不安装这些依赖。

## 数据文件要求

大部分示例需要以下数据文件：

1. **测评集文件**: `hydrobench-eval/hydrobench/data/hydrobench.xlsx`
   - 包含题目、选项、正确答案等信息   - 可选列：Level（难度）、Type（题型）

2. **模型预测文件**: `examples/test.xlsx`
   - 包含模型预测结果
   - 需要包含 ID 列用于匹配
   - 每个模型一列，列名为模型名称

## 输出文件说明

运行示例后，会在 `output/` 或 `test/output/` 目录下生成以下文件：

1. **单个模型报告** (`<模型名>/score_report.xlsx` 和 `<模型名>/score_report.json`)
   - 每个模型有独立的文件夹，包含 JSON 和 Excel 两种格式的报告
   - 包含题目内容、正确答案、模型答案的详细对比
   - 包含按类别和难度的统计表

2. **模型对比汇总** (`models_comparison.xlsx`)
   - 所有模型的得分对比
   - 按类别、难度和题型的模型间对比

3. **汇总数据** (`all_models_summary.json`)
   - 完整的评估数据，包含按类别和难度的统计
   - JSON 格式，便于程序处理

## 注意事项

1. 运行示例前，请确保数据文件路径正确
2. 如果数据文件不存在，示例会提示错误信息
3. 某些示例需要修改列名（如 "GPT-4"）以匹配实际数据
4. 确保有足够的磁盘空间保存输出文件

## 更多信息

有关 HydroBench 评估库的更多信息，请参考主 README 文件。

