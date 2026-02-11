"""
American option implementation.
"""

from options_pricing.instruments.option import Option


class AmericanOption(Option):
    """
    American-style option (can be exercised at any time before maturity).
    """
    
    def can_exercise_early(self) -> bool:
        """
        American options can be exercised early.
        
        Returns:
            True
        """
        return True
