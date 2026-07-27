"""
LangGraph Checkpointer

Development configuration using in-memory checkpoint storage.
Replace with PostgresSaver in production if persistent
conversation checkpoints are required.
"""

from langgraph.checkpoint.memory import InMemorySaver

# Global checkpointer instance
checkpointer = InMemorySaver()