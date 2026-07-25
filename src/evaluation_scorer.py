"""
Multi-Agent Evaluation Scorer.
"""

from collections import Counter


def _count_correct_calls(made: list[str], expected: list[str]) -> int:
    """
    Count correctly matched tool calls while respecting duplicates.
    """
    made_counter = Counter(made)
    expected_counter = Counter(expected)

    correct = 0
    for tool in expected_counter:
        correct += min(made_counter[tool], expected_counter[tool])

    return correct


def score_runs(cases: list[dict]) -> dict:
    """
    Compute aggregate evaluation metrics.

    Returns:
        {
            "completion_rate": float,
            "tool_call_precision": float,
            "tool_call_recall": float
        }
    """

    if not cases:
        return {
            "completion_rate": 0.0,
            "tool_call_precision": 0.0,
            "tool_call_recall": 0.0,
        }

    completed = 0
    precision_sum = 0.0
    recall_sum = 0.0

    for case in cases:

        if case["task_completed"]:
            completed += 1

        made = case["tool_calls_made"]
        expected = case["tool_calls_expected"]

        # Perfect match
        if not made and not expected:
            precision = 1.0
            recall = 1.0

        # One side empty
        elif not made or not expected:
            precision = 0.0
            recall = 0.0

        else:
            correct = _count_correct_calls(made, expected)

            precision = correct / len(made)
            recall = correct / len(expected)

        precision_sum += precision
        recall_sum += recall

    total_cases = len(cases)

    return {
        "completion_rate": round(completed / total_cases, 4),
        "tool_call_precision": round(precision_sum / total_cases, 4),
        "tool_call_recall": round(recall_sum / total_cases, 4),
    }