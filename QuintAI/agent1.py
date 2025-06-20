##Data ingestion
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("A Psycho-Cybernetics__-_Maxwell_Maltz.pdf")
text =loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
texts = text_splitter.split_documents(text)
filtered_chunks = texts[:50]

##Vector embedding
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
embedding = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma.from_documents(filtered_chunks, embedding)

from langchain_community.llms import Ollama
llm = Ollama(model="llama3.2")
llm

##designing prompt template
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("""
                                          Answer the following based on the context provided by filtering answers from the database.Think step by step before providing a detailed answer.I will tip you if you provide a good answer.
                                          <context> {context}</context>"""
                                          )

#chain introduction
from langchain.chains.combine_documents import create_stuff_documents_chain

document_chain = create_stuff_documents_chain(llm=llm,prompt=prompt)

retriever = db.as_retriever()

#now we will combine both retrievr and documnent chain then  it becomes retrieval chain
from langchain.chains import create_retrieval_chain
retrieval_chain = create_retrieval_chain(retriever,document_chain)



def responses1(query : str) -> str:

    response = retrieval_chain.invoke({"input": query})
    return response
 
    


# print(response['answer'])