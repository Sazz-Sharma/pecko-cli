from __future__ import annotations

from langchain_core.messages import SystemMessage

from pecko.core.model import get_model
from pecko.core.state import AgentState
from pecko.tools.simple_fs import list_files, read_file, write_file


def get_agent_node():
    """
    Returns the main agent node function with tools bound.
    """
    model = get_model()
    tools = [list_files, read_file, write_file]
    model_with_tools = model.bind_tools(tools)
    
    system_prompt = "You are a helpful AI coding assistant named Pecko. You can list, read, and write files."

    def agent_node(state: AgentState):
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    return agent_node, tools