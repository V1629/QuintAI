# query.py

from agent5 import retriever_setup



query = "Name of the author of this book?"

# Get the retriever object
retriever = retriever_setup(query)

# Your query
query = "Name of the author of this book?"

# Invoke the retriever
# result = retriever.invoke(query)

# Print the result
print("Answer:", retriever)
