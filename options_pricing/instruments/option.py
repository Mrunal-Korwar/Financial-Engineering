"""
Base option class for all option types.
"""

from abc import ABC, abstractmethod
from options_pricing.core.constants import OptionType


class Option(ABC):
    """
    Abstract base class for financial options.
    
    Attributes:
        K: Strike price
        option_type: Call or Put
    """
    
    def __init__(self, K: float, option_type: OptionType):
        """
        Initialize option.
        
        Args:
            K: Strike price
            option_type: Call or Put
        """
        self.K = K
        self.option_type = option_type
    
    def payoff(self, S: float) -> float:
        """
        Calculate option payoff (intrinsic value) at given stock price.
        
        Args:
            S: Stock price
        
        Returns:
            Option payoff
        """
        if self.option_type == OptionType.CALL:
            return max(S - self.K, 0)
        else:  # PUT
            return max(self.K - S, 0)
    
    @abstractmethod
    def can_exercise_early(self) -> bool:
        """
        Determine if early exercise is allowed.
        
        Returns:
            True if early exercise is allowed, False otherwise
        """
        pass
    
    def __repr__(self) -> str:
        """String representation of option."""
        return f"{self.__class__.__name__}(K={self.K}, type={self.option_type.value})"
