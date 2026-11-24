from nour_transfers.rules import can_transfer, days_of_cover, priority


def test_reserve_is_kept_exactly():
    assert can_transfer(from_stock=40, quantity=30, reserve=10) is True


def test_no_sales_means_no_urgency():
    assert days_of_cover(stock=12, avg_daily_sales=0) is None
    assert priority(is_chronic=True, cover_days=None) == "normal"

def test_quantity_zero_is_rejected():
    assert can_transfer(from_stock=40, quantity=0,reserve=10) is False

def test_non_Chronic_item_with_low_Cover_isnot_urgent():
    for i in range(3):
        assert priority(is_chronic=False, cover_days=i) != "urgent"


def test_exactly_3_days_of_cover_isnot_urgent():
    assert priority(is_chronic=True, cover_days=3) != "urgent"
    assert priority(is_chronic=False, cover_days=3) != "urgent"