"""
Output formatting for pricing results.
"""

import json
from typing import Dict, Any
from options_pricing.core.parameters import OptionParameters


class OutputFormatter:
    """
    Format option pricing results for display.
    """
    
    @staticmethod
    def format_basic_result(result: Dict[str, Any]) -> str:
        """
        Format basic pricing result (price only).
        
        Args:
            result: Pricing result dictionary
        
        Returns:
            Formatted result string
        """
        price = result['price']
        parameters = result['parameters']
        
        output = f"\nOption Fair Value: ${price:.4f}\n"
        return output
    
    @staticmethod
    def format_detailed_result(result: Dict[str, Any]) -> str:
        """
        Format detailed pricing result with all parameters.
        
        Args:
            result: Pricing result dictionary
        
        Returns:
            Formatted result string
        """
        price = result['price']
        parameters = result['parameters']
        model = result.get('model', 'Unknown')
        
        # Header
        output = "\n" + "="*60 + "\n"
        output += "OPTIONS PRICING RESULT\n"
        output += "="*60 + "\n\n"
        
        # Model info
        output += f"Model: {model}\n\n"
        
        # Option specification
        output += "Option Specification:\n"
        output += f"  Type: {parameters.option_style.value.title()} {parameters.option_type.value.title()}\n"
        output += f"  Strike Price (K): ${parameters.K:.2f}\n"
        output += f"  Time to Maturity (T): {parameters.T:.4f} years\n\n"
        
        # Market parameters
        output += "Market Parameters:\n"
        output += f"  Initial Stock Price (S0): ${parameters.S0:.2f}\n"
        output += f"  Interest Rate (r): {parameters.r*100:.2f}%\n"
        output += f"  Volatility (sigma): {parameters.sigma*100:.2f}%\n"
        output += f"  Dividend Yield (q): {parameters.q*100:.2f}%\n\n"
        
        # Model parameters
        output += "Model Parameters:\n"
        output += f"  Number of Periods (N): {parameters.N}\n"
        output += f"  Time Step (dt): {parameters.T/parameters.N:.6f} years\n\n"
        
        # Result
        output += "="*60 + "\n"
        output += f"FAIR VALUE: ${price:.4f}\n"
        output += "="*60 + "\n"
        
        # Early exercise boundary if applicable
        if 'early_exercise_boundary' in result:
            boundary = result['early_exercise_boundary']
            if boundary:
                output += "\nEarly Exercise Boundary:\n"
                output += "-"*60 + "\n"
                output += f"{'Time Step':<12} {'Time (Years)':<15} {'Stock Price Range':<25} {'Nodes':<8}\n"
                output += "-"*60 + "\n"
                
                for point in boundary:
                    time_step = point['time_step']
                    time_years = point['time_years']
                    min_price = point['min_stock_price']
                    max_price = point['max_stock_price']
                    num_nodes = point['num_nodes']
                    
                    price_range = f"${min_price:.2f} - ${max_price:.2f}"
                    output += f"{time_step:<12} {time_years:<15.4f} {price_range:<25} {num_nodes:<8}\n"
                
                output += "\n"
        
        return output
    
    @staticmethod
    def export_to_json(result: Dict[str, Any], filepath: str) -> None:
        """
        Export pricing result to JSON file.
        
        Args:
            result: Pricing result dictionary
            filepath: Output file path
        """
        # Prepare export data (exclude tree object)
        export_data = {
            'price': result['price'],
            'model': result.get('model'),
            'parameters': result['parameters'].to_dict()
        }
        
        # Add early exercise boundary if present
        if 'early_exercise_boundary' in result:
            export_data['early_exercise_boundary'] = result['early_exercise_boundary']
        
        # Write to file
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
