def analyze_ticket(ticket):
    fields = ticket.get("fields", ticket)  # Use fields if present, else ticket itself
    summary = fields.get('summary', '')
    description = (
        fields.get('description', {})
        if isinstance(fields.get('description', {}), dict)
        else fields.get('description', '')
    )

    if isinstance(description, dict):
        description = (
            description.get('content', [{}])[0]
            .get('content', [{}])[0]
            .get('text', '')
        )

    query = f"{summary} {description}".strip()

    from rag_utils import retrieve_similar_tickets
    from auto_assign import fetch_all_tickets

    similar_keys = retrieve_similar_tickets(query)
    all_tickets = fetch_all_tickets()
    similar_tickets = [t for t in all_tickets if t['key'] in similar_keys]

    context = ""
    for t in similar_tickets:
        ctx_fields = t.get("fields", t)
        ctx_summary = ctx_fields.get('summary', '')
        ctx_description = ctx_fields.get('description', '')
        if isinstance(ctx_description, dict):
            ctx_description = (
                ctx_description.get('content', [{}])[0]
                .get('content', [{}])[0]
                .get('text', '')
            )
        context += f"\nTicket: {t['key']}\nSummary: {ctx_summary}\nDescription: {ctx_description}\n---"

    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import PromptTemplate
    from config import OLLAMA_MODEL

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
    llm = OllamaLLM(model=OLLAMA_MODEL)
    chain = prompt | llm

    return chain.invoke({
        "key": ticket.get("key", ""),
        "summary": summary,
        "description": description,
        "context": context
    })

