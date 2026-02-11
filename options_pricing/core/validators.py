"""
Validation functions for option pricing parameters.
"""

from typing import Any
from options_pricing.utils.exceptions import ValidationError


def validate_positive(value: float, name: str) -> None:
    """
    Validate that a value is strictly positive (> 0).
    
    Args:
        value: The value to validate
        name: Parameter name for error messages
    
    Raises:
        ValidationError: If value is not positive
    """
    if value <= 0:
        raise ValidationError(f"{name} must be positive, got {value}")


def validate_non_negative(value: float, name: str) -> None:
    """
    Validate that a value is non-negative (>= 0).
    
    Args:
        value: The value to validate
        name: Parameter name for error messages
    
    Raises:
        ValidationError: If value is negative
    """
    if value < 0:
        raise ValidationError(f"{name} must be non-negative, got {value}")


def validate_probability(p: float) -> None:
    """
    Validate that a probability is in the valid range (0, 1).
    
    Args:
        p: Probability value to validate
    
    Raises:
        ValidationError: If probability is out of range
    """
    if not (0 < p < 1):
        raise ValidationError(
            f"Risk-neutral probability must be between 0 and 1 (exclusive), got {p}"
        )


def validate_integer_positive(value: int, name: str) -> None:
    """
    Validate that an integer value is strictly positive.
    
    Args:
        value: The value to validate
        name: Parameter name for error messages
    
    Raises:
        ValidationError: If value is not a positive integer
    """
    if not isinstance(value, int):
        raise ValidationError(f"{name} must be an integer, got {type(value).__name__}")
    if value <= 0:
        raise ValidationError(f"{name} must be positive, got {value}")
