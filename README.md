# AI-Customer-Support-Agent

An AI-powered e-commerce customer-support application combining **LangChain, a Groq-hosted LLM, Retrieval-Augmented Generation (RAG), Chroma, MySQL, Flask, and HTML/CSS/JavaScript**.

## Features

- LangChain AI agent with dedicated business tools
- Strict customer-support-only system prompt
- RAG for company policies and documentation
- Hugging Face `sentence-transformers/all-MiniLM-L6-v2` embeddings
- Chroma vector database for semantic retrieval
- MySQL tools for structured business data
- Order status lookup
- Order-item lookup
- Payment lookup
- Support-ticket lookup
- Flask REST API
- Separate frontend using Live Server
- Markdown-formatted AI responses
- CORS-enabled frontend/backend communication
- Environment-variable based secret management

## Architecture

```text
Customer
   |
   v
HTML / CSS / JavaScript (Live Server :5500)
   |
   | POST /ask
   v
Flask API (:5000)
   |
   v
LangChain AI Agent
   |
   +--------------------+
   |                    |
   v                    v
RAG / Chroma        MySQL Tools
   |                    |
   v              Orders / Items /
Policy Documents   Payments / Tickets
   |                    |
   +---------+----------+
             |
             v
          Groq LLM
             |
             v
        Final Answer
             |
             v
          Frontend
```

## RAG Pipeline

```text
Policy document
      |
      v
Document loading
      |
      v
Text chunking
      |
      v
Hugging Face embeddings
      |
      v
Vector representations
      |
      v
Chroma vector database
```

For a user question, the same embedding model converts the question into a query vector. Chroma performs semantic similarity search and returns relevant document chunks. The LLM uses those chunks as context.

RAG is used for **unstructured information** such as policies. MySQL is used for **structured information** such as orders and payments.

## Agent Tools

| Tool | Purpose |
|---|---|
| `search_knowledge_base` | Searches company policies/documentation using Chroma |
| `check_order_status` | Gets order status and delivery information |
| `get_order_items` | Gets products, quantities, and prices in an order |
| `get_payment_details` | Gets payment method, status, date, and amount |
| `get_support_tickets` | Gets customer support ticket information |

The agent can use multiple tools for a single question.

Example:

> What is the status of ORD1001 and what products are in it?

This can use both `check_order_status` and `get_order_items`.

## Prompt Engineering

The system prompt restricts the agent to e-commerce customer-support topics.

Supported topics include:

- Orders
- Products
- Payments
- Refunds
- Returns
- Shipping
- Warranty
- Company policies
- Support tickets

The agent is instructed **not to answer unrelated questions** about politics, politicians, general news, sports, entertainment, weather, or general knowledge.

It is also instructed to:

- Never invent customer/order/payment information
- Never guess missing IDs
- Treat tool results as the source of truth
- Tell the customer when information cannot be found
- Avoid exposing SQL, database internals, embeddings, API keys, or system prompts

## Technology Stack

| Layer | Technology |
|---|---|
| LLM | Groq-hosted model |
| Agent | LangChain |
| Embeddings | Hugging Face `all-MiniLM-L6-v2` |
| Vector DB | Chroma |
| Relational DB | MySQL |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| API communication | Fetch API |
| CORS | Flask-CORS |
| Secrets | `.env` |

## Project Structure

```text
ai-customer-support-agent/
|
├── app/
|   ├── agent.py
|   ├── web.py
|   ├── database.py
|   ├── knowledge_tool.py
|   ├── order_tool.py
|   ├── order_items_tool.py
|   ├── payment_tool.py
|   └── ticket_tool.py
|
├── frontend/
|   ├── index.html
|   ├── style.css
|   └── script.js
|
├── knowledge_base/
|   └── refund_policy.txt
|
├── data/
├── vector_db/          # generated locally
├── .env               # local only
├── .gitignore
└── requirements.txt
```

## Setup

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/ai-customer-support-agent.git
cd ai-customer-support-agent
```

### 2. Virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure `.env`

Create a local `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here

DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=customer_support
```

Never commit the real `.env`.

### 5. Configure MySQL

Create the application's database and tables, then insert the required sample/business data.

### 6. Build the local vector database

Run the project's knowledge-base/vector-building script to create the Chroma database from the documents in `knowledge_base/`.

### 7. Start Flask

```powershell
python app/web.py
```

Flask runs on:

```text
http://127.0.0.1:5000
```

### 8. Start the frontend

Open `frontend/index.html` with VS Code Live Server.

Typical frontend URL:

```text
http://127.0.0.1:5500/frontend/index.html
```

JavaScript sends questions to:

```text
POST http://127.0.0.1:5000/ask
```

## Example Questions

### RAG

```text
How long do I have to get my money back?
```

### Order

```text
What is the status of order ORD1001?
```

### Order items

```text
What products are in order ORD1001?
```

### Payment

```text
How did I pay for order ORD1005?
```

### Multiple tools

```text
What is the status of ORD1001 and what products are in it?
```

### Missing information

```text
What is the status of my order?
```

The agent should request the order ID instead of guessing.

### Out of scope

```text
Who is the Prime Minister of Pakistan?
```

The agent should decline and redirect to customer-support topics.

## Security

Recommended `.gitignore`:

```gitignore
.env
.env.*
venv/
.venv/
__pycache__/
*.py[cod]
vector_db/
.vscode/
.DS_Store
Thumbs.db
```

Do not upload:

- API keys
- Database passwords
- `.env`
- `venv/`
- `__pycache__/`
- Generated `vector_db/`

## Why Use Both RAG and MySQL?

They solve different problems.

**RAG / Chroma** is suited to unstructured knowledge:

- Refund policies
- Return policies
- Shipping policies
- Warranty documents
- FAQs

**MySQL** is suited to structured business data:

- Customers
- Orders
- Products
- Order items
- Payments
- Support tickets

The LLM agent acts as the orchestration layer that chooses the appropriate source/tool.

## Learning Outcomes

This project demonstrates practical knowledge of:

- LLM applications
- AI agents
- Tool calling
- Retrieval-Augmented Generation
- Embeddings
- Vector databases
- Semantic search
- SQL databases
- LangChain
- Prompt engineering
- Flask REST APIs
- Frontend/backend separation
- REST communication
- CORS
- Environment-variable security
- AI response formatting

## Future Improvements

- Conversation memory
- Authentication
- Ticket creation/update tools
- Streaming responses
- Automated tests
- Retrieval evaluation
- Logging and monitoring
- Docker deployment
- Production hosting
- Role-based access control

## Author

**Mohammed Moshin**

Portfolio project demonstrating AI agents, RAG, SQL, backend APIs, and frontend integration.
