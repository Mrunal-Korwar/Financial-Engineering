"""
Helper calculation functions.
"""

from options_pricing.core.constants import TRADING_DAYS_PER_YEAR


def calculate_periods_from_days(T: float, days_per_year: int = TRADING_DAYS_PER_YEAR) -> int:
    """
    Calculate number of periods assuming one day per period.
    
    Args:
        T: Time to maturity in years
        days_per_year: Trading days per year (default 252)
    
    Returns:
        Number of periods as integer
    """
    return int(T * days_per_year)
