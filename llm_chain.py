from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from config import OLLAMA_MODEL

# Load the local model (like "mistral")
llm = OllamaLLM(model=OLLAMA_MODEL)

# Define the prompt
prompt = PromptTemplate.from_template("""
You are an AI Ops assistant. Analyze this Jira ticket and suggest resolution steps.

Issue Key: {key}
Summary: {summary}
Description: {description}
""")

# Combine using new syntax
chain = prompt | llm

# Use .invoke instead of .run
def analyze_ticket(ticket):
    return chain.invoke(ticket)
