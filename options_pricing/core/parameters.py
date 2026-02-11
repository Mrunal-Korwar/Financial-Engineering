"""
Parameter management for option pricing.
"""

from typing import Dict, Any, Optional
from options_pricing.core.constants import OptionType, OptionStyle, TRADING_DAYS_PER_YEAR
from options_pricing.core.validators import (
    validate_positive,
    validate_non_negative,
    validate_integer_positive
)


class OptionParameters:
    """
    Container for all option pricing parameters with validation.
    
    Attributes:
        r: Compounded annual interest rate
        sigma: Annualized volatility
        q: Continuous dividend yield
        S0: Initial stock price
        K: Strike price
        T: Time to maturity (years)
        N: Number of periods in binomial tree
        option_type: Call or Put
        option_style: European or American
    """
    
    def __init__(
        self,
        r: float,
        sigma: float,
        q: float,
        S0: float,
        K: float,
        T: float,
        option_type: OptionType,
        option_style: OptionStyle,
        N: Optional[int] = None
    ):
        """
        Initialize option parameters.
        
        Args:
            r: Annual interest rate
            sigma: Annual volatility
            q: Continuous dividend yield
            S0: Initial stock price
            K: Strike price
            T: Time to maturity (years)
            option_type: Call or Put
            option_style: European or American
            N: Number of periods (if None, calculated as T * 252)
        """
        self.r = r
        self.sigma = sigma
        self.q = q
        self.S0 = S0
        self.K = K
        self.T = T
        self.option_type = option_type
        self.option_style = option_style
        
        # Calculate N if not provided
        if N is None:
            self.N = int(T * TRADING_DAYS_PER_YEAR)
        else:
            self.N = N
    
    def validate(self) -> None:
        """
        Validate all parameters.
        
        Raises:
            ValidationError: If any parameter is invalid
        """
        # Validate rate, volatility, and dividend yield are non-negative
        validate_non_negative(self.r, "Interest rate (r)")
        validate_non_negative(self.sigma, "Volatility (sigma)")
        validate_non_negative(self.q, "Dividend yield (q)")
        
        # Validate stock price and strike price are positive
        validate_positive(self.S0, "Initial stock price (S0)")
        validate_positive(self.K, "Strike price (K)")
        
        # Validate time to maturity is positive
        validate_positive(self.T, "Time to maturity (T)")
        
        # Validate number of periods is positive integer
        validate_integer_positive(self.N, "Number of periods (N)")
        
        # Validate option type and style are proper enums
        if not isinstance(self.option_type, OptionType):
            raise TypeError(f"option_type must be OptionType enum, got {type(self.option_type)}")
        if not isinstance(self.option_style, OptionStyle):
            raise TypeError(f"option_style must be OptionStyle enum, got {type(self.option_style)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert parameters to dictionary.
        
        Returns:
            Dictionary representation of parameters
        """
        return {
            "interest_rate": self.r,
            "volatility": self.sigma,
            "dividend_yield": self.q,
            "initial_stock_price": self.S0,
            "strike_price": self.K,
            "time_to_maturity": self.T,
            "number_of_periods": self.N,
            "option_type": self.option_type.value,
            "option_style": self.option_style.value
        }
    
    def __repr__(self) -> str:
        """String representation of parameters."""
        return (
            f"OptionParameters("
            f"S0={self.S0}, K={self.K}, r={self.r}, "
            f"sigma={self.sigma}, q={self.q}, T={self.T}, N={self.N}, "
            f"type={self.option_type.value}, style={self.option_style.value})"
        )
