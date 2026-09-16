from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph


# state
class State(TypedDict):
    msg: str


# node
def dict_graphstate(state: State) -> State:
    """This node modifies the msg field in the state"""
    return {"msg": state["msg"] + "I love building stuffs that i learn"}


# connect the graph

builder = StateGraph(State)

builder.add_node("firstnode_dict", dict_graphstate)

builder.add_edge(START, "firstnode_dict")
builder.add_edge("firstnode_dict", END)

graph = builder.compile()

# Uncomment below to test locally:
# res = graph.invoke({"msg": "learning langgraph is cool and fun "})
# print(res["msg"])
