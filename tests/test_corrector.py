

from types import SimpleNamespace

from app.sql_corrector import correct_sql


def test_correct_sql():

    question = "Show me the names of all customers"

    bad_sql = """
    SELECT customer_name
    FROM customers;
    """

    error = "no such column: customer_name"

    # Fake OpenAI response
    fake_response = SimpleNamespace(
        output_text="SELECT name FROM customers;"
    )

    # Fake OpenAI client
    fake_client = SimpleNamespace(
        responses=SimpleNamespace(
            create=lambda **kwargs: fake_response
        )
    )

    corrected_sql = correct_sql(
        question,
        bad_sql,
        error,
        client=fake_client
    )

    assert corrected_sql == "SELECT name FROM customers;"
