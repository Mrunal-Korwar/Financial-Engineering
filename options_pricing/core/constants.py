"""
Constants and enumerations for options pricing.
"""

from enum import Enum


class OptionType(Enum):
    """Option type enumeration."""
    CALL = "call"
    PUT = "put"

    @classmethod
    def from_string(cls, value: str):
        """Create OptionType from string value."""
        value_lower = value.lower()
        for member in cls:
            if member.value == value_lower:
                return member
        raise ValueError(f"Invalid option type: {value}. Must be 'call' or 'put'.")


class OptionStyle(Enum):
    """Option style enumeration."""
    EUROPEAN = "european"
    AMERICAN = "american"

    @classmethod
    def from_string(cls, value: str):
        """Create OptionStyle from string value."""
        value_lower = value.lower()
        for member in cls:
            if member.value == value_lower:
                return member
        raise ValueError(f"Invalid option style: {value}. Must be 'european' or 'american'.")


# Trading days per year (used for period calculations)
TRADING_DAYS_PER_YEAR = 252
