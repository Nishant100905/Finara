"""
Financial graph router.
"""

from langgraph.graph import END


def should_continue(state):
    """
    Decide whether another tool call is needed.
    """

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END