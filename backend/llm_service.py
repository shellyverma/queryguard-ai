import os

from dotenv import load_dotenv
import google.generativeai as genai

from database import get_schema_info

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY .env file mein nahi mili.")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.6-flash")


def generate_sql(question: str) -> str:
    schema = get_schema_info()

    # The database schema gives Gemini the tables and columns
    # it can use while generating the SQL query.
    prompt = f"""
You are an expert PostgreSQL SQL assistant.

Convert the user's natural language question into a PostgreSQL SELECT query.

DATABASE SCHEMA:
{schema}

RULES:
1. Generate only a SELECT query.
2. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, or REVOKE.
3. Never generate multiple SQL statements.
4. Use only tables and columns available in the database schema.
5. Use valid PostgreSQL syntax.
6. Return only the SQL query.
7. Do not use markdown code fences.
8. Do not explain the query.

USER QUESTION:
{question}
"""

    response = model.generate_content(prompt)

    return response.text.strip()


def generate_answer(question: str, sql_query: str, columns, rows) -> str:
    result_data = []

    for row in rows:
        row_dict = {}

        for column, value in zip(columns, row):
            row_dict[column] = value

        result_data.append(row_dict)

    # Gemini converts the database result into a simple
    # natural-language answer for the user.
    prompt = f"""
You are a helpful data analyst.

User question:
{question}

SQL query:
{sql_query}

Database result:
{result_data}

Explain the result in simple English.

Rules:
1. Answer the user's question directly.
2. Mention the important result or number.
3. Keep the answer concise.
4. Do not invent information.
5. If there are no results, clearly say that no matching data was found.
"""

    response = model.generate_content(prompt)

    return response.text.strip()