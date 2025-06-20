from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
import os

groq_api_key = os.getenv("groq_api_key" )


llm = ChatGroq(groq_api_key = groq_api_key, model_name = "Gemma2-9b-It")

###Chatprompt template
prompt = ChatPromptTemplate.from_template(
    """You are a helpful assistant. Answer the question based on the context provided below. <context>  {context} </context>.I will tip you if you give the answers correctly.
    """ 
)



def responses2(query:str)->str:
    final_prompt = prompt.format(context = query)
    response = llm.invoke(final_prompt)
    return response
