from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from typing import TypedDict, List, Dict, Any

from agent1 import responses1
from agent2 import responses2
from agent3 import responses3
from agent4 import responses4
from judgellm import responses5  # judge model that ranks agent responses

### Define proper state schema using TypedDict
class AgentState(TypedDict):
    question: str
    responses: List[Dict[str, Any]]
    final_answer: str

### Agents as regular functions (not tool wrappers)
def agent1_node(state: AgentState) -> Dict[str, Any]:
    query = state["question"]
    output = responses1(query)
    # Return the update to be merged into state
    return {"responses": state["responses"] + [{"agent": "agent1", "output": output}]}

def agent2_node(state: AgentState) -> Dict[str, Any]:
    query = state["question"]
    output = responses2(query)
    return {"responses": state["responses"] + [{"agent": "agent2", "output": output}]}

def agent3_node(state: AgentState) -> Dict[str, Any]:
    query = state["question"]
    output = responses3(query)
    return {"responses": state["responses"] + [{"agent": "agent3", "output": output}]}

def agent4_node(state: AgentState) -> Dict[str, Any]:
    query = state["question"]
    output = responses4(query)
    return {"responses": state["responses"] + [{"agent": "agent4", "output": output}]}

### Judge node
def judge_node(state: AgentState) -> Dict[str, Any]:
    answers = [r["output"] for r in state["responses"]]
    final_answer = responses5(state["question"], answers)
    return {"final_answer": final_answer}

### Flow builder
builder = StateGraph(AgentState)

# Add nodes (not as ToolNodes, just regular nodes)
builder.add_node("agent1", agent1_node)
builder.add_node("agent2", agent2_node)
builder.add_node("agent3", agent3_node)
builder.add_node("agent4", agent4_node)
builder.add_node("judge", judge_node)

# Define flow - parallel execution of agents
builder.add_edge(START, "agent1")
builder.add_edge(START, "agent2")
builder.add_edge(START, "agent3")
builder.add_edge(START, "agent4")

# All agents feed into judge
builder.add_edge("agent1", "judge")
builder.add_edge("agent2", "judge")
builder.add_edge("agent3", "judge")
builder.add_edge("agent4", "judge")

# Judge leads to end
builder.add_edge("judge", END)

### Compile the flow
app = builder.compile()

# Optional: visualize
try:
    from IPython.display import display, Image
    display(Image(app.get_graph().draw_mermaid_png()))
except:
    pass

### Wrapper to run flow
def run_flow(query: str):
    initial_state = {
        "question": query,
        "responses": [],
        "final_answer": ""
    }
    result = app.invoke(initial_state)
    return result["final_answer"]  # Fixed: removed .get and used proper dict access

### CLI entry
if __name__ == "__main__":
    query = input("How can I help you? ")
    answer = run_flow(query)
    print("\n🤖 Final Answer:\n", answer)