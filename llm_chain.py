from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import OLLAMA_MODEL

llm = Ollama(model=OLLAMA_MODEL)

prompt = PromptTemplate.from_template("""
You are an AI Ops assistant. Analyze this Jira ticket and suggest resolution steps.

Issue Key: {key}
Summary: {summary}
Description: {description}
""")

chain = LLMChain(llm=llm, prompt=prompt)

def analyze_ticket(ticket):
    return chain.run(ticket)
