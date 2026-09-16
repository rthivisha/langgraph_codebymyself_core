from langgraph.graph import  START, END, StateGraph, MessagesState
from typing import  Literal
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI

#tools
@tool
def delivarycost(distance:int) -> str:
    """calculates the delivary cost of orders"""
    try:
        if distance>=50 :
            cost = distance//10 
            return f"The delivary cost is ${cost}"
        else :
            cost = distance//5
            return f"The delivary cost is ${cost}"
    except Exception as e:
        return f"Tool execution failed :{str(e)}"

#tool node
tools_here= [delivarycost]
tool_node = ToolNode(tools_here)
    

#model
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
llm_tools = llm.bind_tools(tools_here)

#node
def find_cost(state:MessagesState) :
    instruction = SystemMessage(content ="you are an financial agent .  execute the user query without tools if possible.")
    full_prompt = [instruction ] + state["messages"]

    response = llm_tools.invoke(full_prompt)
    return {"messages" : [response]}

#edge
def decisionchooser(state:MessagesState)-> Literal["tools","__end__"]:
    last_message= state["messages"][-1]

    """we are checking whether a tool call exist """
    if hasattr(last_message,"tool_calls")and last_message.tool_calls:
        return "tools"
    return "__end__"

#putting together
builder = StateGraph(MessagesState)

builder.add_node("find_cost",find_cost)
builder.add_node("tools",tool_node)

builder.add_edge(START, "find_cost")
builder.add_conditional_edges("find_cost",decisionchooser,{"tools":"tools","__end__":END})

builder.add_edge("tools", "find_cost")


graph = builder.compile()
