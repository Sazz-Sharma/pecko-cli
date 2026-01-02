from __future__ import annotations

from langchain_core.messages import SystemMessage

from pecko.core.model import get_model
from pecko.core.state import AgentState
from pecko.tools.simple_fs import list_files, read_file


def get_reviewer_node():
    """
    Returns the reviewer agent node function with read-only tools bound.
    """
    model = get_model()
    tools = [list_files, read_file]
    model_with_tools = model.bind_tools(tools)
    
    system_prompt = (
        "You are a diligent code reviewer acting as a Reviewer. "
        "Your goal is to review the work done by the Worker agent against the tasks provided by the Planner. "
        "Check for correctness, code quality, and adherence to the plan. "
        "You can use tools to inspect the files. "
        "If there are issues, provide specific feedback. "
        "If the work is satisfactory, confirm that the task is complete."
    )

    def reviewer_node(state: AgentState):
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    return reviewer_node, tools
