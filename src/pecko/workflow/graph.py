from __future__ import annotations

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from pecko.agents.agent import get_agent_node
from pecko.agents.planner import get_planner_node
from pecko.agents.worker import get_worker_node
from pecko.agents.reviewer import get_reviewer_node
from pecko.core.state import AgentState


def create_graph():
    """
    Constructs the multi-agent executable graph.
    """
    planner_node, planner_tools = get_planner_node()
    worker_node, worker_tools = get_worker_node()
    reviewer_node, reviewer_tools = get_reviewer_node()

    workflow = StateGraph(AgentState)

    
    workflow.add_node("planner", planner_node)
    workflow.add_node("worker", worker_node)
    workflow.add_node("reviewer", reviewer_node)

   
    workflow.add_node("planner_tools", ToolNode(planner_tools))
    workflow.add_node("worker_tools", ToolNode(worker_tools))
    workflow.add_node("reviewer_tools", ToolNode(reviewer_tools))

    workflow.add_edge(START, "planner")

    workflow.add_conditional_edges(
        "planner",
        tools_condition,
        {"tools": "planner_tools", "__end__": "worker"}
    )
    workflow.add_edge("planner_tools", "planner")

    workflow.add_conditional_edges(
        "worker",
        tools_condition,
        {"tools": "worker_tools", "__end__": "reviewer"}
    )
    workflow.add_edge("worker_tools", "worker")

    workflow.add_conditional_edges(
        "reviewer",
        tools_condition,
        {"tools": "reviewer_tools", "__end__": END}
    )
    workflow.add_edge("reviewer_tools", "reviewer")

    return workflow.compile()

# graph = create_graph()

# png_data = graph.get_graph().draw_mermaid_png()
# with open("graph_output.png", "wb") as f:
#     f.write(png_data)
# print("Graph visualization saved to 'graph_output.png'")

