from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from .benchmark import Benchmark, Example


def _detect_file_format(file_path: Path) -> str:
    """
    检测文件的实际格式（通过读取文件头）。
    
    Args:
        file_path: 文件路径
    
    Returns:
        'excel' 如果是 Excel 格式（.xlsx, .xls），'csv' 如果是 CSV 格式，'unknown' 如果无法确定
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)  # 读取前8个字节
            # Excel 文件（.xlsx）以 ZIP 魔数开头：PK\x03\x04
            if header[:2] == b'PK':
                return 'excel'
            # Excel 97-2003 (.xls) 以 OLE2 格式开头
            if header[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1':
                return 'excel'
            # CSV 文件通常是文本格式，检查是否包含可打印字符
            try:
                header.decode('utf-8', errors='strict')
                return 'csv'
            except UnicodeDecodeError:
                try:
                    header.decode('gbk', errors='strict')
                    return 'csv'
                except UnicodeDecodeError:
                    return 'unknown'
    except Exception:
        return 'unknown'


def _read_csv_safe(csv_path: Path) -> pd.DataFrame:
    """
    安全地读取 CSV 文件，尝试多种编码和参数组合。
    
    Args:
        csv_path: CSV 文件路径
    
    Returns:
        DataFrame 对象
    
    Raises:
        ValueError: 如果所有尝试都失败
    """
    # 检查 pandas 版本以兼容不同的参数
    pandas_version = tuple(map(int, pd.__version__.split('.')[:2]))
    use_on_bad_lines = pandas_version >= (1, 3)  # pandas >= 1.3.0 支持 on_bad_lines
    
    encodings = ["utf-8", "utf-8-sig", "gbk", "gb18030", "latin-1"]
    last_error = None
    
    for encoding in encodings:
        try:
            # 尝试使用 Python 引擎，更宽松的解析
            read_csv_kwargs = {
                'filepath_or_buffer': csv_path,
                'encoding': encoding,
                'engine': 'python',
                'sep': ',',  # 明确指定分隔符
                'quotechar': '"',  # 明确指定引号字符
            }
            if use_on_bad_lines:
                read_csv_kwargs['on_bad_lines'] = 'skip'
            else:
                read_csv_kwargs['error_bad_lines'] = False
                read_csv_kwargs['warn_bad_lines'] = False
            df = pd.read_csv(**read_csv_kwargs)
            return df
        except (UnicodeDecodeError, pd.errors.ParserError, TypeError) as e:
            last_error = e
            continue
    
    # 如果所有编码都失败，尝试最基本的读取方式（跳过错误行）
    try:
        read_csv_kwargs = {
            'filepath_or_buffer': csv_path,
            'encoding': "utf-8",
            'engine': 'python',
            'sep': None,  # 自动检测分隔符
        }
        if use_on_bad_lines:
            read_csv_kwargs['on_bad_lines'] = 'skip'
        else:
            read_csv_kwargs['error_bad_lines'] = False
            read_csv_kwargs['warn_bad_lines'] = False
        df = pd.read_csv(**read_csv_kwargs)
        return df
    except Exception as e:
        # 检查是否是 Excel 格式的文件被误当作 CSV
        actual_format = _detect_file_format(csv_path)
        if actual_format == 'excel':
            raise ValueError(
                f"无法读取 CSV 文件 {csv_path}。"
                f"检测到文件实际上是 Excel 格式（.xlsx 或 .xls），但扩展名是 .csv。"
                f"请将文件重命名为 .xlsx 或 .xls，或使用 load_benchmark_from_file 函数（它会自动检测格式）。"
            ) from (last_error or e)
        raise ValueError(
            f"无法读取 CSV 文件 {csv_path}。"
            f"请检查文件格式是否正确（确保使用逗号分隔，字段中的换行符用引号包裹）。"
            f"错误: {last_error or e}"
        ) from (last_error or e)


def load_benchmark_from_file(
    file_path: str | Path,
    *,
    answer_col: str = "Answer",
    question_col: str = "Question",
    id_col: str | None = "ID",
    category_col: str | None = "ID",
    level_col: str | None = "Level",
    type_col: str | None = "Type",
    sheet_name: str | int | None = 0,
) -> Benchmark:
    """
    从文件加载 benchmark（支持 CSV、Excel 格式）。
    
    支持的文件格式：.xlsx, .xls, .csv
    函数会自动检测文件格式，即使扩展名不匹配也能正确读取。

    Args:
        file_path: 文件路径（支持 CSV、XLSX、XLS 格式）
        answer_col: 标准答案列名，默认为 "Answer"
        question_col: 题目内容列名，默认为 "Question"
        id_col: 题目ID列名，如果为 None 则自动生成
        category_col: 类别列名（如 "ID"），用于提取类别前缀（如 BK-001 -> BK）
        level_col: 难度等级列名，默认为 "Level"
        type_col: 题型列名，默认为 "Type"
        sheet_name: 工作表名称或索引（仅 Excel 文件），默认为第一个工作表

    Returns:
        Benchmark 对象

    Example:
        >>> benchmark = load_benchmark_from_file("hydrobench.xlsx")
        >>> benchmark = load_benchmark_from_file("hydrobench.csv")
        >>> benchmark = load_benchmark_from_file("hydrobench.xls")
        >>> report = benchmark.score(predictions)
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    # 根据文件扩展名和实际格式选择读取方式
    file_ext = file_path.suffix.lower()
    actual_format = _detect_file_format(file_path)
    
    # 如果扩展名是 .csv 但实际是 Excel 格式，使用 Excel 读取方式
    if file_ext == ".csv" and actual_format == 'excel':
        print(f"⚠ 警告: 文件扩展名是 .csv，但检测到实际格式是 Excel。将使用 Excel 读取方式。")
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    elif file_ext == ".csv":
        df = _read_csv_safe(file_path)
    elif file_ext in (".xlsx", ".xls"):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        # 如果扩展名不支持，但检测到是 Excel 格式，尝试使用 Excel 读取
        if actual_format == 'excel':
            print(f"⚠ 警告: 文件扩展名是 {file_ext}，但检测到实际格式是 Excel。将尝试使用 Excel 读取方式。")
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: .csv, .xlsx, .xls")

    if answer_col not in df.columns:
        raise ValueError(
            f"Column '{answer_col}' not found in file. Available columns: {list(df.columns)}"
        )

    if question_col not in df.columns:
        raise ValueError(
            f"Column '{question_col}' not found in file. Available columns: {list(df.columns)}"
        )

    examples: list[Example] = []
    for idx, row in df.iterrows():
        answer_val = row.get(answer_col)
        if pd.isna(answer_val):
            continue

        answer_str = str(answer_val).strip()
        if not answer_str:
            continue

        question_text = str(row.get(question_col, "")).strip()

        # 解析选项字母（从题目文本中提取 A/B/C/D 等）
        option_letters = set(
            re.findall(r"([A-Z])\s*[\.．、：:）\)]", question_text)
        )
        if not option_letters:
            # 如果题目中没有找到选项，从答案中提取可能的选项
            option_letters = set(ch for ch in answer_str if ch.isalpha() and ch.isupper())

        option_labels = sorted(option_letters) if option_letters else []

        # 解析正确答案（从 Answer 列提取）
        correct_letters: set[str] = set()
        for ch in answer_str:
            if ch.strip() and ch.isalpha() and ch.isupper():
                correct_letters.add(ch)
            elif ch in {",", "，", ";", "；", "/", "、", "+", "|"}:
                continue

        # 如果没有找到选项标签，使用正确答案中的字母
        if not option_labels and correct_letters:
            option_labels = sorted(correct_letters)

        # 构建 metadata
        metadata: dict[str, Any] = {}

        if category_col and category_col in df.columns:
            category_val = row.get(category_col)
            if not pd.isna(category_val):
                category_str = str(category_val)
                match = re.search(r"[A-Za-z]+", category_str)
                if match:
                    metadata["category"] = match.group(0)

        if level_col and level_col in df.columns:
            level_val = row.get(level_col)
            if not pd.isna(level_val):
                level_str = str(level_val).strip()
                # 映射常见的中文/英文等级
                level_map = {
                    "A": "basic conceptual knowledge",
                    "B": "engineering applications",
                    "C": "reasoning and calculation",
                }
                metadata["level"] = level_map.get(level_str.upper(), level_str)

        if type_col and type_col in df.columns:
            type_val = row.get(type_col)
            if not pd.isna(type_val):
                type_str = str(type_val).strip()
                type_map = {
                    "单选题": "single choice",
                    "多选题": "multiple choice",
                    "single choice": "single choice",
                    "multiple choice": "multiple choice",
                    "single-choice": "single choice",
                    "multiple-choice": "multiple choice",
                }
                metadata["type"] = type_map.get(type_str, type_map.get(type_str.lower(), type_str))

        # 生成题目ID
        if id_col and id_col in df.columns:
            example_id = str(row.get(id_col, "")).strip()
            if not example_id or pd.isna(row.get(id_col)):
                example_id = f"{file_path.stem}-{idx+1:04d}"
        else:
            example_id = f"{file_path.stem}-{idx+1:04d}"

        examples.append(
            Example(
                id=example_id,
                input_text=question_text,
                correct_options=tuple(sorted(correct_letters)),
                metadata=metadata,
            )
        )

    if not examples:
        raise ValueError(f"No valid examples found in file: {file_path}")

    file_type = "CSV" if file_ext == ".csv" else "Excel"
    return Benchmark(
        name=file_path.stem,
        description=f"Loaded from {file_type}: {file_path.name}",
        examples=examples,
        source_path=file_path,
    )


