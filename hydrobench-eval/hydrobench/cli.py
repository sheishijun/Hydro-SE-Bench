from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .benchmark import Benchmark
from .datasets import BUILTIN_BENCHMARKS, download_hydrobench_data, load_builtin_benchmark
from .excel_loader import load_benchmark_from_file, load_predictions_from_excel
from .batch_evaluate import evaluate_all_models


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hydrobench",
        description="Score model predictions on the HydroBench benchmark.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    eval_parser = subparsers.add_parser("evaluate", help="Score a predictions file")
    eval_parser.add_argument(
        "--benchmark",
        choices=sorted(BUILTIN_BENCHMARKS),
        help="Use a bundled benchmark (hydrobench).",
    )
    eval_parser.add_argument(
        "--benchmark-path",
        type=Path,
        help="Path to a benchmark JSON or Excel file (overrides --benchmark).",
    )
    eval_parser.add_argument(
        "--benchmark-excel",
        type=Path,
        help="Path to a benchmark CSV or Excel file (alternative to --benchmark-path).",
    )
    eval_parser.add_argument(
        "--predictions",
        type=Path,
        required=True,
        help="JSON, CSV, or Excel file containing model outputs.",
    )
    eval_parser.add_argument(
        "--predictions-id-col",
        type=str,
        default="ID",
        help="Column name for question IDs in predictions Excel. If not specified and Excel has 'ID' column, will use it. Set to empty string to disable ID matching and use row order instead.",
    )
    eval_parser.add_argument(
        "--predictions-answer-col",
        type=str,
        default="Answer",
        help="Column name for answers in predictions Excel (default: Answer).",
    )
    eval_parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write a report. Supports .json, .csv, .xlsx, and .md formats.",
    )
    eval_parser.add_argument(
        "--output-format",
        choices=["json", "csv", "xlsx", "md", "auto"],
        default="auto",
        help="Output format. 'auto' detects from file extension (default: auto).",
    )
    eval_parser.add_argument(
        "--show-details",
        action="store_true",
        help="Print per-question correctness to stdout.",
    )

    # 批量评估命令
    batch_parser = subparsers.add_parser(
        "batch-evaluate",
        help="Batch evaluate multiple models from an Excel file",
    )
    batch_parser.add_argument(
        "--excel",
        type=Path,
        required=True,
        help="CSV or Excel file containing predictions from multiple models.",
    )
    batch_parser.add_argument(
        "--benchmark",
        choices=sorted(BUILTIN_BENCHMARKS),
        default="hydrobench",
        help="Use a bundled benchmark (default: hydrobench).",
    )
    batch_parser.add_argument(
        "--benchmark-path",
        type=Path,
        help="Path to a benchmark JSON or Excel file (overrides --benchmark).",
    )
    batch_parser.add_argument(
        "--id-col",
        type=str,
        help="Column name for question IDs (default: auto-detect).",
    )
    batch_parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory to save detailed reports (default: same as Excel file directory).",
    )
    batch_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output.",
    )

    # 下载命令
    download_parser = subparsers.add_parser(
        "download",
        help="Download hydrobench data files (JSON or Excel)",
    )
    download_parser.add_argument(
        "--format",
        choices=["json", "csv", "xlsx", "all"],
        default="all",
        help="File format to download: json, csv, xlsx, or all (default: all)",
    )
    download_parser.add_argument(
        "--output",
        type=Path,
        help="Output directory or file path. If directory, files will be saved there. If file path, only single format can be specified. Default: current directory",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "evaluate":
        benchmark = _load_benchmark(args)
        predictions_payload = _load_predictions(args)

        report = benchmark.score(predictions_payload)
        print(report.summary())

        if args.show_details:
            for score in report.example_scores:
                status = "✓" if score.is_correct else "✗"
                print(f"{status} {score.example_id}: expected {score.expected}, predicted {score.predicted}")

        if args.output:
            output_path = Path(args.output)
            output_format = args.output_format
            
            # 自动检测格式
            if output_format == "auto":
                ext = output_path.suffix.lower()
                if ext == ".csv":
                    output_format = "csv"
                elif ext == ".xlsx":
                    output_format = "xlsx"
                elif ext == ".md" or ext == ".markdown":
                    output_format = "md"
                else:
                    output_format = "json"
            
            # 导出报告
            if output_format == "csv":
                report.to_csv(output_path, benchmark=benchmark)
                print(f"CSV 报告已保存到: {output_path}")
            elif output_format == "xlsx":
                report.to_excel(output_path, benchmark=benchmark)
                print(f"Excel 报告已保存到: {output_path}")
            elif output_format == "md":
                report.to_markdown(output_path, benchmark=benchmark)
                print(f"Markdown 报告已保存到: {output_path}")
            else:
                output_path.write_text(report.to_json(), encoding="utf-8")
                print(f"JSON 报告已保存到: {output_path}")

        return 0

    elif args.command == "batch-evaluate":
        # 加载 benchmark
        if args.benchmark_path:
            path = args.benchmark_path
            if path.suffix.lower() in (".xlsx", ".xls", ".excel"):
                benchmark = load_benchmark_from_file(path)
            else:
                benchmark = Benchmark.from_file(path)
        else:
            benchmark = load_builtin_benchmark(args.benchmark)

        # 确定输出目录
        output_dir = args.output_dir
        if output_dir is None:
            output_dir = args.excel.parent

        # 执行批量评估
        evaluate_all_models(
            args.excel,
            benchmark=benchmark,
            id_col=args.id_col,
            output_dir=output_dir,
            verbose=not args.quiet,
        )

        return 0

    elif args.command == "download":
        # 确定输出路径
        if args.output is None:
            output_path = Path.cwd()
        else:
            output_path = Path(args.output)

        # 如果输出路径是文件，则只支持单个格式
        if output_path.is_file() or (args.format != "all" and output_path.suffix):
            if args.format == "all":
                raise SystemExit(
                    "Cannot download all formats to a single file. "
                    "Please specify --format json, --format csv, or --format xlsx, or use a directory path."
                )
            # 下载到指定文件路径
            downloaded_path = download_hydrobench_data(args.format, output_path)
            print(f"文件已下载到: {downloaded_path}")
        else:
            # 输出路径是目录
            output_path.mkdir(parents=True, exist_ok=True)
            
            if args.format in ("json", "all"):
                json_path = download_hydrobench_data("json", output_path / "hydrobench.json")
                print(f"JSON 文件已下载到: {json_path}")
            
            if args.format in ("csv", "all"):
                csv_path = download_hydrobench_data("csv", output_path / "hydrobench.csv")
                print(f"CSV 文件已下载到: {csv_path}")
            
            if args.format in ("xlsx", "all"):
                xlsx_path = download_hydrobench_data("xlsx", output_path / "hydrobench.xlsx")
                print(f"Excel 文件已下载到: {xlsx_path}")

        return 0

    else:  # pragma: no cover - future-proof
        parser.error("Unknown command")
        return 1


def _load_benchmark(args: argparse.Namespace) -> Benchmark:
    if args.benchmark_excel:
        return load_benchmark_from_file(args.benchmark_excel)
    if args.benchmark_path:
        path = args.benchmark_path
        if path.suffix.lower() in (".csv", ".xlsx", ".xls", ".excel"):
            return load_benchmark_from_file(path)
        return Benchmark.from_file(path)
    if args.benchmark:
        return load_builtin_benchmark(args.benchmark)
    raise SystemExit("Please provide --benchmark, --benchmark-path, or --benchmark-excel")


def _load_predictions(args: argparse.Namespace) -> Any:
    path = args.predictions
    if path.suffix.lower() in (".csv", ".xlsx", ".xls", ".excel"):
        # 如果指定了 id_col 为空字符串，则使用 None（按行顺序）
        id_col = args.predictions_id_col if args.predictions_id_col else None
        # 如果 id_col 是 "ID" 但 Excel 中没有该列，自动降级为 None（按行顺序）
        if id_col == "ID":
            import pandas as pd
            try:
                df = pd.read_excel(path, nrows=0)  # 只读取列名
                if "ID" not in df.columns:
                    id_col = None
            except Exception:
                pass  # 如果读取失败，继续使用 "ID"
        
        return load_predictions_from_excel(
            path,
            id_col=id_col,
            answer_col=args.predictions_answer_col,
        )
    # JSON file
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:  # pragma: no cover - user input
        raise SystemExit(f"无法解析预测文件 {path}: {exc}") from exc

