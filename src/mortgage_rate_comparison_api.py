from flask import Flask, request, jsonify
import numpy_financial as npf

app = Flask(__name__)

# Define the calculation logic
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

# API route to calculate balance
@app.route('/calculate_balance', methods=['POST'])
def calculate_balance_api():
    try:
        # Get data from the POST request
        data = request.json
        principal = data.get('principal')
        term_years = data.get('term_years')
        interest_rates = data.get('interest_rates')
        period_years = data.get('period_years')
        
        if not all([principal, term_years, interest_rates, period_years]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Call the balance calculation function
        balances = calculate_balance(principal, term_years, interest_rates, period_years)
        
        # Return the result as JSON
        return jsonify({"balances": balances}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
