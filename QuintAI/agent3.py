###Creating a wrapper around a wikipedia
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


wiki_tool.name

tools = [wiki_tool]

###Agents:choose a language model to choose a sequence of actions to tkae. in chains, a sequence of actions is hardcoded.in agents,a language model is uused as a reasoning engine to determine which actins to take and in which order
from langchain_community.chat_models import ChatOllama
llm= ChatOllama(model="llama3.2")
llm


from langchain import hub
#Get the prompt to use - you can modify this!
# prompt = hub.pull("hwchase17/openai-functions-agent")
prompt = """
You are a helpful assistant. Answer the question based on the context provided below. <context>  {context} </context>.I will tip you if you give the answers correctly.
"""


from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.agents import create_tool_calling_agent


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # Works well with ChatOllama
    verbose=True,
    handle_parsing_errors=True
)

def responses3(query :str)->str:
    response = agent.invoke({"input": query})
    return response                    
# response.pretty_print()
# print(response)