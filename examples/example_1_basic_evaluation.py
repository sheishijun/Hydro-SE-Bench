"""
示例 1: 基础评估功能
展示如何使用 HydroBench 库进行单个模型的评估
"""

from utils import setup_package_path, get_output_dir, get_test_data_path

# 设置包路径
PROJECT_ROOT = setup_package_path()

from hydrobench import Benchmark, load_builtin_benchmark, load_predictions_from_excel


def main():
    """基础评估示例"""
    print("=" * 80)
    print("示例 1: 基础评估功能")
    print("=" * 80)
    print()
    
    # 1. 加载内置的测评集
    print("步骤 1: 加载测评集...")
    benchmark = load_builtin_benchmark("hydrobench")
    print(f"✓ 已加载测评集，共 {len(benchmark.examples)} 道题目")
    print()
    
    # 2. 加载模型预测结果（从 CSV 或 Excel 文件）
    print("步骤 2: 加载模型预测结果...")
    excel_path = get_test_data_path(PROJECT_ROOT)
    
    if not excel_path.exists():
        print(f"⚠ 示例文件不存在: {excel_path}")
        print("请确保 test.csv 或 test.xlsx 文件存在，或修改 excel_path 指向您的数据文件")
        return
    
    # 假设 CSV/Excel 文件中有一个名为 "DeepSeek-V3.2-Exp" 的列包含模型答案
    # load_predictions_from_excel 函数支持 CSV 和 Excel 格式（自动识别）
    predictions = load_predictions_from_excel(
        excel_path,
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
    
    # 5. 保存报告（可选）
    output_dir = get_output_dir(PROJECT_ROOT, "example_1_basic_evaluation")
    
    # 保存 JSON 报告
    json_file = output_dir / "basic_evaluation_report.json"
    json_file.write_text(report.to_json(), encoding="utf-8")
    print(f"✓ JSON 报告已保存: {json_file}")
    
    # 保存 CSV 报告（轻量，推荐）
    try:
        csv_file = output_dir / "basic_evaluation_report.csv"
        report.to_csv(csv_file, benchmark=benchmark)
        print(f"✓ CSV 报告已保存: {csv_file}")
    except ImportError:
        print("⚠ 未安装 pandas，跳过 CSV 报告生成")
    
    # 保存 Excel 报告（如果安装了 pandas 和 openpyxl）
    try:
        excel_file = output_dir / "basic_evaluation_report.xlsx"
        report.to_excel(excel_file, benchmark=benchmark)
        print(f"✓ Excel 报告已保存: {excel_file}")
    except ImportError:
        print("⚠ 未安装 pandas 或 openpyxl，跳过 Excel 报告生成")
    
    print("\n" + "=" * 80)
    print("示例完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()

