from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def get_schema_info():
    """Database ka schema (tables aur columns) fetch karta hai, taaki LLM ko context mil sake."""
    query = text("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    with engine.connect() as conn:
        result = conn.execute(query)
        rows = result.fetchall()

    schema = {}
    for table_name, column_name, data_type in rows:
        if table_name not in schema:
            schema[table_name] = []
        schema[table_name].append(f"{column_name} ({data_type})")

    schema_text = ""
    for table, columns in schema.items():
        schema_text += f"Table: {table}\nColumns: {', '.join(columns)}\n\n"

    return schema_text

def run_query(sql_query):
    """SQL query ko safely execute karta hai aur result return karta hai."""
    with engine.connect() as conn:
        result = conn.execute(text(sql_query))
        rows = result.fetchall()
        columns = list(result.keys())
        return columns, rows