def load_predictions_from_excel(
    excel_path: str | Path,
    *,
    answer_col: str = "Answer",
    id_col: str | None = "ID",
    sheet_name: str | int | None = 0,
) -> dict[str, Any] | list[Any]:
    """
    从 Excel 或 CSV 文件加载模型预测结果。
    
    支持的文件格式：.xlsx, .xls, .csv

    支持两种模式：
    1. 如果提供了 id_col，返回字典 {question_id: answer}
    2. 否则返回列表，按行顺序排列

    Args:
        excel_path: Excel 或 CSV 文件路径
        answer_col: 预测答案列名，默认为 "Answer"
        id_col: 题目ID列名。如果提供，返回字典格式；否则返回列表格式
        sheet_name: 工作表名称或索引（仅 Excel 文件），默认为第一个工作表

    Returns:
        预测结果，格式为字典或列表

    Example:
        >>> # 使用 ID 列，返回字典
        >>> predictions = load_predictions_from_excel("model_output.xlsx", id_col="ID")
        >>> predictions = load_predictions_from_excel("model_output.csv", id_col="ID")
    >>> # 不使用 ID 列，返回列表（按行顺序）
    >>> predictions = load_predictions_from_excel("model_output.xlsx", id_col=None)
    """
    excel_path = Path(excel_path)
    if not excel_path.is_file():
        raise FileNotFoundError(f"File not found: {excel_path}")

    # 根据文件扩展名和实际格式选择读取方式
    file_ext = excel_path.suffix.lower()
    actual_format = _detect_file_format(excel_path)
    
    # 如果扩展名是 .csv 但实际是 Excel 格式，使用 Excel 读取方式
    if file_ext == ".csv" and actual_format == 'excel':
        print(f"⚠ 警告: 文件扩展名是 .csv，但检测到实际格式是 Excel。将使用 Excel 读取方式。")
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    elif file_ext == ".csv":
        df = _read_csv_safe(excel_path)
    elif file_ext in (".xlsx", ".xls"):
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    else:
        # 如果扩展名不支持，但检测到是 Excel 格式，尝试使用 Excel 读取
        if actual_format == 'excel':
            print(f"⚠ 警告: 文件扩展名是 {file_ext}，但检测到实际格式是 Excel。将尝试使用 Excel 读取方式。")
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: .csv, .xlsx, .xls")

    if answer_col not in df.columns:
        raise ValueError(
            f"Column '{answer_col}' not found in file. Available columns: {list(df.columns)}"
        )

    if id_col and id_col not in df.columns:
        raise ValueError(
            f"Column '{id_col}' not found in file. Available columns: {list(df.columns)}"
        )

    if id_col:
        # 返回字典格式 {id: answer}
        result: dict[str, Any] = {}
        for _, row in df.iterrows():
            answer_val = row.get(answer_col)
            if pd.isna(answer_val):
                continue
            question_id_raw = row.get(id_col)
            if pd.isna(question_id_raw):
                continue
            question_id = str(question_id_raw).strip()
            if not question_id:
                continue
            result[question_id] = answer_val
        return result
    else:
        # 返回列表格式（按行顺序）
        result: list[Any] = []
        for _, row in df.iterrows():
            answer_val = row.get(answer_col)
            result.append(answer_val if not pd.isna(answer_val) else None)
        return result


