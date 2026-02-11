"""
Abstract base class for pricing models.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from options_pricing.instruments.option import Option
from options_pricing.core.parameters import OptionParameters


class PricingModel(ABC):
    """
    Abstract base class for all option pricing models.
    """
    
    @abstractmethod
    def price(self, option: Option, parameters: OptionParameters) -> Dict[str, Any]:
        """
        Calculate option price.
        
        Args:
            option: Option to price
            parameters: Pricing parameters
        
        Returns:
            Dictionary containing pricing results
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> str:
        """
        Get information about the pricing model.
        
        Returns:
            Model description string
        """
        pass
