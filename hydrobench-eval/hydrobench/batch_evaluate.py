"""
批量评估多个模型的得分计算功能
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .benchmark import Benchmark
from .datasets import load_builtin_benchmark
from .excel_loader import load_predictions_from_excel, _read_csv_safe


# 标准列（非模型列）列表
STANDARD_COLUMNS = {
    "ID", "id", "Id", "ID列", "id列",
    "Question", "question", "Question列", "题目", "问题", "问题列",
    "Answer", "answer", "Answer列", "答案", "标准答案", "正确答案",
    "Level", "level", "难度", "难度等级",
    "Type", "type", "题型", "题目类型",
    "Category", "category", "类别", "分类",
    "Token", "token", "token列", "token数量", "token长度",
}


def is_standard_column(col_name: str) -> bool:
    """判断是否是标准列（非模型列）"""
    col_lower = str(col_name).lower()
    # 检查是否在标准列列表中
    if col_name in STANDARD_COLUMNS:
        return True
    # 检查是否包含 token 关键词
    if "token" in col_lower:
        return True
    return False


def identify_model_columns(df: pd.DataFrame, verbose: bool = True) -> list[str]:
    """
    从 DataFrame 中识别模型列。
    
    Args:
        df: Excel 文件读取的 DataFrame
        verbose: 是否输出详细信息
    
    Returns:
        模型列名列表
    """
    model_columns = []
    
    if verbose:
        print("=" * 80)
        print("正在识别模型列...")
        print("=" * 80)
    
    for col in df.columns:
        if is_standard_column(col):
            if verbose:
                print(f"  [标准列] {col} - 跳过")
            continue
        
        # 检查该列是否包含答案数据
        non_null_count = df[col].notna().sum()
        if non_null_count == 0:
            if verbose:
                print(f"  [空列] {col} - 跳过（无数据）")
            continue
        
        # 检查该列的数据是否像答案（包含字母 A-Z）
        sample_values = df[col].dropna().head(10).astype(str)
        has_answer_pattern = False
        for val in sample_values:
            val_str = str(val).upper().strip()
            # 检查是否包含字母（答案通常是 A, B, C, D 等）
            if any(c.isalpha() and c.isupper() for c in val_str):
                has_answer_pattern = True
                break
        
        if has_answer_pattern:
            model_columns.append(col)
            if verbose:
                print(f"  [模型列] ✓ {col} - 包含 {non_null_count} 个答案")
        else:
            if verbose:
                print(f"  [其他列] {col} - 跳过（数据格式不像答案）")
    
    if verbose:
        print(f"\n✓ 识别到 {len(model_columns)} 个模型列:")
        for i, col in enumerate(model_columns, 1):
            non_null_count = df[col].notna().sum()
            print(f"  {i}. {col} ({non_null_count} 个答案)")
    
    return model_columns


def evaluate_all_models(
    excel_path: str | Path,
    *,
    benchmark: Benchmark | None = None,
    benchmark_name: str = "hydrobench",
    id_col: str | None = None,
    output_dir: str | Path | None = None,
    verbose: bool = True,
) -> dict[str, Any]:
    """
    批量评估 CSV 或 Excel 文件中所有模型的得分。
    
    Args:
        excel_path: CSV 或 Excel 文件路径
        benchmark: Benchmark 对象，如果为 None 则使用内置的 benchmark
        benchmark_name: 如果 benchmark 为 None，使用此名称加载内置 benchmark
        id_col: ID 列名，如果为 None 则自动检测
        output_dir: 输出目录，如果为 None 则不保存文件
        verbose: 是否输出详细信息
    
    Returns:
        包含所有模型评估结果的字典
    """
    excel_path = Path(excel_path)
    if not excel_path.is_file():
        raise FileNotFoundError(f"File not found: {excel_path}")
    
    # 加载 benchmark
    if benchmark is None:
        if verbose:
            print(f"正在加载内置的 {benchmark_name} 测评集...")
        benchmark = load_builtin_benchmark(benchmark_name)
        if verbose:
            print(f"✓ 已加载测评集，共 {len(benchmark.examples)} 道题目\n")
    
    # 读取文件（支持 CSV 和 Excel）
    file_ext = excel_path.suffix.lower()
    if verbose:
        file_type = "CSV" if file_ext == ".csv" else "Excel"
        print(f"正在读取 {file_type} 文件：{excel_path}")
    
    if file_ext == ".csv":
        # 使用安全的 CSV 读取函数，支持多种编码和格式
        df = _read_csv_safe(excel_path)
    else:
        df = pd.read_excel(excel_path)
    
    if verbose:
        print(f"\n文件包含 {len(df)} 行，{len(df.columns)} 列")
        print(f"所有列名: {list(df.columns)}\n")
    
    # 识别模型列
    model_columns = identify_model_columns(df, verbose=verbose)
    
    if len(model_columns) == 0:
        raise ValueError(
            "未识别到任何模型列。请检查文件格式。\n"
            "提示：模型列应该包含答案数据（如 A, B, C, D 或 A,B 等）"
        )
    
    # 确定 ID 列
    if id_col is None:
        for possible_id in ["ID", "id", "Id"]:
            if possible_id in df.columns:
                id_col = possible_id
                break
    
    if verbose:
        if id_col:
            print(f"\n✓ 使用 ID 列进行匹配: {id_col}")
        else:
            print(f"\n⚠ 未找到 ID 列，将使用行顺序匹配")
    
    # 对每个模型列进行得分计算
    results = []
    errors = []
    
    if verbose:
        print("\n" + "=" * 80)
        print("开始批量计算得分...")
        print("=" * 80)
    
    for model_col in model_columns:
        if verbose:
            print(f"\n正在处理模型: {model_col}")
            print("-" * 80)
        
        try:
            # 加载该模型的预测结果
            predictions = load_predictions_from_excel(
                excel_path,
                id_col=id_col,
                answer_col=model_col
            )
            
            # 计算得分
            report = benchmark.score(predictions)
            
            # 统计信息
            correct_count = sum(1 for s in report.example_scores if s.is_correct)
            incorrect_count = len(report.example_scores) - correct_count
            missing_count = sum(1 for s in report.example_scores if s.missing_prediction)
            
            # Statistics by category, level, and type
            category_stats = report.get_category_stats(benchmark) if benchmark else {}
            level_stats = report.get_level_stats(benchmark) if benchmark else {}
            type_stats = report.get_type_stats(benchmark) if benchmark else {}
            
            # Save result
            result = {
                "model_name": model_col,
                "total_score": report.total_score,
                "max_score": report.max_score,
                "accuracy": report.accuracy,
                "correct_count": correct_count,
                "incorrect_count": incorrect_count,
                "missing_count": missing_count,
                "category_stats": category_stats,
                "level_stats": level_stats,
                "type_stats": type_stats,
            }
            results.append(result)
            
            if verbose:
                print(f"  总分: {report.total_score}/{report.max_score}")
                print(f"  准确率: {report.accuracy:.2%}")
                print(f"  答对: {correct_count}, 答错: {incorrect_count}, 缺失: {missing_count}")
            
            # 保存详细报告（JSON 和 Excel）
            if output_dir:
                output_dir_path = Path(output_dir)
                output_dir_path.mkdir(parents=True, exist_ok=True)
                
                # 生成安全的文件夹名（用于创建文件夹）
                safe_name = model_col.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_")
                
                # 为每个模型创建单独的文件夹
                model_dir = output_dir_path / safe_name
                model_dir.mkdir(parents=True, exist_ok=True)
                
                # 保存 JSON 报告
                json_file = model_dir / "score_report.json"
                json_file.write_text(report.to_json(), encoding="utf-8")
                
                # 保存 CSV 报告（轻量，推荐）
                csv_file = model_dir / "score_report.csv"
                try:
                    report.to_csv(csv_file, benchmark=benchmark)
                    if verbose:
                        print(f"  ✓ CSV 报告: {csv_file}")
                except ImportError:
                    if verbose:
                        print(f"  ⚠ 提示: 安装 pandas 可生成 CSV 报告")
                
                # 保存 Excel 报告（更直观，可选）
                excel_file = model_dir / "score_report.xlsx"
                try:
                    report.to_excel(excel_file, benchmark=benchmark)
                    if verbose:
                        print(f"  ✓ Excel 报告: {excel_file}")
                except ImportError:
                    if verbose:
                        print(f"  ⚠ 提示: 安装 pandas 和 openpyxl 可生成 Excel 报告")
                
                if verbose:
                    print(f"  ✓ 详细报告已保存到文件夹: {safe_name}/")
            
        except Exception as e:
            error_info = {
                "model_name": model_col,
                "error": str(e)
            }
            errors.append(error_info)
            if verbose:
                print(f"  ❌ 处理失败: {e}")
    
    # 按准确率排序
    sorted_results = sorted(results, key=lambda x: x["accuracy"], reverse=True)
    
    # 汇总结果
    summary = {
        "benchmark": benchmark_name,
        "total_questions": len(benchmark.examples),
        "models_count": len(model_columns),
        "model_columns": model_columns,
        "results": sorted_results,
        "errors": errors if errors else None,
    }
    
    # 保存汇总结果
    if output_dir:
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)
        summary_file = output_dir_path / "all_models_summary.json"
        summary_file.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        if verbose:
            print(f"\n✓ 汇总结果已保存到: {summary_file}")
    
    # 输出汇总
    if verbose:
        print("\n" + "=" * 80)
        print("所有模型得分汇总")
        print("=" * 80)
        print(f"{'模型名称':<40} {'总分':<15} {'准确率':<15} {'答对/答错/缺失':<25}")
        print("-" * 80)
        
        for result in sorted_results:
            score_str = f"{result['total_score']}/{result['max_score']}"
            accuracy_str = f"{result['accuracy']:.2%}"
            detail_str = f"{result['correct_count']}/{result['incorrect_count']}/{result['missing_count']}"
            print(f"{result['model_name']:<40} {score_str:<15} {accuracy_str:<15} {detail_str:<25}")
        
        if errors:
            print("\n处理失败的模型:")
            for error in errors:
                print(f"  {error['model_name']}: {error['error']}")
        
        print("\n" + "=" * 80)
        print("批量计算完成！")
        print("=" * 80)
        print(f"\n共处理 {len(model_columns)} 个模型")
        if output_dir:
            print(f"结果保存在: {output_dir_path}")
    
    return summary

