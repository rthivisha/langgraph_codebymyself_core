# import libraries
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


# state
class State(TypedDict):
    message: str


# node
def graphtypes_langgraph(state: State) -> State:
    return {
        "message": f"This is simple stategraph with one node and two edges and {state['message']}"
    }


# edges


# building the workflow - connection of nodes, edges and state

builder = StateGraph(State)

builder.add_node("firstnode", graphtypes_langgraph)

builder.add_edge(START, "firstnode")
builder.add_edge("firstnode", END)

graph = builder.compile()

# print(graph.invoke({"message": "I'm learning and building stuffs here"}))
