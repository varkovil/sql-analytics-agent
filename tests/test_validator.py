from app.sql_validator import validate_sql


def test_valid_select():
    sql = "SELECT * FROM customers"

    assert validate_sql(sql) is True


def test_reject_delete():
    sql = "DELETE FROM customers"

    assert validate_sql(sql) is False


def test_reject_empty_query():
    sql = ""

    assert validate_sql(sql) is False


def test_reject_multiple_statements():
    sql = "SELECT * FROM customers; DROP TABLE customers;"

    assert validate_sql(sql) is False