# query.py

from agent3 import responses3




query = "name of the author of this book?"

# Get the retriever object
retriever = responses3(query)

# # Your query
# query = "Name of the author of this book?"

# Invoke the retriever
# result = retriever.invoke(query)

# Print the result
print("Answer:", retriever)
