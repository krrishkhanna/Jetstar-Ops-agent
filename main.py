from dotenv import load_dotenv
from agent import build_graph

load_dotenv()

def run_query(query: str) -> str:
    app = build_graph()
    initial_state = {
        "query": query,
        "messages": [],
        "tool_to_call": "",
        "tool_result": "",
        "final_answer": "",
        "iteration": 0,
    }
    result = app.invoke(initial_state)
    return result["final_answer"] or "Sorry, I could not process that request."

if __name__ == "__main__":
    print("Starting Jetstar Operations Agent...\n")
    test_queries = [
        "What is the status of Jetstar flight JQ202?",
        "My flight JQ303 was cancelled. What are my rebooking options?",
        "Can you check the travel credits for passenger JS003?",
    ]
    for query in test_queries:
        print(f"\nPassenger: {query}")
        answer = run_query(query)
        print(f"Agent:     {answer}")
        print("-" * 65)
