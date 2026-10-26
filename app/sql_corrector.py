
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schema import get_database_schema

load_dotenv()


def correct_sql(question, sql_query, error, client=None):

    if client is None:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    schema = get_database_schema()

    prompt = f"""
You are an expert SQL developer.

A SQL query was generated for the user's question, but the database
returned an error when the query was executed.

Your task is to correct the SQL query.

Database schema:
{schema}

User question:
{question}

Original SQL query:
{sql_query}

Database error:
{error}

Generate a corrected SQL query that answers the user's question.

Return ONLY the corrected SQL query.
Do not include explanations, markdown, or ```sql fences.
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    corrected_sql = response.output_text.strip()

    return corrected_sql
