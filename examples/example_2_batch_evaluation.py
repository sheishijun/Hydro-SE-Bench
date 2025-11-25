"""
示例 2: 批量评估多个模型
展示如何使用 HydroBench 库批量评估 Excel 文件中的多个模型
"""

from utils import setup_package_path, get_output_dir, get_test_data_path

# 设置包路径
PROJECT_ROOT = setup_package_path()

from hydrobench import evaluate_all_models, load_builtin_benchmark, create_summary_excel


def main():
    """批量评估示例"""
    print("=" * 80)
    print("示例 2: 批量评估多个模型")
    print("=" * 80)
    print()
    
    # 1. 设置输入和输出路径
    excel_path = get_test_data_path(PROJECT_ROOT)
    output_dir = get_output_dir(PROJECT_ROOT, "example_2_batch_evaluation")
    
    if not excel_path.exists():
        print(f"⚠ 示例文件不存在: {excel_path}")
        print("请确保 test.xlsx 文件存在，或修改 excel_path 指向您的数据文件")
        return
    
    print(f"输入文件: {excel_path}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 2. 执行批量评估
    # evaluate_all_models 会自动：
    # - 识别 Excel 文件中的所有模型列
    # - 为每个模型计算得分
    # - 生成详细的 Excel 报告（每个模型一个文件）
    # - 保存汇总 JSON 文件
    print("正在执行批量评估...")
    summary = evaluate_all_models(
        excel_path,
        benchmark_name="hydrobench",
        output_dir=output_dir,
        verbose=True,
    )
    
    # 3. 生成模型对比汇总 Excel
    print("\n正在生成模型对比汇总...")
    benchmark = load_builtin_benchmark("hydrobench")
    create_summary_excel(summary, output_dir, benchmark)
    
    # 4. 显示汇总结果
    print("\n" + "=" * 80)
    print("评估完成！")
    print("=" * 80)
    print(f"\n共评估 {summary['models_count']} 个模型，{summary['total_questions']} 道题目")
    print("\n模型得分排名（按准确率排序）：")
    print("-" * 80)
    print(f"{'排名':<6} {'模型名称':<40} {'得分':<15} {'准确率':<12}")
    print("-" * 80)
    
    for idx, result in enumerate(summary["results"], 1):
        score_str = f"{result['total_score']}/{result['max_score']}"
        accuracy_str = f"{result['accuracy']:.2%}"
        print(f"{idx:<6} {result['model_name']:<40} {score_str:<15} {accuracy_str:<12}")
    
    print("\n" + "=" * 80)
    print("输出文件说明：")
    print("=" * 80)
    print(f"1. 每个模型的详细报告: {output_dir}/<模型名>/")
    print("   - score_report.xlsx: 包含题目内容、正确答案、模型答案的详细对比")
    print("   - score_report.json: JSON 格式的详细数据")
    print("   - 包含按类别和难度的统计表")
    print(f"2. 模型对比汇总（Excel）: {output_dir}/models_comparison.xlsx")
    print("   - 所有模型的得分对比")
    print("   - 按类别、难度和题型的模型间对比")
    print(f"3. 汇总数据（JSON）: {output_dir}/all_models_summary.json")
    print("   - 完整的评估数据，包含按类别和难度的统计，便于程序处理")
    print("=" * 80)


if __name__ == "__main__":
    main()

