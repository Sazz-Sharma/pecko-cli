from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    The state of the agent graph.
    """
    messages: Annotated[list[BaseMessage], add_messages]
