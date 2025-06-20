import google.generativeai as genai
import os

gemini_api_key = os.getenv("gemini_api_key")

# Configure your API key
genai.configure(api_key=gemini_api_key)


model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"

def responses4(query:str)->str:

    response = model.generate_content(query)
    return response

# print(response.text)