"""
JSON configuration file loader.
"""

import json
from pathlib import Path
from typing import Dict, Any
from options_pricing.core.parameters import OptionParameters
from options_pricing.core.constants import OptionType, OptionStyle
from options_pricing.utils.exceptions import ConfigurationError


class ConfigLoader:
    """
    Load option parameters from JSON configuration file.
    """
    
    @staticmethod
    def load(filepath: str) -> OptionParameters:
        """
        Load and parse JSON configuration file.
        
        Args:
            filepath: Path to JSON configuration file
        
        Returns:
            OptionParameters object
        
        Raises:
            ConfigurationError: If file cannot be loaded or is invalid
        """
        # Check file exists
        path = Path(filepath)
        if not path.exists():
            raise ConfigurationError(f"Configuration file not found: {filepath}")
        
        # Load JSON
        try:
            with open(path, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error reading configuration file: {e}")
        
        # Validate and extract parameters
        try:
            params = ConfigLoader._extract_parameters(config)
            return params
        except Exception as e:
            raise ConfigurationError(f"Error parsing configuration: {e}")
    
    @staticmethod
    def _extract_parameters(config: Dict[str, Any]) -> OptionParameters:
        """
        Extract option parameters from configuration dictionary.
        
        Args:
            config: Configuration dictionary
        
        Returns:
            OptionParameters object
        
        Raises:
            KeyError: If required keys are missing
            ValueError: If parameter values are invalid
        """
        # Get nested option_parameters dict
        if 'option_parameters' in config:
            params = config['option_parameters']
        else:
            # Assume top-level config is the parameters
            params = config
        
        # Extract required parameters
        r = params['interest_rate']
        sigma = params['volatility']
        q = params['dividend_yield']
        S0 = params['initial_stock_price']
        K = params['strike_price']
        T = params['time_to_maturity']
        
        # Extract option type and style
        option_type_str = params['option_type']
        option_style_str = params['option_style']
        
        # Convert to enums
        option_type = OptionType.from_string(option_type_str)
        option_style = OptionStyle.from_string(option_style_str)
        
        # Extract optional number of periods
        N = params.get('number_of_periods', None)
        
        # Create parameters object
        return OptionParameters(
            r=r,
            sigma=sigma,
            q=q,
            S0=S0,
            K=K,
            T=T,
            option_type=option_type,
            option_style=option_style,
            N=N
        )
    
    @staticmethod
    def merge_with_cli(parameters: OptionParameters, args) -> OptionParameters:
        """
        Merge CLI arguments with config-loaded parameters (CLI overrides).
        
        Args:
            parameters: Parameters loaded from config
            args: Parsed CLI arguments
        
        Returns:
            Updated OptionParameters object
        """
        # Override with CLI values if provided
        if args.r is not None:
            parameters.r = args.r
        if args.sigma is not None:
            parameters.sigma = args.sigma
        if args.q is not None:
            parameters.q = args.q
        if args.S0 is not None:
            parameters.S0 = args.S0
        if args.K is not None:
            parameters.K = args.K
        if args.T is not None:
            parameters.T = args.T
        if args.N is not None:
            parameters.N = args.N
        if hasattr(args, 'option_type') and args.option_type is not None:
            parameters.option_type = OptionType.from_string(args.option_type)
        if hasattr(args, 'option_style') and args.option_style is not None:
            parameters.option_style = OptionStyle.from_string(args.option_style)
        
        return parameters
