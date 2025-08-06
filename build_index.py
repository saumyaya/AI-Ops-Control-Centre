from sentence_transformers import SentenceTransformer
import faiss
import pickle
from auto_assign import fetch_all_tickets

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Fetch Jira tickets
tickets = fetch_all_tickets()

# Extract summaries and descriptions
texts = []
keys = []

for t in tickets:
    summary = t['fields'].get('summary', '')
    
    description_field = t['fields'].get('description', {})
    if isinstance(description_field, dict):
        try:
            description = description_field.get('content', [{}])[0].get('content', [{}])[0].get('text', '')
        except (IndexError, AttributeError, TypeError):
            description = ''
    else:
        description = ''
    
    combined_text = f"{summary} {description}".strip()
    texts.append(combined_text)
    keys.append(t['key'])

# Compute embeddings
embeddings = model.encode(texts, convert_to_tensor=False, show_progress_bar=True)
embeddings = embeddings.astype("float32")

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, "ticket_index.faiss")

# Save keys with pickle
with open("ticket_keys.pkl", "wb") as f:
    pickle.dump(keys, f)

print("✅ FAISS index and ticket keys saved successfully.")
