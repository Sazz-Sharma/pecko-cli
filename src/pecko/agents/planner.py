from __future__ import annotations

from langchain_core.messages import SystemMessage

from pecko.core.model import get_model
from pecko.core.state import AgentState
from pecko.tools.simple_fs import list_files, read_file


def get_planner_node():
    """
    Returns the planner agent node function with read-only tools bound.
    """
    model = get_model()
    # Planner needs to see the file structure and content to plan effectively
    tools = [list_files, read_file]
    model_with_tools = model.bind_tools(tools)
    
    system_prompt = (
        "You are a senior software architect acting as a Planner. "
        "Your goal is to analyze the user's request and the current codebase state, "
        "then create a detailed, step-by-step plan for the Worker agent to implement. "
        "Do not write the implementation code yourself. "
        "Focus on breaking down the problem into clear, actionable tasks. "
        "You can use tools to explore the codebase before making a plan."
    )

    def planner_node(state: AgentState):
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    return planner_node, tools
