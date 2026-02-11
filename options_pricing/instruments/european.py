"""
European option implementation.
"""

from options_pricing.instruments.option import Option


class EuropeanOption(Option):
    """
    European-style option (can only be exercised at maturity).
    """
    
    def can_exercise_early(self) -> bool:
        """
        European options cannot be exercised early.
        
        Returns:
            False
        """
        return False
