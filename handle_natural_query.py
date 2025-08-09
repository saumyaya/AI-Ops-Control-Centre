from query_bank import QUERY_MAP  # your existing query bank dictionary
from difflib import get_close_matches
from config import OLLAMA_MODEL
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

def handle_natural_query(user_query):
    # 1. Try exact or close match from query bank first
    if user_query.lower() in QUERY_MAP:
        return QUERY_MAP[user_query.lower()]

    # Close match check
    close_matches = get_close_matches(user_query.lower(), QUERY_MAP.keys(), n=1, cutoff=0.8)
    if close_matches:
        return QUERY_MAP[close_matches[0]]

    # 2. Fallback to LLM-to-JQL generation
    print("💡 No match in query bank — using AI to generate JQL...")
    llm = OllamaLLM(model=OLLAMA_MODEL)
    
    prompt = PromptTemplate.from_template("""
    You are a Jira expert. Convert the following natural language query into a valid JQL query.
    Only return the JQL, nothing else.

    Query: {query}
    """)

    chain = prompt | llm
    jql = chain.invoke({"query": user_query}).strip()

    # Basic validation (optional)
    if not jql.lower().startswith(("project =", "status", "assignee", "priority", "created", "updated")):
        print("⚠️ AI generated suspicious JQL, returning None")
        return None

    return jql
