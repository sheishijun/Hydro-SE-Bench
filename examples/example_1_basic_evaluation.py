"""
Example 1: Basic Evaluation Functionality
Demonstrates how to use the HydroBench library to evaluate a single model
"""

from utils import setup_package_path, get_output_dir, get_test_data_path

# Setup package path
PROJECT_ROOT = setup_package_path()

from hydrosebench import Benchmark, load_builtin_benchmark, load_predictions_from_excel


def main():
    """Basic evaluation example"""
    print("=" * 80)
    print("Example 1: Basic Evaluation Functionality")
    print("=" * 80)
    print()
    
    # 1. Load built-in benchmark
    print("Step 1: Loading benchmark...")
    benchmark = load_builtin_benchmark("hydrosebench")
    print(f"✓ Benchmark loaded, {len(benchmark.examples)} questions total")
    print()
    
    # 2. Load model predictions (from CSV or Excel file)
    print("Step 2: Loading model predictions...")
    excel_path = get_test_data_path(PROJECT_ROOT)
    
    if not excel_path.exists():
        print(f"⚠ Example file does not exist: {excel_path}")
        print("Please ensure test.csv or test.xlsx file exists, or modify excel_path to point to your data file")
        return
    
    # Assume CSV/Excel file has a column named "DeepSeek-V3.2-Exp" containing model answers
    # load_predictions_from_excel function supports both CSV and Excel formats (auto-detected)
    predictions = load_predictions_from_excel(
        excel_path,
        id_col="ID",
        answer_col="DeepSeek-V3.2-Exp"  # Please modify according to actual column name
    )
    
    # Filter out predictions with empty answers (only calculate rows with values)
    from utils import filter_empty_answers
    original_count = len(predictions) if isinstance(predictions, (dict, list)) else 0
    predictions = filter_empty_answers(predictions)
    filtered_count = len(predictions) if isinstance(predictions, (dict, list)) else 0
    
    if original_count != filtered_count:
        print(f"✓ Loaded {original_count} predictions, filtered {original_count - filtered_count} empty answers")
        print(f"✓ Using {filtered_count} predictions with non-empty answers")
    else:
        print(f"✓ Loaded {filtered_count} predictions")
    print()
    
    # 3. Calculate scores
    print("Step 3: Calculating scores...")
    report = benchmark.score(predictions)
    
    # 4. Display results
    print("\n" + "=" * 80)
    print("Evaluation Results")
    print("=" * 80)
    print(report.summary())
    print()
    
    # 5. Save reports (optional)
    output_dir = get_output_dir(PROJECT_ROOT, "example_1_basic_evaluation")
    
    # Save JSON report
    json_file = output_dir / "basic_evaluation_report.json"
    json_file.write_text(report.to_json(), encoding="utf-8")
    print(f"✓ JSON report saved: {json_file}")
    
    # Save CSV report (lightweight, recommended)
    try:
        csv_file = output_dir / "basic_evaluation_report.csv"
        report.to_csv(csv_file, benchmark=benchmark)
        print(f"✓ CSV report saved: {csv_file}")
    except ImportError:
        print("⚠ pandas not installed, skipping CSV report generation")
    
    # Save Excel report (if pandas and openpyxl are installed)
    try:
        excel_file = output_dir / "basic_evaluation_report.xlsx"
        report.to_excel(excel_file, benchmark=benchmark)
        print(f"✓ Excel report saved: {excel_file}")
    except ImportError:
        print("⚠ pandas or openpyxl not installed, skipping Excel report generation")
    
    print("\n" + "=" * 80)
    print("Example completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
