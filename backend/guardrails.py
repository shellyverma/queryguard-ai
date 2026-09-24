import re

# These SQL operations can modify or destroy database data,
# so QueryGuard blocks them and allows read-only queries.
BLOCKED_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
    "MERGE",
    "EXEC",
    "EXECUTE",
}


def clean_sql(sql_query: str) -> str:
    # Gemini may return SQL inside markdown code fences.
    if not sql_query:
        return ""

    sql_query = sql_query.strip()
    sql_query = re.sub(r"^```sql\s*", "", sql_query, flags=re.IGNORECASE)
    sql_query = re.sub(r"^```\s*", "", sql_query)
    sql_query = re.sub(r"\s*```$", "", sql_query)

    return sql_query.strip()


def validate_sql(sql_query: str) -> tuple[bool, str]:
    sql_query = clean_sql(sql_query)

    if not sql_query:
        return False, "SQL query empty hai."

    normalized_sql = sql_query.upper().strip()

    # QueryGuard only executes SELECT queries.
    if not normalized_sql.startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    # Multiple statements could be used to bypass the safety check.
    statements = [
        statement.strip()
        for statement in sql_query.split(";")
        if statement.strip()
    ]

    if len(statements) > 1:
        return False, "Multiple SQL statements are not allowed."

    # Check whether the query contains any blocked SQL operation.
    for keyword in BLOCKED_KEYWORDS:
        pattern = rf"\b{keyword}\b"

        if re.search(pattern, normalized_sql):
            return False, f"Blocked SQL keyword detected: {keyword}"

    return True, "SQL query is valid."


def is_safe_query(sql_query: str) -> bool:
    is_valid, _ = validate_sql(sql_query)
    return is_valid