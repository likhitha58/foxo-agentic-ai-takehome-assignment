# Foxo Agentic AI Takehome Assignment

This project implements two small but practical agent-simulation utilities:

1. A token budget allocator that decides how each agent call should be executed under a limited budget.
2. An evaluation scorer that aggregates quality metrics for completed agent runs.

The code is intentionally simple, readable, and focused on the core logic behind budget allocation and run evaluation.

## Project Overview

The assignment is split into two independent modules:

- [src/budget_allocator.py](src/budget_allocator.py): allocates available tokens across agent calls using a “full → degraded → skipped” decision policy.
- [src/evaluation_scorer.py](src/evaluation_scorer.py): computes aggregate evaluation metrics such as completion rate and tool-call precision/recall.

The repository also includes:

- [tests/test_budget_allocator.py](tests/test_budget_allocator.py): validates budget allocation behavior.
- [tests/test_evaluation_scorer.py](tests/test_evaluation_scorer.py): validates scoring behavior and edge cases.
- [examples](examples): placeholder/example locations for usage scripts.

## File-by-File Explanation

### 1. src/budget_allocator.py

This module contains the function `allocate_budget(calls, total_budget)`.

#### What it does
It processes a list of agent calls in order and assigns each call one of three decisions:

- `full`: the full estimated token amount fits in the remaining budget.
- `degraded`: the full amount does not fit, so the system uses half the estimated tokens (rounded down).
- `skipped`: even the degraded version cannot fit, so the call is skipped.

#### Why this is useful
This models a common real-world behavior in agent systems: when resources are constrained, the system should still try to do something useful rather than failing completely.

#### Logic behind the function
For each call:

1. Read the agent name and its estimated token cost.
2. Compare the cost to the current `remaining_budget`.
3. If the full cost fits, run it fully and reduce the remaining budget.
4. If not, try the degraded version using `estimated_tokens // 2`.
5. If even that does not fit, skip the call.
6. Record the decision and the tokens used in the output list.

#### Important behavior
- The budget is updated after every allocation.
- Calls are handled strictly in input order.
- Degraded execution is rounded down to avoid fractional token usage.

#### Example output
A call with 300 estimated tokens and a remaining budget of 200 will be treated as:

- full if 300 <= 200? No
- degraded if 150 <= 200? Yes

So it becomes a degraded run using 150 tokens.

---

### 2. src/evaluation_scorer.py

This module contains the function `score_runs(cases)`.

#### What it does
It evaluates a batch of completed agent-run cases and returns aggregate metrics:

- `completion_rate`: the fraction of cases where `task_completed` is `True`
- `tool_call_precision`: how often the made tool calls were correct
- `tool_call_recall`: how often the expected tool calls were recovered

#### Why this is useful
These metrics are commonly used to monitor the quality of agent systems over time. A high completion rate means the system finishes tasks successfully, while precision and recall reflect how accurately the system used expected tools.

#### Core helper function
`_count_correct_calls(made, expected)`

This counts how many tool calls were correctly matched while respecting duplicates.

Example:

- made = `["search", "search"]`
- expected = `["search"]`

The function counts one correct match, not two, because duplicates are handled carefully.

#### Logic behind the scoring calculations

##### Completion rate

$$
completion\_rate = \frac{\text{number of completed cases}}{\text{total number of cases}}
$$

##### Precision

Precision measures how many of the made tool calls were correct:

$$
precision = \frac{\text{total correct tool calls}}{\text{total tool calls made}}
$$

##### Recall

Recall measures how many of the expected tool calls were actually captured:

$$
recall = \frac{\text{total correct tool calls}}{\text{total tool calls expected}}
$$

#### Edge-case handling
The implementation carefully handles empty lists:

- If both made and expected are empty, precision and recall are treated as `1.0`.
- If one side is empty and the other is not, precision and recall are treated as `0.0`.
- All returned metrics are rounded to 4 decimal places.

This avoids divide-by-zero errors and makes the metric behavior consistent.

---

## Theory Behind the Calculations

### Budget allocation theory
The budget allocator follows a simple greedy strategy:

- Process calls in the given order.
- Use the available resources as efficiently as possible.
- Prefer a full run when possible.
- If full is impossible, fall back to degraded execution.
- If even degraded is impossible, skip the call.

This is a practical strategy for resource-constrained multi-agent systems because it preserves the order of execution and avoids overspending.

### Evaluation metrics theory
The scorer uses standard information-retrieval-style metrics:

- Precision answers: “Of all the calls the system made, how many were correct?”
- Recall answers: “Of all the calls the system should have made, how many did it actually make?”

These metrics are widely used to evaluate tool selection, action accuracy, and downstream run quality.

---

## How to Run the Project

### 1. Install dependencies
If needed, install the required package list:

```bash
pip install -r requirements.txt
```

### 2. Run tests
Run the full test suite:

```bash
python -m pytest -q
```

Or run the two relevant suites directly:

```bash
python -m pytest -q tests/test_budget_allocator.py tests/test_evaluation_scorer.py
```

### 3. Example usage
You can import the functions directly in Python:

```python
from src.budget_allocator import allocate_budget
from src.evaluation_scorer import score_runs

budget_result = allocate_budget(
    [
        {"agent": "Planner", "estimated_tokens": 300},
        {"agent": "Researcher", "estimated_tokens": 800},
    ],
    900,
)

print(budget_result)

score_result = score_runs(
    [
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
)

print(score_result)
```

---

## Testing Summary

The project uses pytest for validation.

The tests cover:

- full execution when budget is sufficient
- degraded execution when full does not fit
- skipping when neither full nor degraded fit
- empty input handling
- zero-budget behavior
- duplicate-aware call counting
- empty-list edge cases for precision and recall

---

## Summary

This repository demonstrates two core ideas in agent systems:

- Resource-aware execution through budget allocation
- Quality measurement through evaluation scoring

Together, these pieces form a compact framework for reasoning about how agents should behave under constraints and how their performance should be measured over time.
