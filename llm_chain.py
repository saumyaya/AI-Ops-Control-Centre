def safe_get_description(desc):
    """Safely extract Jira ticket description as plain text."""
    if not isinstance(desc, dict):
        return ""
    try:
        return (
            desc.get('content', [{}])[0]
            .get('content', [{}])[0]
            .get('text', '')
        )
    except (AttributeError, IndexError, KeyError):
        return ""


def analyze_ticket(ticket):
    # Handle flattened tickets from CLI/UI
    if 'raw' in ticket:  
        ticket = ticket['raw']

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

    # Extract ticket details safely
    fields = ticket.get('fields', {})
    summary = fields.get('summary', ticket.get('summary', ''))

    if 'fields' in ticket:  # Jira API format
        description = safe_get_description(fields.get('description'))
    else:  # Flattened format
        description = ticket.get('description', '')

    query = f"{summary} {description}".strip()

    # Retrieve and filter similar tickets
    similar_keys = retrieve_similar_tickets(query)
    all_tickets = fetch_all_tickets()
    similar_tickets = [t for t in all_tickets if t['key'] in similar_keys]

    # Build similarity context safely
    context = ""
    for t in similar_tickets:
        ctx_fields = t.get('fields', {})
        ctx_summary = ctx_fields.get('summary', t.get('summary', ''))

        if 'fields' in t:
            ctx_description = safe_get_description(ctx_fields.get('description'))
        else:
            ctx_description = t.get('description', '')

        context += f"\nTicket: {t['key']}\nSummary: {ctx_summary}\nDescription: {ctx_description}\n---"

    # Invoke chain
    return chain.invoke({
        "key": ticket.get('key', ''),
        "summary": summary,
        "description": description,
        "context": context
    })
