from app.analytics import (
    get_revenue_by_region,
    get_revenue_by_product,
)


def test_revenue_by_region():
    results = get_revenue_by_region()

    assert len(results) == 4


def test_revenue_by_product():
    results = get_revenue_by_product()

    assert len(results) == 3