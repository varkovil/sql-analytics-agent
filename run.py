from app.database import get_connection
connection = get_connection()
cursor = connection.cursor()
cursor.execute("""SELECT region,SUM(revenue) FROM customers JOIN orders ON customers.customer_id = orders.customer_id GROUP BY region""")
results = cursor.fetchall()
for row in results:
    print(f"Region: {row[0]}, Total Revenue: {row[1]}")
connection.close()
