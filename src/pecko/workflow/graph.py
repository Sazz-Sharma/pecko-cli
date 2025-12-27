from __future__ import annotations

from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

from pecko.agents.agent import get_agent_node
from pecko.core.state import AgentState


def create_graph():
    """
    Constructs the executable graph.
    """
    
    agent_node, tools = get_agent_node()

    workflow = StateGraph(AgentState)
    
   
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))
    
    
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        tools_condition,
    )
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()