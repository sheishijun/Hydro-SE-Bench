"""
Common utility functions for example code
"""

from pathlib import Path
import sys


def setup_package_path() -> Path:
    """
    Setup package path and return project root directory.
    
    Returns:
        Project root directory path
    """
    project_root = Path(__file__).resolve().parent.parent
    package_dir = project_root / "hydrosebench-eval"
    
    if package_dir.exists() and str(package_dir) not in sys.path:
        sys.path.insert(0, str(package_dir))
    
    return project_root


def get_output_dir(project_root: Path, example_name: str) -> Path:
    """
    Get output directory for an example.
    
    Args:
        project_root: Project root directory
        example_name: Example name (e.g., "example_1_basic_evaluation")
    
    Returns:
        Output directory path
    """
    output_dir = project_root / "examples" / "output" / example_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_test_data_path(project_root: Path) -> Path:
    """
    Get test data file path.
    Prioritizes CSV file, returns Excel file if CSV doesn't exist.
    
    Args:
        project_root: Project root directory
    
    Returns:
        Test data file path (CSV or Excel)
    """
    csv_path = project_root / "examples" / "test.csv"
    if csv_path.exists():
        return csv_path
    return project_root / "examples" / "test.xlsx"


def get_benchmark_data_path(project_root: Path) -> Path:
    """
    Get built-in benchmark data file path.
    Prioritizes CSV file, returns Excel file if CSV doesn't exist.
    
    Args:
        project_root: Project root directory
    
    Returns:
        Benchmark data file path (CSV or Excel)
    """
    csv_path = project_root / "hydrosebench-eval" / "hydrosebench" / "data" / "hydrosebench.csv"
    if csv_path.exists():
        return csv_path
    return project_root / "hydrosebench-eval" / "hydrosebench" / "data" / "hydrosebench.xlsx"


def filter_empty_answers(predictions):
    """
    Filter out predictions with empty answers.
    Only keep predictions that have non-empty answer values.
    
    Args:
        predictions: Predictions dict {id: answer} or list of answers
    
    Returns:
        Filtered predictions (same format as input)
    """
    if isinstance(predictions, dict):
        # Filter dictionary: remove entries where answer is empty/None
        return {k: v for k, v in predictions.items() 
                if v is not None and str(v).strip() != ''}
    elif isinstance(predictions, list):
        # Filter list: remove None and empty string values
        return [v for v in predictions 
                if v is not None and str(v).strip() != '']
    else:
        return predictions


def filter_empty_answers_from_file(input_path: Path, output_path: Path = None, model_columns: list[str] = None):
    """
    Filter out rows where all model answer columns are empty from CSV/Excel file.
    Only keep rows that have at least one non-empty answer value.
    
    Args:
        input_path: Input CSV or Excel file path
        output_path: Output file path (if None, overwrites input file)
        model_columns: List of model column names to check. If None, auto-detect.
    
    Returns:
        Path to filtered file and number of rows filtered
    """
    import pandas as pd
    from hydrosebench.excel_loader import _read_csv_safe, _detect_file_format
    from hydrosebench.batch_evaluate import identify_model_columns
    
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path
    else:
        output_path = Path(output_path)
    
    # Read file
    file_ext = input_path.suffix.lower()
    actual_format = _detect_file_format(input_path)
    
    if file_ext == ".csv" and actual_format == 'excel':
        df = pd.read_excel(input_path, engine='openpyxl')
    elif file_ext == ".csv":
        df = _read_csv_safe(input_path)
    elif file_ext in (".xlsx", ".xls"):
        df = pd.read_excel(input_path, engine='openpyxl' if file_ext == ".xlsx" else 'xlrd')
    else:
        if actual_format == 'excel':
            df = pd.read_excel(input_path, engine='openpyxl')
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    original_count = len(df)
    
    # Identify model columns if not provided
    if model_columns is None:
        model_columns = identify_model_columns(df, verbose=False)
    
    # Also check Answer column if it exists
    answer_columns = ['Answer'] if 'Answer' in df.columns else []
    all_answer_columns = answer_columns + model_columns
    
    if not all_answer_columns:
        # No answer columns found, return original file
        return input_path, 0
    
    # Filter rows: keep only rows where at least one answer column has a non-empty value
    def has_any_answer(row):
        for col in all_answer_columns:
            val = row.get(col)
            if val is not None and str(val).strip() != '':
                return True
        return False
    
    df_filtered = df[df.apply(has_any_answer, axis=1)].copy()
    filtered_count = original_count - len(df_filtered)
    
    # Save filtered file
    if file_ext == ".csv":
        df_filtered.to_csv(output_path, index=False, encoding='utf-8')
    else:
        df_filtered.to_excel(output_path, index=False, engine='openpyxl')
    
    return output_path, filtered_count