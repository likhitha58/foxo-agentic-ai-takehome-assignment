# Foxo Agentic AI Take-home Assignment

This repository contains my solutions for the **Foxo Agentic AI Take-home Assignment**.

The assignment consists of two independent problems:

1. **Token Budget Allocator with Graceful Degradation**
2. **Multi-Agent Evaluation Scorer**

Both solutions are implemented in Python with emphasis on clean, readable code, modular design, and comprehensive unit testing.

---

# Repository Structure

```text
foxo-agentic-ai-takehome-assignment/
│
├── src/
│   ├── budget_allocator.py
│   └── evaluation_scorer.py
│
├── tests/
│   ├── test_budget_allocator.py
│   └── test_evaluation_scorer.py
│
├── examples/
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Tech Stack

- Python 3.12
- pytest
- collections.Counter

---

# Problem 1 – Token Budget Allocator with Graceful Degradation

## Objective

Allocate a fixed token budget across a sequence of agent calls while ensuring that the total allocated tokens never exceed the available budget.

Each call is processed in execution order and receives one of three decisions:

- **full** – Execute using the complete estimated token cost.
- **degraded** – Execute using 50% of the estimated token cost (rounded down).
- **skipped** – Skip the call if neither full nor degraded execution fits within the remaining budget.

---

## Implementation

The solution is implemented in:

```text
src/budget_allocator.py
```

The function:

```python
allocate_budget(calls, total_budget)
```

processes every agent call sequentially.

For every call:

1. Read the agent name and estimated token requirement.
2. Check whether the full token requirement fits within the remaining budget.
3. If full execution is not possible, compute the degraded cost using:

```python
estimated_tokens // 2
```

4. If the degraded version fits, allocate the degraded amount.
5. Otherwise, skip the call.
6. Update the remaining budget after every successful allocation.

The allocator never exceeds the available budget and preserves the original execution order.

---

## Example

Input

```python
calls = [
    {"agent": "Planner", "estimated_tokens": 300},
    {"agent": "Researcher", "estimated_tokens": 800},
    {"agent": "Critic", "estimated_tokens": 500},
]

total_budget = 900
```

Output

```python
[
    {"agent": "Planner", "decision": "full", "tokens_used": 300},
    {"agent": "Researcher", "decision": "degraded", "tokens_used": 400},
    {"agent": "Critic", "decision": "skipped", "tokens_used": 0},
]
```

---

# Problem 2 – Multi-Agent Evaluation Scorer

## Objective

Compute aggregate evaluation metrics for a collection of completed agent-run cases.

The implementation returns three metrics:

- Completion Rate
- Tool Call Precision
- Tool Call Recall

All values are rounded to four decimal places.

---

## Implementation

The solution is implemented in:

```text
src/evaluation_scorer.py
```

The main function is:

```python
score_runs(cases)
```

The implementation processes every evaluation case individually.

For each case:

- Determine whether the task was completed.
- Compare the tool calls made against the expected tool calls.
- Compute precision and recall for that individual case.
- Aggregate the metrics across all cases by averaging them.

---

## Duplicate Tool Call Handling

The implementation includes a helper function:

```python
_count_correct_calls(made, expected)
```

This function uses Python's `collections.Counter` to correctly match tool calls while respecting duplicate occurrences.

Example:

```python
made = ["search", "search"]
expected = ["search"]
```

The correct number of matched tool calls is:

```text
1
```

Only one occurrence is counted because only one matching expected call exists.

This prevents duplicate tool calls from being over-counted.

---

## Metric Calculations

### Completion Rate

Calculated as:

```text
Completed Tasks / Total Cases
```

---

### Tool Call Precision

For each evaluation case:

```text
Correct Tool Calls / Tool Calls Made
```

The final precision is the average across all cases.

---

### Tool Call Recall

For each evaluation case:

```text
Correct Tool Calls / Expected Tool Calls
```

The final recall is the average across all cases.

---

## Edge Cases

The implementation handles several special cases safely.

### Empty input

If no evaluation cases are provided:

```python
[]
```

all returned metrics are:

```text
0.0
```

---

### Empty tool-call lists

If both

```python
tool_calls_made
```

and

```python
tool_calls_expected
```

are empty, then

```text
precision = 1.0
recall = 1.0
```

because the agent correctly performed no tool calls.

If only one list is empty, both precision and recall are returned as:

```text
0.0
```

This avoids divide-by-zero errors while matching the required behavior.

---

# Testing

The project uses **pytest** for automated testing.

## Budget Allocator Tests

The test suite validates:

- Sample assignment example
- Full execution
- Degraded execution
- Skipped execution
- Empty input
- Zero budget
- Odd token degradation
- Budget updates after each allocation

---

## Evaluation Scorer Tests

The test suite validates:

- Empty input
- Perfect matches
- Empty tool-call lists
- Empty made calls
- Empty expected calls
- Duplicate-aware tool matching
- Partial matches
- Average metric calculation across multiple evaluation cases

---

# Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
python -m pytest -v
```

Run only the Budget Allocator tests:

```bash
python -m pytest tests/test_budget_allocator.py -v
```

Run only the Evaluation Scorer tests:

```bash
python -m pytest tests/test_evaluation_scorer.py -v
```

---

# Example Usage

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
            "tool_calls_made": ["search", "calculator"],
            "tool_calls_expected": ["search", "calculator"],
        }
    ]
)

print(score_result)
```

---

# Results

- Token Budget Allocator implemented
- Multi-Agent Evaluation Scorer implemented
- 16 automated unit tests
- All tests passing

---

# Notes

The implementation follows the problem specification by:

- Processing budget allocations in execution order.
- Never exceeding the available token budget.
- Supporting graceful degradation through 50% token reduction.
- Computing completion rate, tool-call precision, and tool-call recall.
- Handling duplicate tool calls correctly.
- Handling empty input and empty tool-call edge cases safely.

---

# License

This project was developed as part of the **Foxo Agentic AI Take-home Assignment**.