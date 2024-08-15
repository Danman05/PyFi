from const import _ALLOWED_PERIODS_

def validate_period(period):
    """
    Validates if the provided period is allowed.

    Args:
        period (str): The period to validate.

    Raises:
        ValueError: If the period is not in the allowed periods list.
    """
    if period not in _ALLOWED_PERIODS_:
        raise ValueError(f"Invalid Period: {period}. Allowed periods are: {_ALLOWED_PERIODS_}")
    