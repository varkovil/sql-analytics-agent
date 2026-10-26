
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from app.relevance_checker import is_question_relevant
from app.sql_generator import generate_sql_query
from app.sql_validator import validate_sql
from app.sql_executor import execute_sql
from app.sql_corrector import correct_sql
from app.answer_generator import gen_natural_language_explanation

class SQLstate(TypedDict):
    question: str
    sql_query: str
    is_valid: bool
    is_question_relevant: str
    column_names: list
    results: list
    error: str
    explanation: str
    attempt: int
    max_attempts: int



def relevance_check_node(state:SQLstate):
    result = is_question_relevant(state["question"])

    return {
        "is_question_relevant": result
    }

def route_after_relevance_check(state: SQLstate):
    if state.get("is_question_relevant")=='yes':
        return "sql_generator_node"
    else:
        return END   


def sql_generator_node(state:SQLstate):
    sql_query=generate_sql_query(state.get("question"))
    # only for debugging purposes, you can uncomment the following line to simulate an error in the generated SQL
    #sql_query = sql_query.replace("FROM orders","FROM odez")
    return {"sql_query": sql_query}

def sql_validator_node(state: SQLstate):
    attempt = state.get("attempt", 0) + 1
    is_valid = validate_sql(state["sql_query"])
    # only for debugging purposes, you can uncomment the following line to simulate three attempts
    #is_valid=False
    return {
        "is_valid": is_valid,
        "attempt": attempt 
    }

def route_after_validation(state: SQLstate):
    if state.get("is_valid"):
        return "sql_executor_node"
    elif state.get("attempt") < state.get("max_attempts"):
        return "sql_corrector_node"
    else:
        return END

def sql_executor_node(state:SQLstate):
    column_names, results, error= execute_sql(state.get("sql_query"))
    return{
        "column_names":column_names,
        "results":results,
        "error": error
    }

def route_after_execution(state:SQLstate):
  
    if state.get("error")== None:
       return "answer_generator_node"
    return "sql_corrector_node"


def sql_corrector_node(state:SQLstate):
    correction_number = state.get("attempt", 1)
    print(f"\n--- Correction after validation attempt {correction_number} ---")
    print("Attempting to correct SQL...")
    corrected_sql=correct_sql(state.get("question"),state.get("sql_query"),state.get("error"))
    return{
        "sql_query":corrected_sql
    }


def answer_generator_node(state:SQLstate):
    explanation=gen_natural_language_explanation(state.get("column_names"),state.get("results"))
    return{
        "explanation":explanation
    }


builder = StateGraph(SQLstate)

builder.add_node("relevance_check_node", relevance_check_node)
builder.add_node("sql_generator_node", sql_generator_node)
builder.add_node("sql_validator_node", sql_validator_node)
builder.add_node("sql_executor_node", sql_executor_node)
builder.add_node("sql_corrector_node", sql_corrector_node)
builder.add_node("answer_generator_node", answer_generator_node)

builder.add_edge(START, "relevance_check_node")
builder.add_conditional_edges("relevance_check_node", route_after_relevance_check)
builder.add_edge("sql_generator_node", "sql_validator_node")
builder.add_conditional_edges("sql_validator_node", route_after_validation)  
builder.add_conditional_edges("sql_executor_node", route_after_execution)
builder.add_edge("sql_corrector_node", "sql_validator_node")
builder.add_edge("answer_generator_node", END)


graph = builder.compile()

final_state = graph.invoke({
    "question": "give the product wise revenue",
    "sql_query": "",
    "is_valid": False,
    "is_question_relevant": False,
    "column_names": [],
    "results": [],
    "error": "",
    "explanation": "",
    "attempt": 0,
    "max_attempts": 3
})


def printing(state):
    print(f"\nSQL validation attempts: {state.get('attempt', 0)}")
    if state.get("error") is None and state.get("explanation"):
        print("\nColumns:")
        print(state.get("column_names"))
    
        print("\nResults:")
        for row in state.get("results"):
            print(row)
        print("\nExplanation:")
        print(state["explanation"])

    elif state.get("is_question_relevant") == "no":
        print("Sorry, your question is not relevant to the database.")

    else:
        print("Sorry, I couldn't process your question successfully.")


printing(final_state)