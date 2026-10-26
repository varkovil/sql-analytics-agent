from app.sql_executor import execute_sql


def test_execute_sql():
    sql = """
    SELECT region, SUM(revenue) AS total_revenue
    FROM customers
    JOIN orders
        ON customers.customer_id = orders.customer_id
    GROUP BY region
    """

    columns, results, error = execute_sql(sql)

    assert error is None
    assert "region" in columns
    assert "total_revenue" in columns
    assert len(results) == 4


def test_execute_invalid_sql():
    sql = """
    SELECT customer_name
    FROM customers
    """

    columns, results, error = execute_sql(sql)

    assert columns == []
    assert results == []
    assert error is not None