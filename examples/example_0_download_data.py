"""
示例 0: 下载 HydroBench 数据文件
展示如何使用 HydroBench 库下载内置的 hydrobench.json 和 hydrobench.csv 文件

本示例演示了两种方式：
1. 使用 Python API 下载
2. 使用命令行工具下载

注意：包内数据文件使用 CSV 格式（更轻量，适合版本控制），
     如果需要 Excel 格式，可以从 CSV 转换或使用报告导出功能。
"""

from pathlib import Path
from utils import setup_package_path, get_output_dir

# 设置包路径
PROJECT_ROOT = setup_package_path()

from hydrobench import download_hydrobench_data


def download_with_python_api():
    """使用 Python API 下载数据文件"""
    print("=" * 80)
    print("方式 1: 使用 Python API 下载")
    print("=" * 80)
    print()
    
    output_dir = get_output_dir(PROJECT_ROOT, "example_0_download_data")
    
    # 示例 1: 下载 JSON 文件到当前目录
    print("示例 1.1: 下载 JSON 文件到当前目录")
    print("-" * 80)
    json_path = download_hydrobench_data("json")
    print(f"✓ JSON 文件已下载到: {json_path}")
    print(f"  文件大小: {json_path.stat().st_size / 1024:.2f} KB")
    print()
    
    # 示例 2: 下载 CSV 文件到当前目录
    print("示例 1.2: 下载 CSV 文件到当前目录")
    print("-" * 80)
    csv_path = download_hydrobench_data("csv")
    print(f"✓ CSV 文件已下载到: {csv_path}")
    print(f"  文件大小: {csv_path.stat().st_size / 1024:.2f} KB")
    print()
    
    # 示例 3: 下载 JSON 文件到指定目录
    print("示例 1.3: 下载 JSON 文件到指定目录")
    print("-" * 80)
    custom_json_path = output_dir / "hydrobench.json"
    json_path = download_hydrobench_data("json", custom_json_path)
    print(f"✓ JSON 文件已下载到: {json_path}")
    print()
    
    # 示例 4: 下载 CSV 文件到指定目录
    print("示例 1.4: 下载 CSV 文件到指定目录")
    print("-" * 80)
    custom_csv_path = output_dir / "hydrobench.csv"
    csv_path = download_hydrobench_data("csv", custom_csv_path)
    print(f"✓ CSV 文件已下载到: {csv_path}")
    print()
    
    # 示例 5: 下载到自定义文件名
    print("示例 1.5: 下载到自定义文件名")
    print("-" * 80)
    custom_path = output_dir / "my_custom_hydrobench.csv"
    csv_path = download_hydrobench_data("csv", custom_path)
    print(f"✓ CSV 文件已下载到: {csv_path}")
    print()
    
    return output_dir


def download_with_cli():
    """使用命令行工具下载数据文件"""
    print("=" * 80)
    print("方式 2: 使用命令行工具下载")
    print("=" * 80)
    print()
    
    print("以下命令可以在终端中运行：")
    print()
    
    print("1. 下载所有格式（JSON、CSV、Excel）到当前目录：")
    print("   python -m hydrobench download")
    print()
    
    print("2. 只下载 JSON 文件：")
    print("   python -m hydrobench download --format json")
    print()
    
    print("3. 只下载 CSV 文件（推荐，轻量）：")
    print("   python -m hydrobench download --format csv")
    print()
    
    print("4. 只下载 Excel 文件（如果包内存在）：")
    print("   python -m hydrobench download --format xlsx")
    print()
    
    print("5. 下载到指定目录：")
    print("   python -m hydrobench download --output ./my_data")
    print()
    
    print("6. 下载到指定文件路径：")
    print("   python -m hydrobench download --format csv --output ./my_data/hydrobench.csv")
    print()
    
    print("注意：命令行方式需要先安装 hydrobench 包")
    print("     安装方式: pip install -e ../hydrobench-eval")
    print()


def verify_downloaded_files(output_dir: Path):
    """验证下载的文件"""
    print("=" * 80)
    print("验证下载的文件")
    print("=" * 80)
    print()
    
    json_file = output_dir / "hydrobench.json"
    csv_file = output_dir / "hydrobench.csv"
    
    if json_file.exists():
        print(f"✓ JSON 文件存在: {json_file}")
        print(f"  文件大小: {json_file.stat().st_size / 1024:.2f} KB")
        
        # 尝试读取 JSON 文件验证格式
        import json
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    print(f"  包含 {len(data)} 条记录")
                elif isinstance(data, dict) and 'examples' in data:
                    print(f"  包含 {len(data['examples'])} 条记录")
        except Exception as e:
            print(f"  ⚠️  读取 JSON 文件时出错: {e}")
    else:
        print(f"✗ JSON 文件不存在: {json_file}")
    
    print()
    
    if csv_file.exists():
        print(f"✓ CSV 文件存在: {csv_file}")
        print(f"  文件大小: {csv_file.stat().st_size / 1024:.2f} KB")
        
        # 尝试读取 CSV 文件验证格式
        try:
            import pandas as pd
            df = pd.read_csv(csv_file, nrows=0, encoding='utf-8')  # 只读取列名
            print(f"  包含列: {', '.join(df.columns.tolist())}")
        except Exception as e:
            print(f"  ⚠️  读取 CSV 文件时出错: {e}")
    else:
        print(f"✗ CSV 文件不存在: {csv_file}")
    
    print()


def main():
    """主函数"""
    print()
    print("=" * 80)
    print("示例 0: 下载 HydroBench 数据文件")
    print("=" * 80)
    print()
    print("本示例展示如何下载包内置的 hydrobench.json 和 hydrobench.csv 文件")
    print("这些文件包含了完整的测评集数据，可以用于本地评估和分析")
    print()
    print("注意：CSV 格式更轻量，适合版本控制。如果需要 Excel 格式，")
    print("     可以使用报告导出功能（report.to_excel()）或从 CSV 转换。")
    print()
    
    # 使用 Python API 下载
    output_dir = download_with_python_api()
    
    # 显示命令行方式
    download_with_cli()
    
    # 验证下载的文件
    verify_downloaded_files(output_dir)
    
    print("=" * 80)
    print("示例完成！")
    print("=" * 80)
    print()
    print(f"所有文件已保存到: {output_dir}")
    print()


if __name__ == "__main__":
    main()

