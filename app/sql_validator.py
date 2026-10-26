def validate_sql(sql):
    sql = sql.strip()

    if not sql:
        return False

    if not sql.lower().startswith("select"):
        return False

    dangerous_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
    ]

    sql_lower = sql.lower()
    for keyword in dangerous_keywords:
        if keyword in sql_lower:
            return False

    return True