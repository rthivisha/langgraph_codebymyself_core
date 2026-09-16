from langgraph.graph import START , END ,StateGraph
from typing_extensions import TypedDict
from typing import Literal, NotRequired
from langchain_google_genai import ChatGoogleGenerativeAI


#state
class State(TypedDict):
    graph_int:NotRequired[int]
    graph_str:str

#declare our model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash" )


#node- we are going to create 3 nodes

def node1(state:State) -> State:
    model_response = model.invoke("RETURN Luke NAME ONLY")

    if (model_response.content == "Luke"):
        return{"graph_int": int("1"),
               "graph_str":state["graph_str"] + "We should with Luke"}
    elif(model_response.content == "zhanglinghe"):
        return {"graph_int": int("2"), "graph_str": state["graph_str"] + "We should with Linghe"}
    else:
        return{"graph_int":int("0"),
               "graph_str" : state["graph_str"]+ "invalid response"}

def node2 (state:State) -> State:
    return {
        "graph_int": int("1"),
        "graph_str": state["graph_str"] + "We go with Luke",
    }


def node3(state: State) -> State:
    return {
        "graph_int": int("2"),
        "graph_str": state["graph_str"] + "We go with zhanglinghe",
    }
    #edge

def chooseedge(state:State) -> Literal["node2","node3",END]:
    if state["graph_int"] == 1 :
        return "node2"
    elif state["graph_int"] == 2 :
        return "node3"
    else:
        return END

#putting all together

builder = StateGraph(State)

builder.add_node("node1",node1)
builder.add_node("node2", node2)
builder.add_node("node3", node3)

builder.add_edge(START , "node1")
builder.add_conditional_edges("node1", chooseedge)
builder.add_edge("node2", END)
builder.add_edge("node3", END)
builder.add_edge("node1", END)


graph = builder.compile()
