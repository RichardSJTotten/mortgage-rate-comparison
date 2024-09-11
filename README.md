# Flask Loan Balance Calculator

This Flask application provides an API endpoint to calculate the remaining balance of a loan or investment over time given certain parameters. It uses the `numpy_financial` library for financial calculations.

## Features

- **Balance Calculation**: Computes the remaining balance of a principal amount over a specified term, considering varying interest rates and periods.

## Requirements

- Python 3.x
- Flask
- numpy_financial

You can install the necessary Python libraries using pip:

```bash
pip install Flask numpy_financial
```

# Code Explanation

## Imports

```python
from flask import Flask, request, jsonify
import numpy_financial as npf
```

# Flask Application Setup

The Flask application is initialized and configured in this section. Here's a detailed breakdown of how the Flask application is set up:

## Creating the Flask Application Instance

```python
app = Flask(__name__)
```

# Balance Calculation Logic

The `calculate_balance` function determines the remaining balance of a loan or investment over time. Here's a breakdown of the key variables and how the function operates:

## Key Variables

- **`principal`**: The initial amount of the loan or investment.
- **`term_years`**: The total duration of the loan or investment in years.
- **`interest_rates`**: A list of annual interest rates for different periods.
- **`period_years`**: A list of years corresponding to each interest rate.

## How It Works

1. **Convert Term to Months**:
   ```python
   term_months = term_years * 12
   ```
- Converts the total loan term from years to months for calculation.
2. **Initialise Variables**:
   ```python
   current_balance = principal
   start_month = 0
   ```
- **`current_balance`**: starts as the initial amount.
- **`start_month`**: tracks how many months have passed.
3. **Calculate Payments for Each Interest Rate Period: For each interest rate and corresponding period:**:
- Monthly Rate
   ```python
   monthly_rate = rate / 100 / 12
   ```
- Converts the annual interest rate to a monthly rate.
- Monthly Payment
   ```python
   monthly_payment = npf.pmt(monthly_rate, remaining_term, -current_balance)
   ```
- Calculates the monthly payment amount based on the remaining balance and rate.
- Update Balance: Each month:
   ```python
   interest_payment = current_balance * monthly_rate
   principal_payment = monthly_payment - interest_payment
   current_balance -= principal_payment
   ```
- Calculates the interest and principal parts of the payment.
- Updates the balance by subtracting the principal payment.
4. **Handle Remaining Months: After all interest rate periods:**:
   ```python
   while start_month < term_months and current_balance > 0:
    interest_payment = current_balance * monthly_rate
    principal_payment = monthly_payment - interest_payment
    current_balance -= principal_payment
    start_month += 1
   ```
- Continues to update the balance until the end of the term or the balance reaches zero.

# Summary

The `calculate_balance` function provides a detailed monthly breakdown of the remaining balance for a loan or investment, considering different interest rates over time. 

## Key Points

- **Initial Setup**: The function starts with the initial principal and calculates the total term in months.
- **Interest Rate Handling**: For each interest rate period, it calculates the monthly payment and updates the balance each month.
- **Remaining Term**: After processing all specified periods, the function continues to update the balance until the end of the term or the balance reaches zero.

The result is a list of the remaining balances after each month, showing how the balance changes over time with varying interest rates.
