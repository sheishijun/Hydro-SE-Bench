"""
示例 4: 采样功能
展示如何从测评集中按类别采样题目
"""

from utils import setup_package_path, get_output_dir, get_benchmark_data_path

# 设置包路径
PROJECT_ROOT = setup_package_path()

from hydrobench import (
    load_builtin_benchmark,
    load_benchmark_from_file,
    sample_benchmark_by_category,
    sample_examples_by_category,
    save_benchmark,
)


def main():
    """采样功能示例"""
    print("=" * 80)
    print("示例 4: 采样功能")
    print("=" * 80)
    print()
    
    # 1. 加载测评集
    print("步骤 1: 加载测评集...")
    benchmark = load_builtin_benchmark("hydrobench")
    print(f"✓ 已加载测评集，共 {len(benchmark.examples)} 道题目")
    print()
    
    # 2. 按类别采样题目
    print("步骤 2: 按类别采样题目...")
    print("从每个类别中采样 5 道题目...")
    
    sampled_examples = sample_examples_by_category(
        benchmark,
        per_category=5
    )
    
    print(f"✓ 采样完成，共采样 {len(sampled_examples)} 道题目")
    print()
    
    # 显示采样结果统计
    from collections import Counter
    categories = []
    for example in sampled_examples:
        category = example.category
        if category:
            categories.append(category)
    
    category_counts = Counter(categories)
    print("采样结果按类别分布：")
    print("-" * 80)
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} 道")
    print()
    
    # 3. 创建采样后的测评集并自动保存
    print("步骤 3: 创建采样后的测评集...")
    output_dir = get_output_dir(PROJECT_ROOT, "example_4_sampling")
    
    # 根据输入格式自动选择输出格式
    # 由于使用的是内置 benchmark（从 JSON 加载），输出 JSON
    output_file = output_dir / "sampled_benchmark_from_json.json"
    
    sampled_benchmark = sample_benchmark_by_category(
        benchmark,
        per_category=5,
        output_path=output_file  # 自动保存，格式根据输入自动检测
    )
    
    print(f"✓ 已创建采样后的测评集，共 {len(sampled_benchmark.examples)} 道题目")
    print(f"✓ 采样结果已自动保存: {output_file}")
    print()
    
    # 4. 演示从 csv 加载并采样（如果 csv 文件存在）
    excel_benchmark_path = get_benchmark_data_path(PROJECT_ROOT)
    if excel_benchmark_path.exists():
        print("步骤 4: 演示从 csv/excel加载并采样...")
        excel_benchmark = load_benchmark_from_file(excel_benchmark_path)
        
        # 从 csv 加载的，输出 csv格式
        excel_output_file = output_dir / "sampled_benchmark_from_csv.csv"
        sampled_excel_benchmark = sample_benchmark_by_category(
            excel_benchmark,
            per_category=5,
            output_path=excel_output_file  # 自动保存为 csv 格式
        )
        
        print(f"✓ 从 Excel 加载并采样完成，共 {len(sampled_excel_benchmark.examples)} 道题目")
        print(f"✓ 采样结果已自动保存为 csv: {excel_output_file}")
        print()
    
    print("\n" + "=" * 80)
    print("示例完成！")
    print("=" * 80)
    print(f"\n输出文件保存在: {output_dir}")
    print("说明: 输出格式根据输入格式自动选择（JSON 输入 -> JSON 输出，csv 输入 -> csv 输出）")


if __name__ == "__main__":
    main()

