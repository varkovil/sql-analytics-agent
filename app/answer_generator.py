import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))   

def gen_natural_language_explanation(columns,results):
    prompt = f"""
You are a seasoned data analyst. You need to analyse the results of an SQL query
given below and explain the results in natural language. 
The SQL query has been executed, and you have the results in a tuple format. 
If the results contain no meaningful data (for example, an empty result
set or NULL values), please state that you cannot find any data in the database for the given query.
Do not speculate about why the data is missing.
Only if the data is available, proceed with the analysis.
Your task is to interpret the data, identify trends, patterns, and anomalies, 
and provide actionable insights that can help in decision-making.
Generate your response only based on the data provided. 

Do not make assumptions or add information that is not present in the results.  

query_result = {columns}: {results}
"""
    response = client.responses.create(input=prompt, model="gpt-4o-mini")


    explanation = response.output_text.strip()

    return explanation



