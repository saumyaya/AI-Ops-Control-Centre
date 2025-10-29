# 📊 Jira AI Control Centre (Streamlit UI)

* An **AI-powered Jira dashboard** with an intuitive **web UI** built in **Streamlit**.
It combines Jira’s ticketing system with **local LLM analysis** to help teams **view, analyze, comment, and assign tickets** with ease.
* [Click here](https://ai-ops-control-centre-vn6kkepdzfbwbai7bbtjpf.streamlit.app/)
---

## 🚀 Features

### 📋 Ticket Management

* **All Tickets** — View all Jira tickets in the project
* **Open Tickets** — Show tickets not marked as Done
* **Closed Tickets** — Show completed tickets

### 📝 Ticket Actions

* **Summarize** — Display the summary & description of a ticket
* **Analyze** — AI-generated analysis of a ticket's content
* **Comment** — Post AI suggestions directly as a Jira comment
* **Suggest** — Get RAG-powered recommendations using similar past tickets

### 🧑‍💼 Assignment

* **Auto Assign** — Distribute unassigned tickets to least-loaded team members
* **Auto Assign Specific** — Assign a chosen ticket to the least-loaded user

### ❓ Natural Language Queries

* Ask in plain English (e.g., *"Show me high priority tickets"*) and get filtered Jira results

### 🔄 Live Updates

* **Refresh** — Reload Jira data without restarting the app

---

## 🧠 Tech Stack

* **Python 3.x**
* **Streamlit** (UI)
* **Jira REST API v3** (ticket management)
* **Ollama LLM** (local AI model for analysis)
* **FAISS + Sentence Transformers** (RAG for similar ticket retrieval)

---

## 🛠 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/ai-ops-control-centre.git
cd ai-ops-control-centre
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Jira & Model

Instead of storing credentials in `config.py`, store them in **Streamlit Secrets**:
Create a `.streamlit/secrets.toml` file:

```toml
EMAIL = "your-email@example.com"
API_TOKEN = "your-jira-api-token"
DOMAIN = "https://your-domain.atlassian.net"
PROJECT_KEY = "YOURPROJECT"
OLLAMA_MODEL = "mistral"

ASSIGNEE_EMAILS = [
    "user1@example.com",
    "user2@example.com"
]
```

---

## 💬 Usage

Run the app locally:

```bash
streamlit run ui_app.py
```

Deploy to **Streamlit Cloud**:

* Push code to GitHub
* Link repo in [share.streamlit.io](https://share.streamlit.io)
* Add your credentials in Streamlit Cloud → **Secrets**

---

## 📂 Project Structure

```
ai-ops-control-centre/
├── ui_app.py               # Streamlit UI app
├── chatbot.py               # CLI version
├── auto_assign.py           # Ticket assignment logic
├── jira_client.py           # Jira API functions
├── llm_chain.py             # AI + RAG processing
├── rag_utils.py             # Similar ticket retrieval
├── handle_natural_query.py  # Natural language → JQL
├── config.py                # Loads credentials (from secrets in UI)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---
## 📝 Author’s Note

This project is built using Ollama, meaning all AI features run locally on your machine. If you attempt to deploy this project (for example, on Streamlit Cloud or another hosting service), the AI-powered functionality will not work, since Ollama requires a local runtime environment.

Please note that the current Streamlit deployment is for educational purposes only — it demonstrates the app’s structure and interface, but the AI components are inactive in that environment.

## 💡 Scope for Improvement

* Integrate a Remote LLM API: Replace local Ollama calls with a cloud-based API (e.g., OpenAI, Anthropic, or Hugging Face) to enable online deployment.

* Add a Configurable Backend: Let users toggle between local (Ollama) and remote (API-based) modes using environment variables.

* Use a Proxy Service: Run a small local server that communicates with Ollama and can be connected to a remote app via secure tunneling (e.g., ngrok).

* Model Management Tools: Include scripts to easily download or switch between Ollama models.

* Improved Setup Documentation: Provide step-by-step installation and configuration instructions for both local and educational (deployed) use cases.

## 👩‍💻 Author

**Saumya Mathur**

[LinkedIn](https://www.linkedin.com/in/saumya-mathur) | [GitHub](https://github.com/saumyaya)

---
