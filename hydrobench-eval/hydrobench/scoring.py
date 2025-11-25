from __future__ import annotations

import json
import re
from dataclasses import dataclass
from itertools import zip_longest
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

try:
    import pandas as pd
except ImportError:
    pd = None  # type: ignore[assignment]

_CHOICE_PATTERN = re.compile(r"[A-Z]")


@dataclass(slots=True, frozen=True)
class ExampleScore:
    example_id: str
    expected: tuple[str, ...]
    predicted: tuple[str, ...]
    is_correct: bool
    missing_prediction: bool
    raw_prediction: Any = None
    metadata: Mapping[str, Any] | None = None


class ScoreReport:
    def __init__(
        self,
        *,
        benchmark_name: str | None,
        example_scores: Sequence[ExampleScore],
    ) -> None:
        self.benchmark_name = benchmark_name
        self.example_scores = list(example_scores)

    # Summary stats ----------------------------------------------------- #
    @property
    def max_score(self) -> int:
        return len(self.example_scores)

    @property
    def total_score(self) -> int:
        return sum(1 for s in self.example_scores if s.is_correct)

    @property
    def accuracy(self) -> float:
        if not self.example_scores:
            return 0.0
        return self.total_score / self.max_score

    def summary(self) -> str:
        name = self.benchmark_name or "Benchmark"
        return (
            f"{name}: {self.total_score}/{self.max_score} "
            f"({self.accuracy:.2%} accuracy)"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "benchmark": self.benchmark_name,
            "total_score": self.total_score,
            "max_score": self.max_score,
            "accuracy": self.accuracy,
            "examples": [
                {
                    "id": s.example_id,
                    "expected": s.expected,
                    "predicted": s.predicted,
                    "is_correct": s.is_correct,
                    "missing_prediction": s.missing_prediction,
                    "metadata": dict(s.metadata or {}),
                    "raw_prediction": s.raw_prediction,
                }
                for s in self.example_scores
            ],
        }

    def to_json(self, *, ensure_ascii: bool = False, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=ensure_ascii, indent=indent)

    def get_category_stats(self, benchmark: Any | None = None) -> dict[str, dict[str, Any]]:
        """
        按类别统计正确率。
        
        Args:
            benchmark: Benchmark 对象，用于获取题目的类别信息
        
        Returns:
            字典，键为类别名称，值为包含统计信息的字典
        """
        category_stats: dict[str, dict[str, int]] = {}
        
        for score in self.example_scores:
            category = None
            if benchmark is not None:
                for ex in benchmark.examples:
                    if ex.id == score.example_id:
                        category = ex.category
                        break
            elif score.metadata:
                category = score.metadata.get("category")
            
            category = str(category) if category else "未知"
            
            if category not in category_stats:
                category_stats[category] = {"total": 0, "correct": 0}
            
            category_stats[category]["total"] += 1
            if score.is_correct:
                category_stats[category]["correct"] += 1
        
        # 计算准确率
        result = {}
        for category, stats in category_stats.items():
            accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0.0
            result[category] = {
                "total": stats["total"],
                "correct": stats["correct"],
                "incorrect": stats["total"] - stats["correct"],
                "accuracy": accuracy,
            }
        
        return result

    def get_level_stats(self, benchmark: Any | None = None) -> dict[str, dict[str, Any]]:
        """
        按难度等级统计正确率。
        
        Args:
            benchmark: Benchmark 对象，用于获取题目的难度信息
        
        Returns:
            字典，键为难度等级，值为包含统计信息的字典
        """
        level_stats: dict[str, dict[str, int]] = {}
        
        for score in self.example_scores:
            level = None
            if benchmark is not None:
                for ex in benchmark.examples:
                    if ex.id == score.example_id:
                        level = ex.level
                        break
            elif score.metadata:
                level = score.metadata.get("level")
            
            level = str(level) if level else "未知"
            
            if level not in level_stats:
                level_stats[level] = {"total": 0, "correct": 0}
            
            level_stats[level]["total"] += 1
            if score.is_correct:
                level_stats[level]["correct"] += 1
        
        # 计算准确率
        result = {}
        for level, stats in level_stats.items():
            accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0.0
            result[level] = {
                "total": stats["total"],
                "correct": stats["correct"],
                "incorrect": stats["total"] - stats["correct"],
                "accuracy": accuracy,
            }
        
        return result

    def get_type_stats(self, benchmark: Any | None = None) -> dict[str, dict[str, Any]]:
        """
        按题型统计正确率。
        
        Args:
            benchmark: Benchmark 对象，用于获取题目的题型信息
        
        Returns:
            字典，键为题型名称，值为包含统计信息的字典
        """
        type_stats: dict[str, dict[str, int]] = {}
        
        for score in self.example_scores:
            qtype = None
            if benchmark is not None:
                for ex in benchmark.examples:
                    if ex.id == score.example_id:
                        qtype = ex.question_type
                        break
            elif score.metadata:
                qtype = score.metadata.get("type")
            
            qtype = str(qtype) if qtype else "未知"
            
            if qtype not in type_stats:
                type_stats[qtype] = {"total": 0, "correct": 0}
            
            type_stats[qtype]["total"] += 1
            if score.is_correct:
                type_stats[qtype]["correct"] += 1
        
        # 计算准确率
        result = {}
        for qtype, stats in type_stats.items():
            accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0.0
            result[qtype] = {
                "total": stats["total"],
                "correct": stats["correct"],
                "incorrect": stats["total"] - stats["correct"],
                "accuracy": accuracy,
            }
        
        return result

    def to_csv(
        self,
        output_path: str | Path,
        *,
        benchmark: Any | None = None,
    ) -> Path:
        """
        导出为 CSV 格式，包含题目、正确答案、模型答案等详细信息。
        
        Args:
            output_path: 输出文件路径
            benchmark: 可选的 Benchmark 对象，用于获取题目内容等详细信息
        
        Returns:
            输出文件路径
        """
        if pd is None:
            raise ImportError(
                "pandas is required for CSV export. Install it with: pip install pandas"
            )
        
        output_path = Path(output_path)
        
        # 构建数据行（与 to_excel 相同）
        rows = []
        for score in self.example_scores:
            # 获取题目内容（如果有 benchmark）
            question_text = ""
            category = None
            level = None
            question_type = None
            
            if benchmark is not None:
                # 从 benchmark 中查找对应的题目
                example = None
                for ex in benchmark.examples:
                    if ex.id == score.example_id:
                        example = ex
                        break
                
                if example:
                    question_text = example.input_text
                    category = example.category
                    level = example.level
                    question_type = example.question_type
            
            # 格式化答案
            expected_str = ",".join(sorted(score.expected)) if score.expected else "(无)"
            
            # 显示原始输入值，如果缺失则显示"(缺失)"
            if score.missing_prediction:
                predicted_str = "(缺失)"
            elif score.predicted:
                # 如果能解析出有效答案，显示解析后的答案
                predicted_str = ",".join(sorted(score.predicted))
            else:
                # 如果无法解析但原始值存在，直接显示原始值
                if score.raw_prediction is not None:
                    # 显示原始输入值
                    if isinstance(score.raw_prediction, str):
                        predicted_str = score.raw_prediction
                    else:
                        predicted_str = str(score.raw_prediction)
                else:
                    predicted_str = "(缺失)"
            
            rows.append({
                "ID": score.example_id,
                "Question": question_text,
                "Category": category or "",
                "Level": level or "",
                "Type": question_type or "",
                "Correct Answer": expected_str,
                "Model Answer": predicted_str,
                "Is Correct": "✓" if score.is_correct else "✗",
                "Status": "Correct" if score.is_correct else ("Missing" if score.missing_prediction else "Incorrect"),
            })
        
        # 创建 DataFrame 并保存为 CSV
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False, encoding="utf-8-sig")  # 使用 utf-8-sig 以便 Excel 正确打开
        
        return output_path

    def to_excel(
        self,
        output_path: str | Path,
        *,
        benchmark: Any | None = None,
    ) -> Path:
        """
        导出为 Excel 格式，包含题目、正确答案、模型答案等详细信息。
        
        Args:
            output_path: 输出文件路径
            benchmark: 可选的 Benchmark 对象，用于获取题目内容等详细信息
        
        Returns:
            输出文件路径
        """
        if pd is None:
            raise ImportError(
                "pandas is required for Excel export. Install it with: pip install pandas openpyxl"
            )
        
        output_path = Path(output_path)
        
        # 构建数据行
        rows = []
        for score in self.example_scores:
            # 获取题目内容（如果有 benchmark）
            question_text = ""
            category = None
            level = None
            question_type = None
            
            if benchmark is not None:
                # 从 benchmark 中查找对应的题目
                example = None
                for ex in benchmark.examples:
                    if ex.id == score.example_id:
                        example = ex
                        break
                
                if example:
                    question_text = example.input_text
                    category = example.category
                    level = example.level
                    question_type = example.question_type
            
            # 格式化答案
            expected_str = ",".join(sorted(score.expected)) if score.expected else "(无)"
            
            # 显示原始输入值，如果缺失则显示"(缺失)"
            if score.missing_prediction:
                predicted_str = "(缺失)"
            elif score.predicted:
                # 如果能解析出有效答案，显示解析后的答案
                predicted_str = ",".join(sorted(score.predicted))
            else:
                # 如果无法解析但原始值存在，直接显示原始值
                if score.raw_prediction is not None:
                    # 显示原始输入值
                    if isinstance(score.raw_prediction, str):
                        predicted_str = score.raw_prediction
                    else:
                        predicted_str = str(score.raw_prediction)
                else:
                    predicted_str = "(缺失)"
            
            rows.append({
                "ID": score.example_id,
                "Question": question_text,
                "Category": category or "",
                "Level": level or "",
                "Type": question_type or "",
                "Correct Answer": expected_str,
                "Model Answer": predicted_str,
                "Is Correct": "✓" if score.is_correct else "✗",
                "Status": "Correct" if score.is_correct else ("Missing" if score.missing_prediction else "Incorrect"),
            })
        
        # 创建 DataFrame
        df = pd.DataFrame(rows)
        
        # 写入 Excel
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Evaluation Results", index=False)
            
            # 设置列宽
            worksheet = writer.sheets["Evaluation Results"]
            worksheet.column_dimensions["A"].width = 15  # ID
            worksheet.column_dimensions["B"].width = 50  # Question
            worksheet.column_dimensions["C"].width = 15  # Category
            worksheet.column_dimensions["D"].width = 12  # Level
            worksheet.column_dimensions["E"].width = 12  # Type
            worksheet.column_dimensions["F"].width = 15  # Correct Answer
            worksheet.column_dimensions["G"].width = 15  # Model Answer
            worksheet.column_dimensions["H"].width = 10  # Is Correct
            worksheet.column_dimensions["I"].width = 10  # Status
            
            # 添加汇总信息
            summary_row = len(df) + 3
            worksheet.cell(summary_row, 1, "Summary")
            worksheet.cell(summary_row + 1, 1, "Benchmark: hydrobench")
            worksheet.cell(summary_row + 2, 1, f"Total Questions: {self.max_score}")
            worksheet.cell(summary_row + 3, 1, f"Correct: {self.total_score}")
            worksheet.cell(summary_row + 4, 1, f"Incorrect: {self.max_score - self.total_score}")
            worksheet.cell(summary_row + 5, 1, f"Accuracy: {self.accuracy:.2%}")
            
            # 添加按类别统计的工作表
            category_stats = self.get_category_stats(benchmark)
            if category_stats:
                category_rows = []
                for category, stats in sorted(category_stats.items()):
                    category_rows.append({
                        "Category": category,
                        "Total": stats["total"],
                        "Correct": stats["correct"],
                        "Incorrect": stats["incorrect"],
                        "Accuracy": f"{stats['accuracy']:.2%}",
                    })
                
                category_df = pd.DataFrame(category_rows)
                # Excel 工作表名称限制为31个字符
                sheet_name = "By Category"[:31]
                category_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # 设置列宽
                cat_worksheet = writer.sheets[sheet_name]
                cat_worksheet.column_dimensions["A"].width = 30
                cat_worksheet.column_dimensions["B"].width = 12
                cat_worksheet.column_dimensions["C"].width = 12
                cat_worksheet.column_dimensions["D"].width = 12
                cat_worksheet.column_dimensions["E"].width = 12
                
                # 添加汇总信息
                summary_row = len(category_df) + 3
                cat_worksheet.cell(summary_row, 1, "Summary")
                cat_worksheet.cell(summary_row + 1, 1, f"Total Categories: {len(category_stats)}")
                total_questions = sum(s["total"] for s in category_stats.values())
                total_correct = sum(s["correct"] for s in category_stats.values())
                cat_worksheet.cell(summary_row + 2, 1, f"Total Questions: {total_questions}")
                cat_worksheet.cell(summary_row + 3, 1, f"Total Correct: {total_correct}")
                if total_questions > 0:
                    overall_acc = total_correct / total_questions
                    cat_worksheet.cell(summary_row + 4, 1, f"Overall Accuracy: {overall_acc:.2%}")
            
            # 添加按难度统计的工作表
            level_stats = self.get_level_stats(benchmark)
            if level_stats:
                level_rows = []
                for level, stats in sorted(level_stats.items()):
                    level_rows.append({
                        "Level": level,
                        "Total": stats["total"],
                        "Correct": stats["correct"],
                        "Incorrect": stats["incorrect"],
                        "Accuracy": f"{stats['accuracy']:.2%}",
                    })
                
                level_df = pd.DataFrame(level_rows)
                # Excel 工作表名称限制为31个字符
                sheet_name = "By Level"[:31]
                level_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # 设置列宽
                level_worksheet = writer.sheets[sheet_name]
                level_worksheet.column_dimensions["A"].width = 30
                level_worksheet.column_dimensions["B"].width = 12
                level_worksheet.column_dimensions["C"].width = 12
                level_worksheet.column_dimensions["D"].width = 12
                level_worksheet.column_dimensions["E"].width = 12
                
                # 添加汇总信息
                summary_row = len(level_df) + 3
                level_worksheet.cell(summary_row, 1, "Summary")
                level_worksheet.cell(summary_row + 1, 1, f"Total Levels: {len(level_stats)}")
                total_questions = sum(s["total"] for s in level_stats.values())
                total_correct = sum(s["correct"] for s in level_stats.values())
                level_worksheet.cell(summary_row + 2, 1, f"Total Questions: {total_questions}")
                level_worksheet.cell(summary_row + 3, 1, f"Total Correct: {total_correct}")
                if total_questions > 0:
                    overall_acc = total_correct / total_questions
                    level_worksheet.cell(summary_row + 4, 1, f"Overall Accuracy: {overall_acc:.2%}")
            
            # 添加按题型统计的工作表
            type_stats = self.get_type_stats(benchmark)
            if type_stats:
                type_rows = []
                for qtype, stats in sorted(type_stats.items()):
                    type_rows.append({
                        "Type": qtype,
                        "Total": stats["total"],
                        "Correct": stats["correct"],
                        "Incorrect": stats["incorrect"],
                        "Accuracy": f"{stats['accuracy']:.2%}",
                    })
                
                type_df = pd.DataFrame(type_rows)
                sheet_name = "By Type"[:31]
                type_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # 设置列宽
                type_worksheet = writer.sheets[sheet_name]
                type_worksheet.column_dimensions["A"].width = 30
                type_worksheet.column_dimensions["B"].width = 12
                type_worksheet.column_dimensions["C"].width = 12
                type_worksheet.column_dimensions["D"].width = 12
                type_worksheet.column_dimensions["E"].width = 12
                
                # 添加汇总信息
                summary_row = len(type_df) + 3
                type_worksheet.cell(summary_row, 1, "Summary")
                type_worksheet.cell(summary_row + 1, 1, f"Total Types: {len(type_stats)}")
                total_questions = sum(s["total"] for s in type_stats.values())
                total_correct = sum(s["correct"] for s in type_stats.values())
                type_worksheet.cell(summary_row + 2, 1, f"Total Questions: {total_questions}")
                type_worksheet.cell(summary_row + 3, 1, f"Total Correct: {total_correct}")
                if total_questions > 0:
                    overall_acc = total_correct / total_questions
                    type_worksheet.cell(summary_row + 4, 1, f"Overall Accuracy: {overall_acc:.2%}")
        
        return output_path

    def to_markdown(
        self,
        output_path: str | Path | None = None,
        *,
        benchmark: Any | None = None,
        max_rows: int | None = None,
    ) -> str:
        """
        导出为 Markdown 表格格式，便于查看和分享。
        
        Args:
            output_path: 可选的输出文件路径，如果不提供则只返回字符串
            benchmark: 可选的 Benchmark 对象，用于获取题目内容等详细信息
            max_rows: 最大显示行数，None 表示显示全部
        
        Returns:
            Markdown 格式的字符串
        """
        lines = []
        
        # 标题
        lines.append(f"# {self.benchmark_name or '评估报告'}")
        lines.append("")
        lines.append(f"**总分**: {self.total_score}/{self.max_score} ({self.accuracy:.2%})")
        lines.append("")
        
        # 表格头部
        headers = ["ID", "题目", "类别", "难度", "正确答案", "模型答案", "结果"]
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        
        # 表格内容
        scores_to_show = self.example_scores[:max_rows] if max_rows else self.example_scores
        for score in scores_to_show:
            # 获取题目内容
            question_text = ""
            category = ""
            level = ""
            
            if benchmark is not None:
                example = None
                for ex in benchmark.examples:
                    if ex.id == score.example_id:
                        example = ex
                        break
                
                if example:
                    # 截断过长的题目
                    question_text = example.input_text[:50] + "..." if len(example.input_text) > 50 else example.input_text
                    category = str(example.category) if example.category else ""
                    level = str(example.level) if example.level else ""
            
            # 格式化答案
            expected_str = ",".join(sorted(score.expected)) if score.expected else "(无)"
            predicted_str = ",".join(sorted(score.predicted)) if score.predicted else "(缺失)"
            
            # 结果标记
            result = "✓ 正确" if score.is_correct else ("✗ 缺失" if score.missing_prediction else "✗ 错误")
            
            row = [
                score.example_id,
                question_text or "-",
                category or "-",
                level or "-",
                expected_str,
                predicted_str,
                result,
            ]
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
        
        if max_rows and len(self.example_scores) > max_rows:
            lines.append("")
            lines.append(f"*（仅显示前 {max_rows} 条，共 {len(self.example_scores)} 条）*")
        
        markdown_text = "\n".join(lines)
        
        # 如果提供了输出路径，写入文件
        if output_path:
            Path(output_path).write_text(markdown_text, encoding="utf-8")
        
        return markdown_text


