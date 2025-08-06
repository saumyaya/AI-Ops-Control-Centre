
# 🤖 Jira AI Chatbot

An intelligent command-line assistant that integrates **Jira** with a **local LLM (like Ollama Mistral)** to **analyze**, **summarize**, **auto-assign**, **comment**, and **filter tickets using natural language**.  
This tool streamlines DevOps workflows by combining smart JQL handling with LLM-powered analysis and RAG-based suggestions.

---

## 🚀 Features

- 🔍 **List tickets** by status: all, open, or closed  
- 📄 **Summarize** Jira tickets quickly  
- 🧠 **AI-based ticket analysis** using LLM  
- 💬 **Auto-comment** on tickets with AI-generated insights  
- 🧑‍💼 **Auto-assign tickets** using load balancing  
- 🗣️ **Natural Language Questions** like “Which tickets are unassigned?” or “Show high priority issues”  
- 📎 **RAG-based suggestions** from similar past tickets for better recommendations

---

## 🧠 Tech Stack

- Python 3.x  
- Jira REST API v3  
- Ollama (Mistral or compatible local LLM)  
- LangChain + Sentence Transformers + FAISS  
- Concurrent caching for speed optimization  
- Command-line interface (CLI) based interaction

---

## 🛠️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/jira-ai-chatbot.git
cd jira-ai-chatbot
````

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Configure credentials:**
   Create a file called `config.py` with the following content:

```python
EMAIL = "your-email@example.com"
API_TOKEN = "your-jira-api-token"
DOMAIN = "https://your-domain.atlassian.net"
PROJECT_KEY = "KAN"  # Replace with your actual Jira project key
OLLAMA_MODEL = "mistral"

ASSIGNEES = {
    "user1@example.com": "accountId1",
    "user2@example.com": "accountId2"
}
```

4. **(Optional) Build FAISS index for RAG:**

```bash
python build_index.py
```

---

## 💬 Usage

Run the chatbot:

```bash
python chatbot.py
```

---

## 🔧 Commands

| Command                    | Description                                                               |
| -------------------------- | ------------------------------------------------------------------------- |
| `help`                     | Show available commands                                                   |
| `exit` / `quit`            | Exit the chatbot                                                          |
| `refresh`                  | Reload latest ticket data                                                 |
| `all`                      | Show all Jira tickets                                                     |
| `open`                     | Show only open (incomplete) tickets                                       |
| `closed`                   | Show only completed/closed tickets                                        |
| `summarize <TICKET_KEY>`   | Show summary and description of a ticket                                  |
| `analyze <TICKET_KEY>`     | AI-powered analysis for resolution suggestions                            |
| `comment <TICKET_KEY>`     | AI analysis and auto-comment on Jira ticket                               |
| `suggest <TICKET_KEY>`     | RAG-based suggestion from similar past tickets                            |
| `auto assign`              | Assign all unassigned tickets using least-loaded strategy                 |
| `auto assign <TICKET_KEY>` | Assign a specific ticket to the least-loaded user                         |
| `ask <natural question>`   | Natural language question → JQL-based filter (e.g., "tickets with login") |

---

## 🧪 Examples

```bash
You > open  
KAN-102: Database error on user registration  

You > analyze KAN-102  
🧠 AI Suggestion:  
Check if DB pool is saturated. Review recent schema changes.

You > comment KAN-102  
✅ Comment added to KAN-102

You > auto assign  
✅ Assigned KAN-103 to user1@example.com  
✅ Assigned KAN-104 to user2@example.com

You > ask tickets with health check failure  
KAN-105: ELB health probe failing on instance A
```

---

## 📁 Project Structure

```
jira-ai-chatbot/
├── chatbot.py              # CLI chatbot logic
├── llm_chain.py            # LLM + RAG-based analysis
├── auto_assign.py          # Workload-based assignment logic
├── build_index.py          # Builds FAISS index for semantic similarity
├── rag_utils.py            # Search similar tickets with Sentence Transformers + FAISS
├── handle_natural_query.py # Natural language → JQL mapping
├── jira_client.py          # Jira REST API helper functions
├── config.py               # Your credentials + model settings
├── ticket_index.faiss      # (Generated) Vector index file
├── ticket_keys.pkl        # (Generated) Index to ticket mapping
└── README.md               # Project documentation
```

---

## ⚡ Performance Tips

* ✅ Uses **lazy loading** for FAISS, LangChain, and Ollama to reduce startup time
* ✅ LLM results are **threaded and cached** for faster reuse
* ✅ Add `refresh` to reload latest Jira data when needed

---

## 👩‍💻 Author

**Saumya Mathur**

[LinkedIn](https://www.linkedin.com/in/saumya-mathur-60351a270/)


