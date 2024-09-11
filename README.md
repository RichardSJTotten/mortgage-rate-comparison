# Flask API for Balance Calculation

This project provides a Flask API to calculate the remaining balance of a loan or investment over time, considering varying interest rates.

## Code Explanation

### Imports

```python
from flask import Flask, request, jsonify
import numpy_financial as npf
```

- `Flask`: Used to create the web application.
- `request` and `jsonify`: Handle API requests and responses.
- `numpy_financial`: Provides financial functions, including `pmt`, for calculating payment amounts.

### Flask Application Setup

```python
app = Flask(__name__)
```

Creates an instance of the Flask application.

### Balance Calculation Logic

```python
def calculate_balance(principal, term_years, interest_rates, period_years):
    term_months = term_years * 12
    balances = []
    current_balance = principal
    start_month = 0
    
    for rate, years in zip(interest_rates, period_years):
        monthly_rate = rate / 100 / 12
        period_months = years * 12
        remaining_term = term_months - start_month
        
        if current_balance <= 0:
            break
        
        # Calculate the monthly payment for the current period
        monthly_payment = npf.pmt(monthly_rate, remaining_term, -current_balance)
        
        for month in range(period_months):
            interest_payment = current_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            current_balance -= principal_payment
            balances.append(current_balance)
            start_month += 1
            
            if current_balance <= 0:
                break

    while start_month < term_months and current_balance > 0:
        interest_payment = current_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        current_balance -= principal_payment
        balances.append(current_balance)
        start_month += 1
    
    return balances
```

### How It Works

1. **Convert Term to Months**:
   ```python
   term_months = term_years * 12
   ```
2. **Initialize Variables**:
   ```python
   current_balance = principal
   start_month = 0
   ```

3. **Calculate Payments for Each Interest Rate Period**:
   For each interest rate and corresponding period:
   - **Monthly Rate**:
     ```python
     monthly_rate = rate / 100 / 12
     ```
   - **Monthly Payment**:
     ```python
     monthly_payment = npf.pmt(monthly_rate, remaining_term, -current_balance)
     ```
   - **Update Balance**:
     Each month:
     ```python
     interest_payment = current_balance * monthly_rate
     principal_payment = monthly_payment - interest_payment
     current_balance -= principal_payment
     ```

4. **Handle Remaining Months**:
   After all interest rate periods:
   ```python
   while start_month < term_months and current_balance > 0:
       interest_payment = current_balance * monthly_rate
       principal_payment = monthly_payment - interest_payment
       current_balance -= principal_payment
       start_month += 1
   ```

### Summary

The function tracks the balance month by month, adjusting for varying interest rates, and returns a list of remaining balances over time.

## Launching the Flask API in a Poetry Environment

To launch the Flask API using Poetry, follow these steps:

### Prerequisites

- Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed on your system.

### Setting Up the Environment

1. **Install Dependencies**:
   Navigate to the project directory where your `pyproject.toml` file is located and install the project dependencies using Poetry:

   ```bash
   poetry install
   ```

2. **Activate the Poetry Shell**:
   Start a new shell within the Poetry virtual environment:

   ```bash
   poetry shell
   ```

### Running the Flask Application

1. **Start the Flask Server**:
   With the Poetry shell active, run the Flask application:

   ```bash
   python your_script_name.py
   ```

   Replace `your_script_name.py` with the name of your Python file that contains the Flask application.

2. **Verify the Application**:
   The Flask server should start and be accessible at `http://127.0.0.1:5000/` by default. You can test the API endpoints using tools like `curl`, Postman, or your web browser.

### Example

To test the `/calculate_balance` endpoint, you can use `curl`:

```bash
curl -X POST http://127.0.0.1:5000/calculate_balance \
     -H "Content-Type: application/json" \
     -d '{"principal": 100000, "term_years": 30, "interest_rates": [5, 4.5], "period_years": [10, 20]}'
```

### Exiting the Poetry Shell

When you are done working, you can exit the Poetry shell by typing:

```bash
exit
```
