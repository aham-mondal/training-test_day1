# Trade Compliance Checker

## Overview
A Python-based application that checks financial trade orders against predefined portfolio and compliance rules. It validates trades and assigns a compliance decision based on portfolio restrictions, cash availability, holdings, and position concentration.

## Features
- Validates trade quantity, price, and action.
- Checks restricted securities.
- Verifies sufficient holdings for sell orders.
- Checks available cash for buy orders.
- Evaluates portfolio position concentration.
- Generates automated compliance decisions.
- Exports results to a CSV file.

## Technologies Used
- Python 3
- Pandas
- CSV

## Project Structure
```text
training-test_day1/
├── main.py
├── trades_test.csv
├── trade_compliance_results.csv
└── README.md
```

## Installation

Install the required dependency:

```bash
pip install pandas
```

## Usage

Place your input file (`trades_test.csv`) in the project directory and run:

```bash
python main.py
```

## Compliance Decisions

| Decision | Description |
|---|---|
| Approved | Trade passes all checks |
| Rejected | Trade violates compliance rules |
| Needs Manual Sign-off | Requires additional review |

## Output

The application generates `trade_compliance_results.csv`, containing the original trade details along with the compliance decision and reason.

## Author
Aham Mondal