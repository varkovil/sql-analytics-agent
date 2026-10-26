
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class kalstate(TypedDict):
    question: str
    message: str
    status:str
    
    

def first_node(state: kalstate) -> dict:

    question = state.get("question")
    print(f"Question: {question}")

    return {"question": question}

def accept_node(state: kalstate) -> dict:
   
    print("Question accepted.")
    return {"status": "question read successfully"}

def reject_node(state: kalstate) -> dict:
    print("Question must be at least 10 characters long.")
    return {"status": "question rejected"}



builder= StateGraph(kalstate)

builder.add_node("first_node", first_node)
builder.add_node("accept_node", accept_node)
builder.add_node("reject_node", reject_node)
builder.add_edge(START, "first_node")

builder.add_conditional_edges("first_node", lambda state: "accept_node" if len(state.get("question")) >= 10 else "reject_node")
builder.add_edge("accept_node", END)
builder.add_edge("reject_node", END)

graph = builder.compile()

if __name__ == "__main__":
    initial_state = {"question": "Name?"}
    result = graph.invoke(initial_state)
    print(f"Result: {result}")
