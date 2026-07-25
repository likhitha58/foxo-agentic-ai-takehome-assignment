# Foxo Agentic AI Take-home Assignment

This repository contains solutions for the **Foxo Agentic AI Take-home Assignment**, implementing two practical utilities commonly found in agent-based systems:

- **Token Budget Allocator** – Allocates a limited token budget across agent calls using graceful degradation.
- **Multi-Agent Evaluation Scorer** – Computes aggregate metrics to evaluate the quality of agent execution.

The implementation focuses on **clean code, correctness, edge-case handling, and comprehensive unit testing**.

---

# Project Structure

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
│
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

# Project Overview

The project consists of two independent modules.

## 1. Token Budget Allocator

**File:** `src/budget_allocator.py`

### Objective

Allocate a fixed token budget across multiple agent calls while maximizing the number of useful executions.

### Decision Strategy

Each agent call is processed in the given order and assigned one of the following decisions:

- **full** – Execute using the full estimated token count.
- **degraded** – Execute using half of the estimated tokens (`estimated_tokens // 2`).
- **skipped** – Skip the call if neither full nor degraded execution fits within the remaining budget.

### Algorithm

For every agent call:

1. Read the estimated token requirement.
2. Check whether the full execution fits within the remaining budget.
3. If not, attempt degraded execution.
4. If neither fits, skip the call.
5. Update the remaining budget after every successful allocation.

### Key Features

- Greedy allocation strategy
- Budget updated after every allocation
- Calls processed strictly in input order
- Integer-safe degradation using floor division

### Example

Input:

```python
[
    {"agent": "Planner", "estimated_tokens": 300},
    {"agent": "Researcher", "estimated_tokens": 800}
]
```

Budget:

```text
900
```

Output:

```python
[
    {"agent": "Planner", "decision": "full", "tokens_used": 300},
    {"agent": "Researcher", "decision": "degraded", "tokens_used": 400}
]
```

---

# 2. Multi-Agent Evaluation Scorer

**File:** `src/evaluation_scorer.py`

### Objective

Evaluate the performance of multiple agent runs by computing aggregate quality metrics.

### Metrics

The scorer computes:

- **Completion Rate**
- **Tool Call Precision**
- **Tool Call Recall**

### Helper Function

```python
_count_correct_calls(made, expected)
```

Counts correctly matched tool calls while properly handling duplicate tool calls using `collections.Counter`.

Example:

```python
made = ["search", "search"]
expected = ["search"]
```

Correct matches:

```text
1
```

---

### Evaluation Metrics

**Completion Rate**

```text
Completed Tasks / Total Tasks
```

**Tool Call Precision**

```text
Correct Tool Calls / Tool Calls Made
```

**Tool Call Recall**

```text
Correct Tool Calls / Expected Tool Calls
```

### Edge Cases Handled

- Empty input list
- Empty tool-call lists
- Duplicate tool calls
- Division-by-zero prevention
- Metrics rounded to 4 decimal places

---

# Design Approach

## Budget Allocation

The allocator follows a **greedy strategy**.

For every call:

1. Prefer full execution.
2. Otherwise attempt degraded execution.
3. Otherwise skip the call.

This mirrors practical resource allocation used in constrained multi-agent systems.

## Evaluation Scoring

The evaluation module computes aggregate performance using standard information-retrieval metrics.

Duplicate tool calls are matched correctly using `Counter`, preventing over-counting while ensuring accurate precision and recall calculations.

---

# Installation

Clone the repository and install the required dependency.

```bash
pip install -r requirements.txt
```

---

# Running the Tests

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

# Test Coverage

The automated test suite validates:

### Budget Allocator

- Full execution
- Degraded execution
- Skipped execution
- Budget updates after allocation
- Empty inputs
- Zero budget
- Odd-token degradation

### Evaluation Scorer

- Perfect matches
- Duplicate-aware tool matching
- Empty input handling
- Empty tool-call edge cases
- Partial matches
- Average metric calculation across multiple cases

---

# Results

- ✅ Token Budget Allocator implemented
- ✅ Multi-Agent Evaluation Scorer implemented
- ✅ 16 automated unit tests
- ✅ All tests passing

---

# License

This project was developed as part of the **Foxo Agentic AI Take-home Assignment**.