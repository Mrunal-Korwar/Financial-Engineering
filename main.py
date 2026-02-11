#!/usr/bin/env python3
"""
Options Pricing System - Main Entry Point

Price financial options using binomial tree models.

Usage:
    python main.py --config config.json
    python main.py --r 0.05 --sigma 0.25 --q 0.02 --S0 100 --K 100 --T 1.0 --option-type call --option-style american
"""

import sys
from options_pricing.io.cli_parser import CLIParser
from options_pricing.io.config_loader import ConfigLoader
from options_pricing.io.output_formatter import OutputFormatter
from options_pricing.models.binomial import CRRBinomialModel
from options_pricing.instruments.european import EuropeanOption
from options_pricing.instruments.american import AmericanOption
from options_pricing.core.constants import OptionStyle
from options_pricing.utils.exceptions import OptionPricingError


def main():
    """
    Main execution function.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Parse command-line arguments
        cli_parser = CLIParser()
        args = cli_parser.parse()
        
        # Load parameters
        if args.config:
            # Load from config file
            parameters = ConfigLoader.load(args.config)
            # Merge with CLI overrides if any are provided
            parameters = ConfigLoader.merge_with_cli(parameters, args)
        else:
            # Create from CLI arguments only
            parameters = cli_parser.create_parameters_from_args(args)
        
        # Validate parameters
        parameters.validate()
        
        # Create option object based on style
        if parameters.option_style == OptionStyle.EUROPEAN:
            option = EuropeanOption(parameters.K, parameters.option_type)
        else:  # AMERICAN
            option = AmericanOption(parameters.K, parameters.option_type)
        
        # Create pricing model
        model = CRRBinomialModel()
        
        # Calculate price
        result = model.price(option, parameters)
        
        # Format and display output
        formatter = OutputFormatter()
        if args.verbose:
            output = formatter.format_detailed_result(result)
        else:
            output = formatter.format_basic_result(result)
        
        print(output)
        
        # Export to JSON if requested
        if args.export_json:
            formatter.export_to_json(result, args.export_json)
            print(f"Result exported to: {args.export_json}")
        
        return 0
        
    except OptionPricingError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
