from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def generate_sql_query(question):
    prompt = f"""
    You are a SQL expert.

Our database contains these tables:

customers:
- customer_id
- name
- region
- segment

orders:
- order_id
- customer_id
- order_date
- product
- quantity
- revenue

Convert the user's question into SQLite SQL.

User question:
{question}

Return ONLY the SQL query
"""
    response = client.responses.create(
        model="gpt-4o-mini",
        input = prompt
        
    )

    sql=response.output_text.strip()
    if sql.startswith("```sql"):
        sql = sql[6:]
    
    if sql.endswith("```"):
        sql = sql[:-3]

    return sql


