"""
Token Budget Allocator with Graceful Degradation.

Processes agent calls in execution order while ensuring that the
total token budget is never exceeded.
"""


def allocate_budget(calls: list[dict], total_budget: int) -> list[dict]:
    """
    Allocate a fixed token budget across agent calls.

    Each call is processed in order.

    Decision priority:
    1. Full execution
    2. Degraded execution (50% token cost, rounded down)
    3. Skip execution

    Args:
        calls: List of dictionaries containing:
            {
                "agent": str,
                "estimated_tokens": int
            }

        total_budget: Total available token budget.

    Returns:
        List of dictionaries containing:
            {
                "agent": str,
                "decision": "full" | "degraded" | "skipped",
                "tokens_used": int
            }
    """

    remaining_budget = total_budget
    allocation = []

    for call in calls:
        agent = call["agent"]
        estimated_tokens = call["estimated_tokens"]

        if estimated_tokens <= remaining_budget:
            decision = "full"
            tokens_used = estimated_tokens
            remaining_budget = remaining_budget - tokens_used

        else:
            degraded_tokens = estimated_tokens // 2

            if degraded_tokens <= remaining_budget:
                decision = "degraded"
                tokens_used = degraded_tokens
                remaining_budget = remaining_budget - tokens_used
            else:
                decision = "skipped"
                tokens_used = 0

        allocation.append(
            {
                "agent": agent,
                "decision": decision,
                "tokens_used": tokens_used,
            }
        )

    return allocation