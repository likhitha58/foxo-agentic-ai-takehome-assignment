import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.budget_allocator import allocate_budget

def test_sample_budget_allocation():
    calls = [
        {"agent": "Planner", "estimated_tokens": 300},
        {"agent": "Researcher", "estimated_tokens": 800},
        {"agent": "Critic", "estimated_tokens": 500},
    ]

    result = allocate_budget(calls, 900)

    expected = [
        {
            "agent": "Planner",
            "decision": "full",
            "tokens_used": 300,
        },
        {
            "agent": "Researcher",
            "decision": "degraded",
            "tokens_used": 400,
        },
        {
            "agent": "Critic",
            "decision": "skipped",
            "tokens_used": 0,
        },
    ]

    assert result == expected
    
def test_all_calls_run_full_when_budget_is_sufficient():
    calls = [
        {"agent": "Planner", "estimated_tokens": 100},
        {"agent": "Researcher", "estimated_tokens": 200},
    ]

    result = allocate_budget(calls, 500)

    assert result == [
        {
            "agent": "Planner",
            "decision": "full",
            "tokens_used": 100,
        },
        {
            "agent": "Researcher",
            "decision": "full",
            "tokens_used": 200,
        },
    ]
    
def test_degraded_execution_when_full_does_not_fit():
    calls = [
        {"agent": "Researcher", "estimated_tokens": 800},
    ]

    result = allocate_budget(calls, 400)

    assert result == [
        {
            "agent": "Researcher",
            "decision": "degraded",
            "tokens_used": 400,
        }
    ]
    
def test_call_is_skipped_when_full_and_degraded_fail():
    calls = [
        {"agent": "Critic", "estimated_tokens": 500},
    ]

    result = allocate_budget(calls, 100)

    assert result == [
        {
            "agent": "Critic",
            "decision": "skipped",
            "tokens_used": 0,
        }
    ]
    
def test_empty_calls_returns_empty_list():
    result = allocate_budget([], 1000)

    assert result == []

def test_zero_budget_skips_all_calls():
    calls = [
        {"agent": "Planner", "estimated_tokens": 100},
    ]

    result = allocate_budget(calls, 0)

    assert result == [
        {
            "agent": "Planner",
            "decision": "skipped",
            "tokens_used": 0,
        }
    ]
    
def test_degradation_rounds_down_for_odd_tokens():
    calls = [
        {"agent": "Planner", "estimated_tokens": 101},
    ]

    result = allocate_budget(calls, 50)

    assert result == [
        {
            "agent": "Planner",
            "decision": "degraded",
            "tokens_used": 50,
        }
    ]
    
def test_budget_is_updated_after_each_allocation():
    calls = [
        {"agent": "Agent_A", "estimated_tokens": 400},
        {"agent": "Agent_B", "estimated_tokens": 400},
        {"agent": "Agent_C", "estimated_tokens": 400},
    ]

    result = allocate_budget(calls, 900)

    assert result == [
        {
            "agent": "Agent_A",
            "decision": "full",
            "tokens_used": 400,
        },
        {
            "agent": "Agent_B",
            "decision": "full",
            "tokens_used": 400,
        },
        {
            "agent": "Agent_C",
            "decision": "skipped",
            "tokens_used": 0,
        },
    ]