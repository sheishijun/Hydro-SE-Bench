"""
示例 3: 使用自定义测评集
展示如何从 CSV 或 Excel 文件加载自定义测评集并进行评估
"""

from utils import setup_package_path, get_output_dir, get_test_data_path, get_benchmark_data_path

# 设置包路径
PROJECT_ROOT = setup_package_path()

from hydrobench import (
    load_benchmark_from_file,
    load_predictions_from_excel,
    Benchmark,
)


def main():
    """自定义测评集示例"""
    print("=" * 80)
    print("示例 3: 使用自定义测评集")
    print("=" * 80)
    print()
    
    # 1. 从 CSV 或 Excel 文件加载自定义测评集
    print("步骤 1: 加载自定义测评集...")
    benchmark_excel = get_benchmark_data_path(PROJECT_ROOT)
    
    if not benchmark_excel.exists():
        print(f"⚠ 示例文件不存在: {benchmark_excel}")
        print("请确保测评集 CSV 或 Excel 文件存在")
        return
    
    # 先尝试读取文件检查列（可选，用于显示信息）
    # 如果失败，直接加载 benchmark 即可
    import pandas as pd
    file_ext = benchmark_excel.suffix.lower()
    has_level_col = None
    has_type_col = None
    
    try:
        if file_ext == ".csv":
            # 尝试读取前几行检查列（使用与包中相同的逻辑）
            # 这里使用简单的方式，如果失败就跳过检查
            try:
                df_check = pd.read_csv(benchmark_excel, nrows=5, engine='python', encoding='utf-8')
            except:
                try:
                    df_check = pd.read_csv(benchmark_excel, nrows=5, engine='python', encoding='gbk')
                except:
                    df_check = None
            file_type = "CSV"
        else:
            df_check = pd.read_excel(benchmark_excel, nrows=5)
            file_type = "Excel"
        
        if df_check is not None:
            print(f"{file_type} 文件中的列: {list(df_check.columns)}")
            has_level_col = "Level" in df_check.columns
            has_type_col = "Type" in df_check.columns
            print(f"  - 是否有 'Level' 列: {has_level_col}")
            print(f"  - 是否有 'Type' 列: {has_type_col}")
            
            if has_level_col:
                print(f"  - 'Level' 列的前几个值: {df_check['Level'].head(3).tolist()}")
            if has_type_col:
                print(f"  - 'Type' 列的前几个值: {df_check['Type'].head(3).tolist()}")
    except Exception as e:
        print(f"⚠ 无法读取文件进行列检查（将直接加载 benchmark）: {e}")
    
    # 加载 benchmark，使用包中的函数（它会自动处理 CSV 读取的兼容性问题）
    # 明确指定列名以确保正确读取 Level 和 Type
    benchmark = load_benchmark_from_file(
        benchmark_excel,
        level_col="Level" if has_level_col else None,  # 难度列名（如果检测到）
        type_col="Type" if has_type_col else None,     # 题型列名（如果检测到）
        category_col="ID",   # 类别列名（从 ID 中提取）
    )
    print(f"✓ 已加载自定义测评集，共 {len(benchmark.examples)} 道题目")
    
    # 检查是否有难度和题型信息
    examples_with_level = sum(1 for ex in benchmark.examples if ex.level)
    examples_with_type = sum(1 for ex in benchmark.examples if ex.question_type)
    examples_with_category = sum(1 for ex in benchmark.examples if ex.category)
    print(f"  - 包含难度信息的题目: {examples_with_level}/{len(benchmark.examples)}")
    print(f"  - 包含题型信息的题目: {examples_with_type}/{len(benchmark.examples)}")
    print(f"  - 包含类别信息的题目: {examples_with_category}/{len(benchmark.examples)}")
    
    # 显示一些示例的 level 和 type 值
    if examples_with_level > 0:
        sample_levels = [ex.level for ex in benchmark.examples[:5] if ex.level]
        print(f"  - 示例 Level 值: {sample_levels[:3]}")
    if examples_with_type > 0:
        sample_types = [ex.question_type for ex in benchmark.examples[:5] if ex.question_type]
        print(f"  - 示例 Type 值: {sample_types[:3]}")
    
    if examples_with_level == 0:
        print(f"  ⚠ 警告: {file_type} 文件中可能没有 'Level' 列，或列名不匹配")
        if not has_level_col:
            print(f"     提示: {file_type} 文件中确实没有 'Level' 列")
            print("     解决方案: 如果列名不同（如'难度'），请修改 level_col 参数")
    if examples_with_type == 0:
        print(f"  ⚠ 警告: {file_type} 文件中可能没有 'Type' 列，或列名不匹配")
        if not has_type_col:
            print(f"     提示: {file_type} 文件中确实没有 'Type' 列")
            print("     解决方案: 如果列名不同（如'题型'），请修改 type_col 参数")
    print()
    
    # 2. 加载模型预测结果
    print("步骤 2: 加载模型预测结果...")
    predictions_excel = get_test_data_path(PROJECT_ROOT)
    
    if not predictions_excel.exists():
        print(f"⚠ 示例文件不存在: {predictions_excel}")
        print("请确保预测结果 CSV 或 Excel 文件存在")
        return
    
    predictions = load_predictions_from_excel(
        predictions_excel,
        id_col="ID",
        answer_col="DeepSeek-V3.2-Exp"  # 请根据实际列名修改
    )
    print(f"✓ 已加载 {len(predictions)} 个预测结果")
    print()
    
    # 3. 计算得分
    print("步骤 3: 计算得分...")
    report = benchmark.score(predictions)
    
    # 4. 显示结果
    print("\n" + "=" * 80)
    print("评估结果")
    print("=" * 80)
    print(report.summary())
    print()
    
    # 5. 显示按类别统计
    category_stats = report.get_category_stats(benchmark)
    if category_stats:
        print("\n按类别统计：")
        print("-" * 80)
        for category, stats in sorted(category_stats.items()):
            print(f"{category}: {stats['correct']}/{stats['total']} ({stats['accuracy']:.2%})")
    
    # 6. 显示按难度统计
    level_stats = report.get_level_stats(benchmark)
    if level_stats:
        print("\n按难度统计：")
        print("-" * 80)
        for level, stats in sorted(level_stats.items()):
            print(f"{level}: {stats['correct']}/{stats['total']} ({stats['accuracy']:.2%})")
    
    # 7. 保存报告（可选）
    output_dir = get_output_dir(PROJECT_ROOT, "example_3_custom_benchmark")
    
    # 保存 JSON 报告
    json_file = output_dir / "custom_benchmark_report.json"
    json_file.write_text(report.to_json(), encoding="utf-8")
    print(f"\n✓ JSON 报告已保存: {json_file}")
    
    # 保存 CSV 报告（轻量，推荐）
    try:
        csv_file = output_dir / "custom_benchmark_report.csv"
        report.to_csv(csv_file, benchmark=benchmark)
        print(f"✓ CSV 报告已保存: {csv_file}")
    except ImportError:
        print("⚠ 未安装 pandas，跳过 CSV 报告生成")
    
    # 保存 Excel 报告（如果安装了 pandas 和 openpyxl）
    try:
        excel_file = output_dir / "custom_benchmark_report.xlsx"
        report.to_excel(excel_file, benchmark=benchmark)
        print(f"✓ Excel 报告已保存: {excel_file}")
    except ImportError:
        print("⚠ 未安装 pandas 或 openpyxl，跳过 Excel 报告生成")
    
    print("\n" + "=" * 80)
    print("示例完成！")
    print("=" * 80)
    print(f"\n输出文件保存在: {output_dir}")


if __name__ == "__main__":
    main()

