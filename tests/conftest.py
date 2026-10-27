

import pytest
import app.database as database


@pytest.fixture(autouse=True)
def initialize_database(tmp_path, monkeypatch):
    # Give each test its own fresh SQLite database.
    test_database_path = tmp_path / "sales.db"

    # Make the application's database connection use this test database.
    monkeypatch.setattr(database, "DATABASE_PATH", test_database_path)

    # Create the tables and populate sample data.
    database.create_tables()
    database.insert_sample_data()

    # Run the test.
    yield
