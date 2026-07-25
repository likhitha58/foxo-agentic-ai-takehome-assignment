import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.evaluation_scorer import score_runs


def test_empty_cases():
    assert score_runs([]) == {
        "completion_rate": 0.0,
        "tool_call_precision": 0.0,
        "tool_call_recall": 0.0,
    }


def test_perfect_match():
    cases = [
        {
            "task_completed": True,
            "tool_calls_made": ["search", "calculator"],
            "tool_calls_expected": ["search", "calculator"],
        }
    ]

    assert score_runs(cases) == {
        "completion_rate": 1.0,
        "tool_call_precision": 1.0,
        "tool_call_recall": 1.0,
    }


def test_both_tool_lists_empty():
    cases = [
        {
            "task_completed": True,
            "tool_calls_made": [],
            "tool_calls_expected": [],
        }
    ]

    assert score_runs(cases) == {
        "completion_rate": 1.0,
        "tool_call_precision": 1.0,
        "tool_call_recall": 1.0,
    }


def test_empty_made_calls():
    cases = [
        {
            "task_completed": True,
            "tool_calls_made": [],
            "tool_calls_expected": ["search"],
        }
    ]

    assert score_runs(cases) == {
        "completion_rate": 1.0,
        "tool_call_precision": 0.0,
        "tool_call_recall": 0.0,
    }


def test_empty_expected_calls():
    cases = [
        {
            "task_completed": True,
            "tool_calls_made": ["search"],
            "tool_calls_expected": [],
        }
    ]

    assert score_runs(cases) == {
        "completion_rate": 1.0,
        "tool_call_precision": 0.0,
        "tool_call_recall": 0.0,
    }


def test_duplicate_tool_calls():
    cases = [
        {
            "task_completed": True,
            "tool_calls_made": ["search", "search"],
            "tool_calls_expected": ["search"],
        }
    ]

    assert score_runs(cases) == {
        "completion_rate": 1.0,
        "tool_call_precision": 0.5,
        "tool_call_recall": 1.0,
    }


def test_partial_match():
    cases = [
        {
            "task_completed": True,
            "tool_calls_made": ["search"],
            "tool_calls_expected": ["search", "calculator"],
        }
    ]

    assert score_runs(cases) == {
        "completion_rate": 1.0,
        "tool_call_precision": 1.0,
        "tool_call_recall": 0.5,
    }


def test_average_across_multiple_cases():
    cases = [
        {
            "task_completed": True,
            "tool_calls_made": ["search"],
            "tool_calls_expected": ["search"],
        },
        {
            "task_completed": False,
            "tool_calls_made": [],
            "tool_calls_expected": ["calculator"],
        },
    ]

    assert score_runs(cases) == {
        "completion_rate": 0.5,
        "tool_call_precision": 0.5,
        "tool_call_recall": 0.5,
    }