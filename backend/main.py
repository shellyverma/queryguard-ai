from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import run_query
from llm_service import generate_sql, generate_answer
from guardrails import validate_sql, clean_sql


app = FastAPI(
    title="QueryGuard API",
    description="AI-Powered Text-to-SQL Assistant with Query Validation",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "QueryGuard API is running!"
    }


@app.post("/query")
def query_database(request: QueryRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        sql_query = generate_sql(question)
        sql_query = clean_sql(sql_query)

        # Validate the generated SQL before sending it to the database.
        is_valid, validation_message = validate_sql(sql_query)

        if not is_valid:
            return {
                "success": False,
                "question": question,
                "sql_query": sql_query,
                "error": validation_message
            }

        columns, rows = run_query(sql_query)

        # Convert the database result into a natural-language answer.
        answer = generate_answer(
            question,
            sql_query,
            columns,
            rows
        )

        return {
            "success": True,
            "question": question,
            "sql_query": sql_query,
            "columns": columns,
            "rows": [list(row) for row in rows],
            "answer": answer
        }

    except Exception as e:
        return {
            "success": False,
            "question": question,
            "error": str(e)
        }