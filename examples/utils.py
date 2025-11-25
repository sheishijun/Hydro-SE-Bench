"""
示例代码的公共工具函数
"""

from pathlib import Path
import sys


def setup_package_path() -> Path:
    """
    设置包路径并返回项目根目录。
    
    Returns:
        项目根目录路径
    """
    project_root = Path(__file__).resolve().parent.parent
    package_dir = project_root / "hydrobench-eval"
    
    if package_dir.exists() and str(package_dir) not in sys.path:
        sys.path.insert(0, str(package_dir))
    
    return project_root


def get_output_dir(project_root: Path, example_name: str) -> Path:
    """
    获取示例的输出目录。
    
    Args:
        project_root: 项目根目录
        example_name: 示例名称（如 "example_1_basic_evaluation"）
    
    Returns:
        输出目录路径
    """
    output_dir = project_root / "examples" / "output" / example_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_test_data_path(project_root: Path) -> Path:
    """
    获取测试数据文件路径。
    优先返回 CSV 文件，如果不存在则返回 Excel 文件。
    
    Args:
        project_root: 项目根目录
    
    Returns:
        测试数据文件路径（CSV 或 Excel）
    """
    csv_path = project_root / "examples" / "test.csv"
    if csv_path.exists():
        return csv_path
    return project_root / "examples" / "test.xlsx"


def get_benchmark_data_path(project_root: Path) -> Path:
    """
    获取内置测评集数据文件路径。
    优先返回 CSV 文件，如果不存在则返回 Excel 文件。
    
    Args:
        project_root: 项目根目录
    
    Returns:
        测评集数据文件路径（CSV 或 Excel）
    """
    csv_path = project_root / "hydrobench-eval" / "hydrobench" / "data" / "hydrobench.csv"
    if csv_path.exists():
        return csv_path
    return project_root / "hydrobench-eval" / "hydrobench" / "data" / "hydrobench.xlsx"

