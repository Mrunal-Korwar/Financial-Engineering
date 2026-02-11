"""
Custom exceptions for options pricing system.
"""


class OptionPricingError(Exception):
    """Base exception for all option pricing errors."""
    pass


class ValidationError(OptionPricingError):
    """Raised when parameter validation fails."""
    pass


class ConfigurationError(OptionPricingError):
    """Raised when configuration file is invalid or cannot be loaded."""
    pass


class ModelError(OptionPricingError):
    """Raised when pricing model encounters a computational error."""
    pass
