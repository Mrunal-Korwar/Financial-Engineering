# Financial Engineering

Options pricing system using binomial tree models for vanilla European and American options.

## Features

- **Cox-Ross-Rubinstein (CRR) binomial model** for option pricing
- Support for **European and American style** options
- **Call and Put** options
- **Continuous dividend yield** modeling
- Flexible input via **command-line arguments** or **JSON configuration files**
- **Early exercise boundary** detection for American options
- JSON export capability

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Financial-Engineering
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Using Configuration Files

Price an option using a JSON configuration file:

```bash
python main.py --config config_example.json
```

For detailed output including parameters and early exercise boundary:

```bash
python main.py --config config_example.json --verbose
```

### Using Command-Line Arguments

Price an option by specifying all parameters on the command line:

```bash
python main.py --r 0.05 --sigma 0.25 --q 0.02 --S0 100 --K 100 --T 1.0 --option-type call --option-style american
```

### Mixing Config and CLI

Use a config file and override specific parameters:

```bash
python main.py --config config_example.json --K 105 --T 0.5
```

### Export Results

Export pricing results to a JSON file:

```bash
python main.py --config config_example.json --export-json result.json
```

## Configuration File Format

Create a JSON file with the following structure:

```json
{
  "option_parameters": {
    "interest_rate": 0.05,
    "volatility": 0.25,
    "dividend_yield": 0.02,
    "initial_stock_price": 100.0,
    "strike_price": 100.0,
    "time_to_maturity": 1.0,
    "number_of_periods": 252,
    "option_type": "call",
    "option_style": "american"
  }
}
```

### Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `interest_rate` | Annual interest rate (e.g., 0.05 for 5%) | Yes |
| `volatility` | Annual volatility (e.g., 0.25 for 25%) | Yes |
| `dividend_yield` | Continuous dividend yield (e.g., 0.02 for 2%) | Yes |
| `initial_stock_price` | Current stock price | Yes |
| `strike_price` | Option strike price | Yes |
| `time_to_maturity` | Time to maturity in years | Yes |
| `number_of_periods` | Number of binomial tree periods | No (default: T × 252) |
| `option_type` | "call" or "put" | Yes |
| `option_style` | "european" or "american" | Yes |

## Examples

### American Call Option

```bash
python main.py \
  --r 0.05 \
  --sigma 0.25 \
  --q 0.02 \
  --S0 100 \
  --K 100 \
  --T 1.0 \
  --N 252 \
  --option-type call \
  --option-style american \
  --verbose
```

### European Put Option

```bash
python main.py --config config_european_put.json --verbose
```

### American Put with Early Exercise

```bash
python main.py --config config_american_put.json --verbose
```

## Output

### Basic Output
```
Option Fair Value: $12.3456
```

### Detailed Output (--verbose)
```
============================================================
OPTIONS PRICING RESULT
============================================================

Model: CRR Binomial

Option Specification:
  Type: American Call
  Strike Price (K): $100.00
  Time to Maturity (T): 1.0000 years

Market Parameters:
  Initial Stock Price (S0): $100.00
  Interest Rate (r): 5.00%
  Volatility (sigma): 25.00%
  Dividend Yield (q): 2.00%

Model Parameters:
  Number of Periods (N): 252
  Time Step (dt): 0.003968 years

============================================================
FAIR VALUE: $12.3456
============================================================

Early Exercise Boundary:
------------------------------------------------------------
Time Step    Time (Years)    Stock Price Range         Nodes
------------------------------------------------------------
50           0.1984          $115.23 - $118.45         3
100          0.3968          $118.45 - $122.10         5
...
```

## Project Structure

```
Financial-Engineering/
├── main.py                      # Main entry point
├── requirements.txt             # Python dependencies
├── config_example.json          # Example configuration
├── options_pricing/             # Main package
│   ├── models/                  # Pricing models
│   │   ├── binomial.py         # CRR binomial implementation
│   │   └── tree.py             # Tree data structure
│   ├── instruments/             # Financial instruments
│   │   ├── option.py           # Base option class
│   │   ├── european.py         # European options
│   │   └── american.py         # American options
│   ├── core/                    # Core utilities
│   │   ├── parameters.py       # Parameter management
│   │   ├── validators.py       # Validation functions
│   │   └── constants.py        # Constants and enums
│   ├── io/                      # Input/Output
│   │   ├── cli_parser.py       # CLI argument parsing
│   │   ├── config_loader.py    # JSON config loader
│   │   └── output_formatter.py # Output formatting
│   └── utils/                   # Utilities
│       ├── calculations.py     # Helper functions
│       └── exceptions.py       # Custom exceptions
└── tests/                       # Test suite
```

## Model Information

### Cox-Ross-Rubinstein (CRR) Binomial Model

The CRR model uses the following parametrization:

- **Up factor**: u = exp(σ√Δt)
- **Down factor**: d = 1/u
- **Risk-neutral probability**: p = (exp((r-q)Δt) - d) / (u - d)
- **Discount factor**: exp(-rΔt)

The model builds a binomial tree of stock prices and uses backward induction to calculate the option value, checking for optimal early exercise at each node for American options.

### Convergence

As the number of periods (N) increases, the binomial model converges to the Black-Scholes price for European options. For American options, the model provides accurate pricing with early exercise boundaries.


