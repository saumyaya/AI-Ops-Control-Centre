
# 🤖 Jira AI Chatbot

An intelligent command-line chatbot that integrates with **Jira** and a **language model** to analyze, summarize, comment, and assign Jira tickets.
This tool helps streamline ticket management by offering quick insights and updates using natural language understanding.

---

## 🚀 Features

* 🔍 **List tickets** by status: all, open, or closed  
* 📄 **Summarize** Jira tickets  
* 🧠 **AI analysis** of issue descriptions  
* 💬 **Auto-comment** on tickets with AI-generated suggestions  
* 🧑‍💼 **Auto-assign** tickets based on least workload using load balancing  

---

## 🧠 Tech Stack

* Python 3.x  
* Jira REST API (v3)  
* Basic Auth (Email + API Token)  
* Ollama Mistral LLM (or any compatible local model)  

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

3. **Create a `config.py` file:**

```python
EMAIL = "your-email@example.com"
API_TOKEN = "your-jira-api-token"
DOMAIN = "https://your-domain.atlassian.net"
PROJECT_KEY = "your project key"
OLLAMA_MODEL = "mistral"

ASSIGNEES = {
    "user1@example.com": "accountId1",
    "user2@example.com": "accountId2",
    ...
}
```

---

## 💬 Usage

Run the chatbot:

```bash
python chatbot.py
```

---

## 🔧 Commands

```
help                            Show available commands  
exit / quit                     Exit the chatbot  

all                             Show all tickets  
open                            Show only open tickets  
closed                          Show only closed tickets  

summarize <TICKET_KEY>          Show summary and description  
analyze <TICKET_KEY>            Run AI analysis on the ticket  
comment <TICKET_KEY>            Analyze and comment on Jira ticket  

assign <TICKET_KEY>             Auto-assign ticket to least-loaded user  
auto assign                     Auto-assign all unassigned tickets  
```

**Example:**

```
You > open  
KAN-58: Load balancer health check failed for instance B  

You > analyze KAN-58  
🧠 AI Suggestion:  
Investigate health probe configuration or backend instance stability.  

You > comment KAN-58  
✅ Comment added to KAN-58  

You > assign KAN-58  
✅ Assigned KAN-58 to user2@example.com  

You > auto assign  
🔄 Running auto assignment...  
✅ Assigned KAN-59 to user1@example.com  
```

---

## 📁 Project Structure

```
jira-ai-chatbot/
├── chatbot.py            # Main CLI chatbot  
├── auto_assign.py        # Load-balanced ticket assignment logic  
├── jira_client.py        # Jira API interactions  
├── llm_chain.py          # LLM analysis logic  
├── config.py             # Your Jira credentials and settings  
├── main.py               # Powers the chatbot  
└── README.md             # Project info  
```

---

## 👩‍💻 Author

**Saumya Mathur**

[LinkedIn](https://www.linkedin.com/in/saumya-mathur-60351a270/)


