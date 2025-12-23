from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional


def _third_thursday(year: int, month: int) -> date:
    """
    Returns the date of the third Thursday for a given month/year.
    Vietnamese VN30 futures contracts typically expire on this day.
    """
    first_day = date(year, month, 1)
    # weekday(): Monday=0 ... Sunday=6, so Thursday=3
    offset = (3 - first_day.weekday()) % 7
    first_thursday = first_day + timedelta(days=offset)
    return first_thursday + timedelta(weeks=2)


def get_derivative_expiry_overview(
    reference_date: Optional[date] = None,
    months_ahead: int = 4,
) -> List[Dict[str, Any]]:
    """
    Generates a lightweight schedule of upcoming VN30 futures (VN30F) expiry dates.

    Args:
        reference_date: Starting point for the schedule. Defaults to today.
        months_ahead: Number of future expiry months to include.

    Returns:
        A list of dictionaries containing contract metadata such as code, expiry date,
        days remaining and cyclical labels.
    """
    if months_ahead <= 0:
        return []

    if reference_date is None:
        reference_date = datetime.now().date()

    schedule: List[Dict[str, Any]] = []
    month_cursor = reference_date.month
    year_cursor = reference_date.year

    collected = 0
    while collected < months_ahead:
        expiry_date = _third_thursday(year_cursor, month_cursor)
        if expiry_date >= reference_date:
            contract_code = f"VN30F{str(year_cursor)[-2:]}{month_cursor:02d}"
            cycle = (
                "Hợp đồng hiện tại"
                if collected == 0
                else "Kỳ kế tiếp"
                if collected == 1
                else "Kỳ mở rộng"
            )

            schedule.append(
                {
                    "code": contract_code,
                    "expiry_date": expiry_date,
                    "days_remaining": (expiry_date - reference_date).days,
                    "cycle": cycle,
                    "month_label": expiry_date.strftime("Tháng %m/%Y"),
                }
            )
            collected += 1

        # Move to next month
        month_cursor += 1
        if month_cursor > 12:
            month_cursor = 1
            year_cursor += 1

    return schedule

