def analyze_ticket(ticket):
    # Lazy imports
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import PromptTemplate
    from config import OLLAMA_MODEL
    from rag_utils import retrieve_similar_tickets
    from auto_assign import fetch_all_tickets

    # Initialize model and chain
    llm = OllamaLLM(model=OLLAMA_MODEL)
    prompt = PromptTemplate.from_template("""
    You are an AI assistant helping with Jira tickets.

    Current Ticket:
    Key: {key}
    Summary: {summary}
    Description: {description}

    Here are similar past tickets:
    {context}

    Based on the above, suggest the next steps or resolution approach.
    """)
    chain = prompt | llm

    # Extract current ticket info
    summary = ticket['fields'].get('summary', '')
    description = (
        ticket['fields'].get('description', {})
        .get('content', [{}])[0]
        .get('content', [{}])[0]
        .get('text', '')
    )
    query = summary + " " + description

    # Retrieve and filter similar tickets
    similar_keys = retrieve_similar_tickets(query)
    all_tickets = fetch_all_tickets()
    similar_tickets = [t for t in all_tickets if t['key'] in similar_keys]

    # Build similarity context
    context = ""
    for t in similar_tickets:
        ctx_summary = t['fields'].get('summary', '')
        ctx_description = (
            t['fields'].get('description', {})
            .get('content', [{}])[0]
            .get('content', [{}])[0]
            .get('text', '')
        )
        context += f"\nTicket: {t['key']}\nSummary: {ctx_summary}\nDescription: {ctx_description}\n---"

    # Invoke chain
    return chain.invoke({
        "key": ticket['key'],
        "summary": summary,
        "description": description,
        "context": context
    })

