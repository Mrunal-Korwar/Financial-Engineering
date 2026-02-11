"""
Command-line argument parser for options pricing.
"""

import argparse
from typing import Optional
from options_pricing.core.parameters import OptionParameters
from options_pricing.core.constants import OptionType, OptionStyle


class CLIParser:
    """
    Parse command-line arguments for option pricing.
    """
    
    def __init__(self):
        """Initialize CLI parser."""
        self.parser = self._build_parser()
    
    def _build_parser(self) -> argparse.ArgumentParser:
        """
        Build argument parser.
        
        Returns:
            Configured ArgumentParser
        """
        parser = argparse.ArgumentParser(
            description="Price financial options using binomial tree model",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Using config file
  python main.py --config config.json
  
  # Using command-line arguments
  python main.py --r 0.05 --sigma 0.25 --q 0.02 --S0 100 --K 100 --T 1.0 --option-type call --option-style american
  
  # Mix of config and CLI (CLI overrides config)
  python main.py --config config.json --K 105 --T 0.5
            """
        )
        
        # Config file (optional)
        parser.add_argument(
            '--config',
            type=str,
            help='Path to JSON configuration file'
        )
        
        # Option parameters
        parser.add_argument('--r', type=float, help='Annual interest rate')
        parser.add_argument('--sigma', type=float, help='Annual volatility')
        parser.add_argument('--q', type=float, help='Continuous dividend yield')
        parser.add_argument('--S0', type=float, help='Initial stock price')
        parser.add_argument('--K', type=float, help='Strike price')
        parser.add_argument('--T', type=float, help='Time to maturity (years)')
        parser.add_argument('--N', type=int, help='Number of periods (default: T * 252)')
        parser.add_argument(
            '--option-type',
            type=str,
            choices=['call', 'put'],
            help='Option type: call or put'
        )
        parser.add_argument(
            '--option-style',
            type=str,
            choices=['european', 'american'],
            help='Option style: european or american'
        )
        
        # Optional flags
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Display detailed output'
        )
        parser.add_argument(
            '--export-json',
            type=str,
            metavar='FILE',
            help='Export result to JSON file'
        )
        
        return parser
    
    def parse(self):
        """
        Parse command-line arguments.
        
        Returns:
            Parsed arguments namespace
        """
        return self.parser.parse_args()
    
    def create_parameters_from_args(self, args) -> OptionParameters:
        """
        Create OptionParameters from parsed arguments.
        
        Args:
            args: Parsed arguments from argparse
        
        Returns:
            OptionParameters object
        
        Raises:
            ValueError: If required parameters are missing
        """
        # Check that all required parameters are present
        required_params = ['r', 'sigma', 'q', 'S0', 'K', 'T', 'option_type', 'option_style']
        missing = [p for p in required_params if getattr(args, p.replace('-', '_'), None) is None]
        
        if missing and not args.config:
            raise ValueError(
                f"Missing required parameters: {', '.join(missing)}. "
                "Either provide --config or all required parameters."
            )
        
        # Convert string option type and style to enums
        option_type = OptionType.from_string(args.option_type)
        option_style = OptionStyle.from_string(args.option_style)
        
        # Create parameters object
        return OptionParameters(
            r=args.r,
            sigma=args.sigma,
            q=args.q,
            S0=args.S0,
            K=args.K,
            T=args.T,
            option_type=option_type,
            option_style=option_style,
            N=args.N
        )
