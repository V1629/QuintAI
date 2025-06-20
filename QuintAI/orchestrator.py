from langgraph.graph import StateGraph, END, START
from typing import TypedDict, List, Dict, Any

from agent1 import responses1
from agent2 import responses2
from agent3 import responses3
from agent4 import responses4
from judgellm import responses5  # judge model that ranks agent responses

# Define proper state schema using TypedDict
class AgentState(TypedDict):
    question: str
    responses: List[Dict[str, Any]]
    final_answer: str

# Agents as regular functions (not tool wrappers)
def agent1_node(query: str) -> Dict[str, Any]:
    output = responses1(query)
    return {"agent": "agent1", "output": output}

def agent2_node(query: str) -> Dict[str, Any]:
    output = responses2(query)
    return {"agent": "agent2", "output": output}

def agent3_node(query: str) -> Dict[str, Any]:
    output = responses3(query)
    return {"agent": "agent3", "output": output}

def agent4_node(query: str) -> Dict[str, Any]:
    output = responses4(query)
    return {"agent": "agent4", "output": output}

# Judge node
def judge_node(question: str, responses: List[Dict[str, Any]]) -> str:
    answers = [r["output"] for r in responses]
    final_answer = responses5(question, answers)
    return final_answer

# Wrapper to run flow
def run_flow(query: str):
    responses = []
    for agent_func in [agent1_node, agent2_node, agent3_node, agent4_node]:
        try:
            resp = agent_func(query)
            responses.append(resp)
        except Exception as e:
            responses.append({"agent": agent_func.__name__, "output": f"Error: {e}"})
    final_answer = judge_node(query, responses)
    return final_answer

# CLI entry
if __name__ == "__main__":
    query = input("How can I help you? ")
    answer = run_flow(query)
    print("\n🤖 Final Answer:\n", answer)