# 🛡️ QueryGuard

AI-Powered Text-to-SQL Assistant with Query Validation.

QueryGuard allows users to ask questions about a PostgreSQL database in plain English. It uses Gemini to generate SQL, validates the generated query using safety guardrails, executes only safe read-only queries, and converts the database result into a simple natural-language answer.

##  Features

-  Ask database questions in natural language
-  AI-powered SQL generation using Google Gemini
-  SQL validation and safety guardrails
-  Only SELECT queries are allowed
-  Blocks INSERT, UPDATE, DELETE, DROP, ALTER and other unsafe operations
-  PostgreSQL database integration
-  FastAPI backend
-  Streamlit frontend
-  AI-generated natural-language explanations
-  Displays generated SQL and database results

##  Architecture

```text
User Question
     ↓
Streamlit Frontend
     ↓
FastAPI Backend
     ↓
Gemini AI
     ↓
SQL Query Generation
     ↓
QueryGuard Validation
     ↓
PostgreSQL Database
     ↓
Query Result
     ↓
Gemini AI
     ↓
Natural Language Answer


## Tech Stack
Backend
Python
FastAPI
SQLAlchemy
PostgreSQL
Google Gemini API
Frontend
Streamlit
Libraries
python-dotenv
requests
psycopg2-binary
google-generativeai
📁 Project Structure
queryguard-ai/
│
├── backend/
│   ├── database.py
│   ├── guardrails.py
│   ├── llm_service.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   └── app.py
│
├── .gitignore
└── README.md


## How It Works
User enters a question in plain English.
Gemini receives the database schema and user question.
Gemini generates a PostgreSQL SELECT query.
QueryGuard validates the generated SQL.
Unsafe or non-SELECT queries are blocked.
Safe queries are executed on PostgreSQL.
The database result is sent to Gemini.
Gemini converts the result into a simple answer.
The application displays the answer, generated SQL, and database result.

## Example Questions
December mein total sales kitni hui?

Which product generated the highest sales?

North region mein total sales kitni hui?

December mein kitne products sell hue?

November ki total sales batao.


## Security

QueryGuard uses SQL validation before executing AI-generated queries.

The application currently:

Allows only SELECT queries
Blocks data modification queries
Blocks database structure modification queries
Rejects multiple SQL statements

API keys and database credentials are stored in environment variables and are not committed to GitHub.

⚙️ Local Setup
1. Clone the repository
git clone https://github.com/shellyverma/queryguard-ai.git
cd queryguard-ai
2. Create and activate virtual environment
python -m venv venv

Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r backend/requirements.txt
4. Configure environment variables

Create a .env file inside the backend folder:

GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_postgresql_database_url
5. Start the FastAPI backend
cd backend
uvicorn main:app --reload
6. Start the Streamlit frontend

Open another terminal:

streamlit run frontend/app.py

The application will open in the browser.

## Project Status

QueryGuard is currently working as a local AI-powered Text-to-SQL application with PostgreSQL, FastAPI, Streamlit, Gemini integration, and SQL validation.

##  Author

Shelly Verma
