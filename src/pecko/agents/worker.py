from __future__ import annotations

from langchain_core.messages import SystemMessage

from pecko.core.model import get_model
from pecko.core.state import AgentState
from pecko.tools.simple_fs import list_files, read_file, write_file


def get_worker_node():
    """
    Returns the worker agent node function with full file system tools bound.
    """
    model = get_model()
    
    tools = [list_files, read_file, write_file]
    model_with_tools = model.bind_tools(tools)
    
    system_prompt = (
        "You are a skilled software developer acting as a Worker. "
        "Your goal is to implement the tasks provided by the Planner agent. "
        "You have access to the file system to read, write, and list files. "
        "Follow the plan exactly and write high-quality, working code. "
        "If you need more information, explore the codebase using your tools."
    )

    def worker_node(state: AgentState):
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    return worker_node, tools
