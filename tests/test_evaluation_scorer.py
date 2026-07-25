import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.evaluation_scorer import score_runs


def test_score_runs_matches_sample_output():
    cases = [
        {
            "task_completed": True,
            "tool_calls_made": ["search", "search"],
            "tool_calls_expected": ["search"],
        },
        {
            "task_completed": False,
            "tool_calls_made": [],
            "tool_calls_expected": ["search"],
        },
    ]

    assert score_runs(cases) == {
        "completion_rate": 0.5,
        "tool_call_precision": 0.5,
        "tool_call_recall": 0.5,
    }


def test_score_runs_handles_empty_case_lists():
    assert score_runs([]) == {
        "completion_rate": 0.0,
        "tool_call_precision": 0.0,
        "tool_call_recall": 0.0,
    }


def test_score_runs_treats_empty_made_and_expected_as_perfect_match():
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


def test_score_runs_treats_one_empty_side_as_zero():
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