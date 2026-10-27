
import pytest

from app.database import (
    DATABASE_PATH,
    create_tables,
    insert_sample_data,
)


@pytest.fixture(autouse=True)
def initialize_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    create_tables()
    insert_sample_data()

    yield
