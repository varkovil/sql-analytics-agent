from app.database import get_connection


def get_revenue_by_region():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT region, SUM(revenue)
        FROM customers
        JOIN orders
            ON customers.customer_id = orders.customer_id
        GROUP BY region
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_revenue_by_product():
    connection = get_connection() 
    cursor = connection.cursor()
    cursor.execute("""
        SELECT product, SUM(revenue)
        FROM orders
        GROUP BY product
        """)
    results = cursor.fetchall()
    connection.close()
    return results


def get_top_customers():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT customers.customer_id, customers.name, SUM(orders.revenue) as total_revenue
        FROM customers
        JOIN orders ON customers.customer_id = orders.customer_id
        GROUP BY customers.customer_id
        ORDER BY total_revenue DESC
        LIMIT 10
    """)
    results = cursor.fetchall()
    connection.close()
    return results


def test_top_customers():
    connection = get_connection()
    cursor = connection.cursor()    
    cursor.execute("""  
    SELECT customer_id, SUM(revenue)
        FROM orders
        GROUP BY customer_id
        ORDER BY SUM(revenue) DESC
    """)
    results = cursor.fetchall()
    connection.close()
    return results