# ---------------------------------------------------------------------- #
# Public scoring helpers
# ---------------------------------------------------------------------- #
def score_examples(
    examples: Sequence[Any],
    predictions: Any,
    *,
    benchmark_name: str | None = None,
) -> ScoreReport:
    normalized_predictions, is_mapping = _normalize_prediction_input(predictions)

    scores: list[ExampleScore] = []
    if is_mapping:
        mapping: Mapping[str, Any] = normalized_predictions  # type: ignore[assignment]
        for example in examples:
            raw_prediction = mapping.get(example.id)
            predicted = _normalize_answer(raw_prediction)
            expected = tuple(example.correct_options)
            is_correct = set(predicted) == set(expected) and bool(expected)
            scores.append(
                ExampleScore(
                    example_id=example.id,
                    expected=expected,
                    predicted=predicted,
                    is_correct=is_correct,
                    missing_prediction=raw_prediction is None,
                    raw_prediction=raw_prediction,
                    metadata=getattr(example, "metadata", None),
                )
            )
    else:
        seq: Sequence[Any] = normalized_predictions  # type: ignore[assignment]
        seq_len = len(seq)
        for idx, example in enumerate(examples):
            raw_prediction = seq[idx] if idx < seq_len else None
            predicted = _normalize_answer(raw_prediction)
            expected = tuple(example.correct_options)
            is_correct = set(predicted) == set(expected) and bool(expected)
            scores.append(
                ExampleScore(
                    example_id=example.id,
                    expected=expected,
                    predicted=predicted,
                    is_correct=is_correct,
                    missing_prediction=raw_prediction is None,
                    raw_prediction=raw_prediction,
                    metadata=getattr(example, "metadata", None),
                )
            )

    return ScoreReport(benchmark_name=benchmark_name, example_scores=scores)


