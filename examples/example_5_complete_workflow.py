"""
示例 5: 完整工作流程
展示从数据验证、采样、评估到深度分析的完整企业级工作流程
包括：数据质量检查、采样创建子集、批量评估、详细分析、错误分析、报告生成等
"""

from utils import setup_package_path, get_output_dir, get_test_data_path
from pathlib import Path

# 设置包路径
PROJECT_ROOT = setup_package_path()

from hydrobench import (
    evaluate_all_models,
    load_builtin_benchmark,
    create_summary_excel,
    identify_model_columns,
    sample_benchmark_by_category,
    validate_data_quality,
    generate_analysis_report,
)
from hydrobench.excel_loader import _read_csv_safe, _detect_file_format
import pandas as pd


def main():
    """完整工作流程示例"""
    print("=" * 80)
    print("示例 5: 完整工作流程")
    print("=" * 80)
    print("本示例展示：数据验证 → 采样 → 评估 → 深度分析 → 报告生成")
    print("=" * 80)
    print()
    
    # ========== 阶段 1: 数据准备和验证 ==========
    print("【阶段 1】数据准备和验证")
    print("-" * 80)
    
    excel_path = get_test_data_path(PROJECT_ROOT)
    output_dir = get_output_dir(PROJECT_ROOT, "example_5_complete_workflow")
    
    if not excel_path.exists():
        print(f"⚠ 示例文件不存在: {excel_path}")
        print("请确保 test.xlsx 文件存在，或修改 excel_path 指向您的数据文件")
        return
    
    print(f"输入文件: {excel_path}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 1.1 加载测评集
    print("步骤 1.1: 加载测评集...")
    benchmark = load_builtin_benchmark("hydrobench")
    print(f"✓ 已加载测评集，共 {len(benchmark.examples)} 道题目")
    
    # 统计测评集信息
    category_counts = {}
    level_counts = {}
    for ex in benchmark.examples:
        category_counts[ex.category] = category_counts.get(ex.category, 0) + 1
        if ex.level:
            level_counts[ex.level] = level_counts.get(ex.level, 0) + 1
    
    print(f"  - 类别分布: {dict(sorted(category_counts.items()))}")
    if level_counts:
        print(f"  - 难度分布: {dict(sorted(level_counts.items()))}")
    print()
    
    # 1.2 预览和验证数据
    print("步骤 1.2: 预览和验证预测数据...")
    # 根据文件格式安全地读取文件
    file_ext = excel_path.suffix.lower()
    actual_format = _detect_file_format(excel_path)
    
    # 如果扩展名是 .csv 但实际是 Excel 格式，使用 Excel 读取方式
    if file_ext == ".csv" and actual_format == 'excel':
        print(f"  ⚠ 警告: 文件扩展名是 .csv，但检测到实际格式是 Excel。将使用 Excel 读取方式。")
        df = pd.read_excel(excel_path, engine='openpyxl')
    elif file_ext == ".csv":
        df = _read_csv_safe(excel_path)
    elif file_ext in (".xlsx", ".xls"):
        # 尝试使用 openpyxl 引擎（.xlsx）或 xlrd 引擎（.xls）
        try:
            if file_ext == ".xlsx":
                df = pd.read_excel(excel_path, engine='openpyxl')
            else:
                df = pd.read_excel(excel_path, engine='xlrd')
        except Exception:
            # 如果指定引擎失败，让 pandas 自动选择
            df = pd.read_excel(excel_path)
    else:
        # 如果扩展名不支持，但检测到是 Excel 格式，尝试使用 Excel 读取
        if actual_format == 'excel':
            print(f"  ⚠ 警告: 文件扩展名是 {file_ext}，但检测到实际格式是 Excel。将尝试使用 Excel 读取方式。")
            try:
                df = pd.read_excel(excel_path, engine='openpyxl')
            except Exception:
                df = pd.read_excel(excel_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: .csv, .xlsx, .xls")
    
    print(f"  - 数据行数: {len(df)}")
    print(f"  - 总列数: {len(df.columns)}")
    
    # 数据质量检查
    quality_report = validate_data_quality(df, benchmark)
    print(f"  - 识别到 {quality_report['model_count']} 个模型列")
    
    if quality_report["issues"]:
        print("  ⚠ 发现严重问题:")
        for issue in quality_report["issues"]:
            print(f"    - {issue}")
    
    if quality_report["warnings"]:
        print("  ⚠ 警告信息:")
        for warning in quality_report["warnings"]:
            print(f"    - {warning}")
    
    if not quality_report["issues"]:
        print("  ✓ 数据质量检查通过")
    print()
    
    # ========== 阶段 2: 采样创建子集（可选） ==========
    print("【阶段 2】采样创建测试子集（可选）")
    print("-" * 80)
    
    use_sampled = False  # 可以设置为 True 来使用采样后的子集
    if use_sampled:
        print("步骤 2.1: 创建采样子集...")
        sampled_benchmark = sample_benchmark_by_category(
            benchmark,
            per_category=5,
            seed=42,
            output_path=output_dir / "sampled_benchmark.json",
        )
        benchmark = sampled_benchmark
        print(f"✓ 已创建采样子集，共 {len(benchmark.examples)} 道题目")
        print()
    else:
        print("  (跳过采样，使用完整测评集)")
        print()
    
    # ========== 阶段 3: 批量评估 ==========
    print("【阶段 3】批量评估所有模型")
    print("-" * 80)
    
    print("步骤 3.1: 识别模型列...")
    model_columns = identify_model_columns(df, verbose=True)
    print()
    
    if not model_columns:
        print("⚠ 未识别到任何模型列，请检查 Excel 文件格式")
        return
    
    print("步骤 3.2: 执行批量评估...")
    summary = evaluate_all_models(
        excel_path,
        benchmark=benchmark,
        output_dir=output_dir,
        verbose=True,
    )
    print()
    
    # ========== 阶段 4: 生成汇总报告 ==========
    print("【阶段 4】生成汇总报告")
    print("-" * 80)
    
    print("步骤 4.1: 生成模型对比 Excel...")
    create_summary_excel(summary, output_dir, benchmark)
    print("✓ 模型对比汇总 Excel 已生成")
    print()
    
    # ========== 阶段 5: 深度分析 ==========
    print("【阶段 5】深度数据分析")
    print("-" * 80)
    
    # 检查是否有结果
    if not summary["results"]:
        print("⚠ 没有成功评估的模型，无法进行深度分析")
        if summary.get("errors"):
            print("\n处理失败的模型:")
            for error in summary["errors"]:
                print(f"  - {error['model_name']}: {error['error']}")
        return
    
    # 5.1 基础统计分析
    print("步骤 5.1: 基础统计分析...")
    best_model = summary["results"][0]
    worst_model = summary["results"][-1]
    avg_accuracy = sum(r["accuracy"] for r in summary["results"]) / len(summary["results"])
    
    print(f"  🏆 最佳模型: {best_model['model_name']} ({best_model['accuracy']:.2%})")
    print(f"  📉 最差模型: {worst_model['model_name']} ({worst_model['accuracy']:.2%})")
    print(f"  📊 平均准确率: {avg_accuracy:.2%}")
    print(f"  📈 准确率标准差: {pd.Series([r['accuracy'] for r in summary['results']]).std():.4f}")
    print()
    
    # 5.2 类别分析
    print("步骤 5.2: 类别维度分析...")
    if any(r.get("category_stats") for r in summary["results"]):
        all_categories = set()
        for result in summary["results"]:
            if result.get("category_stats"):
                all_categories.update(result["category_stats"].keys())
        
        print("  各类别最佳表现:")
        for category in sorted(all_categories):
            best_acc = 0
            best_model_name = ""
            worst_acc = 1.0
            worst_model_name = ""
            
            for result in summary["results"]:
                stats = result.get("category_stats", {}).get(category, {})
                if stats:
                    acc = stats.get("accuracy", 0)
                    if acc > best_acc:
                        best_acc = acc
                        best_model_name = result["model_name"]
                    if acc < worst_acc:
                        worst_acc = acc
                        worst_model_name = result["model_name"]
            
            print(f"    {category}:")
            print(f"      最佳: {best_model_name} ({best_acc:.2%})")
            print(f"      最差: {worst_model_name} ({worst_acc:.2%})")
            print(f"      差距: {(best_acc - worst_acc):.2%}")
    print()
    
    # 5.3 难度分析
    print("步骤 5.3: 难度维度分析...")
    if any(r.get("level_stats") for r in summary["results"]):
        all_levels = set()
        for result in summary["results"]:
            if result.get("level_stats"):
                all_levels.update(result["level_stats"].keys())
        
        print("  各难度级别平均表现:")
        for level in sorted(all_levels):
            level_accuracies = []
            for result in summary["results"]:
                stats = result.get("level_stats", {}).get(level, {})
                if stats:
                    level_accuracies.append(stats.get("accuracy", 0))
            
            if level_accuracies:
                avg_level_acc = sum(level_accuracies) / len(level_accuracies)
                print(f"    {level}: 平均准确率 {avg_level_acc:.2%} ({len(level_accuracies)} 个模型)")
    print()
    
    
    # 5.4 生成深度分析报告
    print("步骤 5.5: 生成深度分析报告...")
    analysis_report = generate_analysis_report(summary, benchmark, output_dir)
    print()
    
    # ========== 阶段 6: 总结和建议 ==========
    print("【阶段 6】总结和建议")
    print("-" * 80)
    
    print("评估总结:")
    print(f"  - 共评估 {summary['models_count']} 个模型")
    print(f"  - 共 {summary['total_questions']} 道题目")
    print(f"  - 最佳模型准确率: {best_model['accuracy']:.2%}")
    print(f"  - 模型间准确率差距: {(best_model['accuracy'] - worst_model['accuracy']):.2%}")
    print()
    
    print("关键建议:")
    for i, rec in enumerate(analysis_report["recommendations"], 1):
        print(f"  {i}. {rec}")
    print()
    
    # ========== 输出文件清单 ==========
    print("=" * 80)
    print("生成的文件清单")
    print("=" * 80)
    print(f"\n输出目录: {output_dir}")
    print("\n文件列表:")
    
    file_count = 0
    total_size = 0
    for file in sorted(output_dir.glob("*")):
        if file.is_file():
            size = file.stat().st_size
            total_size += size
            size_str = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / (1024 * 1024):.1f} MB"
            print(f"  - {file.name} ({size_str})")
            file_count += 1
    
    print(f"\n总计: {file_count} 个文件，总大小: {total_size / (1024 * 1024):.2f} MB")
    print("\n" + "=" * 80)
    print("✓ 完整工作流程执行完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()

