"""
Binomial tree data structure for option pricing.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any


class BinomialTree:
    """
    Data structure for storing binomial tree values.
    
    Stores stock prices, option values, and early exercise flags
    at each node in the tree.
    
    Attributes:
        N: Number of periods (time steps)
        stock_prices: Stock price at each node S[i, j]
        option_values: Option value at each node V[i, j]
        exercise_flags: Early exercise flag at each node (boolean)
    
    Node indexing: (i, j) where i = time step (0 to N), j = up moves (0 to i)
    """
    
    def __init__(self, N: int):
        """
        Initialize empty binomial tree.
        
        Args:
            N: Number of periods
        """
        self.N = N
        # Arrays of shape (N+1, N+1) to accommodate all nodes
        self.stock_prices = np.zeros((N + 1, N + 1))
        self.option_values = np.zeros((N + 1, N + 1))
        self.exercise_flags = np.zeros((N + 1, N + 1), dtype=bool)
    
    def get_early_exercise_boundary(self, dt: float) -> List[Dict[str, Any]]:
        """
        Extract early exercise boundary from the tree.
        
        The boundary represents the set of stock prices at each time step
        where early exercise is optimal.
        
        Args:
            dt: Time step size in years
        
        Returns:
            List of dictionaries with boundary information at each time step
        """
        boundary = []
        
        for i in range(self.N + 1):
            # Find all nodes at time step i where early exercise is optimal
            exercise_prices = []
            for j in range(i + 1):
                if self.exercise_flags[i, j]:
                    exercise_prices.append(self.stock_prices[i, j])
            
            # If there are early exercise points at this time step, record them
            if exercise_prices:
                boundary.append({
                    'time_step': i,
                    'time_years': round(i * dt, 4),
                    'min_stock_price': round(min(exercise_prices), 4),
                    'max_stock_price': round(max(exercise_prices), 4),
                    'num_nodes': len(exercise_prices)
                })
        
        return boundary
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert stock prices to pandas DataFrame for visualization.
        
        Returns:
            DataFrame with stock prices at each node
        """
        data = []
        for i in range(self.N + 1):
            for j in range(i + 1):
                data.append({
                    'time_step': i,
                    'up_moves': j,
                    'stock_price': self.stock_prices[i, j],
                    'option_value': self.option_values[i, j],
                    'early_exercise': self.exercise_flags[i, j]
                })
        return pd.DataFrame(data)
