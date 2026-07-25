from collections import Counter


def _count_correct_calls(made: list[str], expected: list[str]) -> int:
    """
    Count correctly matched tool calls while respecting duplicates.
    """
    made_counter = Counter(made)
    expected_counter = Counter(expected)

    return sum(
        min(made_counter[tool], expected_counter[tool])
        for tool in expected_counter
    )


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

    completed_tasks = 0
    total_correct_calls = 0
    total_made_calls = 0
    total_expected_calls = 0

    for case in cases:
        if case["task_completed"]:
            completed_tasks += 1

        made = case["tool_calls_made"]
        expected = case["tool_calls_expected"]

        if not made and not expected:
            pass
        elif not made or not expected:
            total_made_calls += len(made)
            total_expected_calls += len(expected)
        else:
            correct_calls = _count_correct_calls(made, expected)
            total_correct_calls += correct_calls
            total_made_calls += len(made)
            total_expected_calls += len(expected)

    total_cases = len(cases)

    if total_made_calls == 0 and total_expected_calls == 0:
        precision_score = 1.0
        recall_score = 1.0
    elif total_made_calls == 0 or total_expected_calls == 0:
        precision_score = 0.0
        recall_score = 0.0
    else:
        precision_score = total_correct_calls / total_made_calls
        recall_score = total_correct_calls / total_expected_calls

    return {
        "completion_rate": round(completed_tasks / total_cases, 4),
        "tool_call_precision": round(precision_score, 4),
        "tool_call_recall": round(recall_score, 4),
    }