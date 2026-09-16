from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
from typing import Literal


# State
class State(TypedDict):
    city: str
    country: str
    msg:str


# Nodes
def nodemyplace(state: State) -> State:
    """This is the place I'm in"""
    return {"city": state["city"], "country": state["country"]}


def nodeplace1(state: State) -> State:
    """This is the place I'm going to"""
    return {"msg": f"I'm going to paris, france"}


def nodemyplace2(state: State) -> State:
    """This is the place I'm going to"""
    return { "msg":f"I'm going to seoul, South korea"}


# conditional edge


def whichplace(state: State) -> Literal["nodemyplace2", "nodeplace1"]:
    if state["city"] == "Bangalore" and state["country"] == "India":
        return "nodeplace1"
    return "nodemyplace2"
        


# connecting the graph
builder = StateGraph(State)

builder.add_node("nodemyplace", nodemyplace)
builder.add_node("nodeplace1", nodeplace1)
builder.add_node("nodemyplace2", nodemyplace2)

builder.add_edge(START, "nodemyplace")
builder.add_conditional_edges("nodemyplace", whichplace)
builder.add_edge("nodeplace1", END)
builder.add_edge("nodemyplace2", END)

graph = builder.compile()
