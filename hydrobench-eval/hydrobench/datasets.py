from __future__ import annotations

import shutil
from pathlib import Path

from .benchmark import Benchmark

# 包内数据目录（相对于当前文件）
_PACKAGE_DIR = Path(__file__).resolve().parent
_DATA_DIR = _PACKAGE_DIR / "data"

BUILTIN_BENCHMARKS: dict[str, Path] = {
    "hydrobench": _DATA_DIR / "hydrobench.json",
}


def load_builtin_benchmark(name: str) -> Benchmark:
    """
    加载内置的测评集。
    
    Args:
        name: 测评集名称，目前支持 "hydrobench"
    
    Returns:
        Benchmark 对象
    
    Example:
        >>> benchmark = load_builtin_benchmark("hydrobench")
        >>> report = benchmark.score(predictions)
    """
    try:
        json_path = BUILTIN_BENCHMARKS[name]
    except KeyError as exc:  # pragma: no cover - defensive
        raise ValueError(
            f"Unknown benchmark '{name}'. Valid options: {sorted(BUILTIN_BENCHMARKS)}"
        ) from exc

    if not json_path.is_file():
        raise FileNotFoundError(
            f"Benchmark file not found: {json_path}. "
            "This may indicate a corrupted package installation."
        )
    return Benchmark.from_file(json_path)


def download_hydrobench_data(
    file_format: str = "json", output_path: Path | str | None = None
) -> Path:
    """
    下载包内的 hydrobench 数据文件到指定位置。
    
    Args:
        file_format: 文件格式，支持 "json"、"csv" 或 "xlsx"，默认为 "json"
        output_path: 输出文件路径。如果为 None，则保存到当前工作目录
    
    Returns:
        下载后的文件路径
    
    Raises:
        ValueError: 当 file_format 不是 "json"、"csv" 或 "xlsx" 时
        FileNotFoundError: 当包内数据文件不存在时
    
    Example:
        >>> # 下载 JSON 文件到当前目录
        >>> from hydrobench import download_hydrobench_data
        >>> path = download_hydrobench_data("json")
        >>> print(f"文件已下载到: {path}")
        
        >>> # 下载 CSV 文件到指定路径
        >>> from pathlib import Path
        >>> path = download_hydrobench_data("csv", Path("./my_data/hydrobench.csv"))
        >>> print(f"文件已下载到: {path}")
        
        >>> # 下载 Excel 文件到指定路径
        >>> path = download_hydrobench_data("xlsx", Path("./my_data/hydrobench.xlsx"))
        >>> print(f"文件已下载到: {path}")
    """
    if file_format not in ("json", "csv", "xlsx"):
        raise ValueError(f'file_format 必须是 "json"、"csv" 或 "xlsx"，当前为: {file_format}')
    
    # 确定源文件路径
    source_file = _DATA_DIR / f"hydrobench.{file_format}"
    
    if not source_file.is_file():
        raise FileNotFoundError(
            f"包内数据文件不存在: {source_file}. "
            "This may indicate a corrupted package installation."
        )
    
    # 确定输出路径
    if output_path is None:
        output_path = Path.cwd() / f"hydrobench.{file_format}"
    else:
        output_path = Path(output_path)
        # 如果输出路径是目录，添加文件名
        if output_path.is_dir():
            output_path = output_path / f"hydrobench.{file_format}"
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 复制文件
    shutil.copy2(source_file, output_path)
    
    return output_path

