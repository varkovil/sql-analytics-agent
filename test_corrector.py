

from app.sql_corrector import correct_sql


question = "Show me the names of all customers"

bad_sql = """
SELECT customer_name
FROM customers;
"""

error = "no such column: customer_name"


corrected_sql = correct_sql(
    question,
    bad_sql,
    error
)

print("Corrected SQL:")
print(corrected_sql)