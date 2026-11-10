"""Business logic: convert a Gregorian date to a Hebrew date via Hebcal."""
import datetime

import httpx

from config import HEBCAL_URL, REQUEST_TIMEOUT


def convert_to_hebrew(gy: int, gm: int, gd: int) -> dict:
    """Convert a Gregorian date to a Hebrew date.

    Args:
        gy: Gregorian year.
        gm: Gregorian month (1-12).
        gd: Gregorian day of month.

    Returns:
        A dict with the Gregorian date, the Hebrew date string, its
        parts (day, month, year) and any events falling on that day.

    Raises:
        ValueError: The date does not exist (or Hebcal rejected it).
        httpx.HTTPError: Hebcal failed or returned a non-JSON response.
    """
    gregorian = datetime.date(gy, gm, gd)  # raises ValueError if invalid

    data = _fetch_from_hebcal(gregorian)
    if "error" in data:
        raise ValueError(data["error"])

    return {
        "gregorian": gregorian.isoformat(),
        "hebrew": data["hebrew"],
        "hebrew_parts": {
            "day": data["hd"],
            "month": data["hm"],
            "year": data["hy"],
        },
        "events": data.get("events", []),
    }


def _fetch_from_hebcal(gregorian: datetime.date) -> dict:
    """Call the Hebcal converter endpoint and return the decoded JSON."""
    params = {
        "cfg": "json",
        "gy": gregorian.year,
        "gm": gregorian.month,
        "gd": gregorian.day,
        "g2h": 1,
    }
    response = httpx.get(HEBCAL_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    try:
        return response.json()
    except ValueError as exc:
        # Not ValueError: that is reserved for "invalid date".
        raise httpx.DecodingError(
            "Hebcal returned a non-JSON response",
            request=response.request,
        ) from exc
