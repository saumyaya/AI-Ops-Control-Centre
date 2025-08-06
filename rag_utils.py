from sentence_transformers import SentenceTransformer
import faiss
import pickle

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("ticket_index.faiss")
ticket_keys = pickle.load(open("ticket_keys.pkl", "rb"))

def retrieve_similar_tickets(query, k=3):
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, k)
    results = [ticket_keys[i] for i in indices[0]]
    return results
