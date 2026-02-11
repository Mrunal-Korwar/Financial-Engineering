"""
Cox-Ross-Rubinstein (CRR) binomial model for option pricing.
"""

import numpy as np
from typing import Dict, Any, Tuple
from options_pricing.models.base import PricingModel
from options_pricing.models.tree import BinomialTree
from options_pricing.instruments.option import Option
from options_pricing.core.parameters import OptionParameters
from options_pricing.core.validators import validate_probability
from options_pricing.utils.exceptions import ModelError


class CRRBinomialModel(PricingModel):
    """
    Cox-Ross-Rubinstein binomial model for option pricing.
    
    Implements the CRR parametrization of the binomial tree:
    - u = exp(sigma * sqrt(dt))  [up factor]
    - d = 1/u  [down factor]
    - p = (exp((r-q)*dt) - d) / (u - d)  [risk-neutral probability]
    """
    
    def __init__(self):
        """Initialize CRR binomial model."""
        self.tree = None
        self._last_parameters = None
    
    def price(self, option: Option, parameters: OptionParameters) -> Dict[str, Any]:
        """
        Price option using CRR binomial tree.
        
        Args:
            option: Option to price
            parameters: Pricing parameters
        
        Returns:
            Dictionary with 'price', 'tree', and optionally 'early_exercise_boundary'
        
        Raises:
            ModelError: If pricing calculation fails
        """
        # Validate parameters
        parameters.validate()
        
        # Calculate CRR parameters
        dt, u, d, p, discount = self._calculate_crr_parameters(parameters)
        
        # Create tree
        self.tree = BinomialTree(parameters.N)
        
        # Build stock price tree (forward)
        self._build_stock_price_tree(parameters.S0, u, d, parameters.N)
        
        # Calculate terminal payoffs
        self._calculate_terminal_payoffs(option, parameters.N)
        
        # Backward induction
        self._backward_induction(option, p, discount, parameters.N)
        
        # Extract price
        price = self.tree.option_values[0, 0]
        
        # Prepare result
        result = {
            'price': price,
            'tree': self.tree,
            'model': 'CRR Binomial',
            'parameters': parameters
        }
        
        # Add early exercise boundary for American options
        if option.can_exercise_early():
            boundary = self.tree.get_early_exercise_boundary(dt)
            result['early_exercise_boundary'] = boundary
        
        self._last_parameters = parameters
        return result
    
    def _calculate_crr_parameters(
        self, 
        parameters: OptionParameters
    ) -> Tuple[float, float, float, float, float]:
        """
        Calculate CRR binomial model parameters.
        
        Args:
            parameters: Option parameters
        
        Returns:
            Tuple of (dt, u, d, p, discount)
        
        Raises:
            ModelError: If risk-neutral probability is out of valid range
        """
        # Time step
        dt = parameters.T / parameters.N
        
        # Up and down factors
        u = np.exp(parameters.sigma * np.sqrt(dt))
        d = 1 / u
        
        # Risk-neutral probability
        p = (np.exp((parameters.r - parameters.q) * dt) - d) / (u - d)
        
        # Validate risk-neutral probability
        try:
            validate_probability(p)
        except Exception as e:
            raise ModelError(
                f"Invalid risk-neutral probability {p:.6f}. "
                f"This may indicate extreme parameter values. "
                f"Original error: {str(e)}"
            )
        
        # Discount factor per period
        discount = np.exp(-parameters.r * dt)
        
        return dt, u, d, p, discount
    
    def _build_stock_price_tree(self, S0: float, u: float, d: float, N: int) -> None:
        """
        Build forward stock price tree.
        
        At node (i, j):
        - i = time step (0 to N)
        - j = number of up moves (0 to i)
        - S[i,j] = S0 * u^j * d^(i-j)
        
        Args:
            S0: Initial stock price
            u: Up factor
            d: Down factor
            N: Number of periods
        """
        for i in range(N + 1):
            for j in range(i + 1):
                self.tree.stock_prices[i, j] = S0 * (u ** j) * (d ** (i - j))
    
    def _calculate_terminal_payoffs(self, option: Option, N: int) -> None:
        """
        Calculate option values at maturity (time N).
        
        Args:
            option: Option to price
            N: Number of periods
        """
        for j in range(N + 1):
            S = self.tree.stock_prices[N, j]
            self.tree.option_values[N, j] = option.payoff(S)
    
    def _backward_induction(
        self, 
        option: Option, 
        p: float, 
        discount: float, 
        N: int
    ) -> None:
        """
        Perform backward induction through the tree.
        
        For each node (i, j) from N-1 back to 0:
        1. Calculate continuation value (expected discounted future value)
        2. Calculate intrinsic value (immediate exercise payoff)
        3. For American: take max(intrinsic, continuation)
        4. For European: use continuation only
        5. Mark early exercise nodes
        
        Args:
            option: Option to price
            p: Risk-neutral probability
            discount: Discount factor per period
            N: Number of periods
        """
        for i in range(N - 1, -1, -1):
            for j in range(i + 1):
                # Continuation value (expected discounted value from holding)
                continuation = discount * (
                    p * self.tree.option_values[i + 1, j + 1] +
                    (1 - p) * self.tree.option_values[i + 1, j]
                )
                
                # Intrinsic value (immediate exercise)
                S = self.tree.stock_prices[i, j]
                intrinsic = option.payoff(S)
                
                # Determine option value based on exercise style
                if option.can_exercise_early():
                    # American: can exercise early
                    self.tree.option_values[i, j] = max(intrinsic, continuation)
                    # Mark if early exercise is optimal
                    self.tree.exercise_flags[i, j] = (
                        intrinsic > continuation and intrinsic > 0
                    )
                else:
                    # European: must hold until maturity
                    self.tree.option_values[i, j] = continuation
                    self.tree.exercise_flags[i, j] = False
    
    def get_model_info(self) -> str:
        """
        Get information about the CRR binomial model.
        
        Returns:
            Model description
        """
        info = "Cox-Ross-Rubinstein (CRR) Binomial Model\n"
        info += "Parametrization:\n"
        info += "  u = exp(sigma * sqrt(dt))\n"
        info += "  d = 1/u\n"
        info += "  p = (exp((r-q)*dt) - d) / (u - d)\n"
        
        if self._last_parameters:
            dt = self._last_parameters.T / self._last_parameters.N
            info += f"\nLast pricing used:\n"
            info += f"  Time step (dt): {dt:.6f} years\n"
            info += f"  Periods (N): {self._last_parameters.N}\n"
        
        return info
