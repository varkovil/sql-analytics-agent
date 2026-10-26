

from openai import OpenAI
import os   
from dotenv import load_dotenv
from app.schema import get_database_schema


load_dotenv()

def is_question_relevant(question):
    schema = get_database_schema()
    

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""You are a database relevance checker. You are given a question and a database schema. 
Your task is to determine if the question is relevant to the database schema.
question:{question}
schema:{schema}
Give only one word answer, either "yes" or "no". If the question is relevant to the database schema, answer "yes". 
If the question is not relevant to the database schema, answer "no".
"""

    response = client.responses.create(input=prompt, model="gpt-4o-mini")
    answer = response.output_text.strip().lower()

    return answer