# ---------------------------------------------------------------------- #
# Helpers
# ---------------------------------------------------------------------- #
def _normalize_prediction_input(predictions: Any) -> tuple[Any, bool]:
    if isinstance(predictions, Mapping):
        return predictions, True

    if isinstance(predictions, Sequence) and not isinstance(predictions, (str, bytes)):
        seq = list(predictions)
        if seq and isinstance(seq[0], Mapping):
            mapping: dict[str, Any] = {}
            for item in seq:
                if not isinstance(item, Mapping):
                    raise TypeError("Prediction list must be uniform")
                if "id" not in item:
                    raise KeyError("Prediction entry missing 'id'")
                mapping[str(item["id"])] = item.get("answer") or item.get("choices") or item.get(
                    "prediction"
                )
            return mapping, True
        return seq, False

    raise TypeError(
        "Predictions must be a mapping of {question_id: answer} or a "
        "sequence following the benchmark order."
    )


def _normalize_answer(raw: Any) -> tuple[str, ...]:
    if raw is None:
        return tuple()

    if isinstance(raw, str):
        return tuple(dict.fromkeys(_CHOICE_PATTERN.findall(raw.upper())))

    if isinstance(raw, Sequence) and not isinstance(raw, (str, bytes)):
        letters: list[str] = []
        for item in raw:
            letters.extend(_normalize_answer(item))
        return tuple(dict.fromkeys(letters))

    if isinstance(raw, Mapping):
        for key in ("answer", "answers", "choices", "prediction", "output"):
            if key in raw:
                return _normalize_answer(raw[key])
        return tuple()

    return tuple(dict.fromkeys(_CHOICE_PATTERN.findall(str(raw).upper())))

