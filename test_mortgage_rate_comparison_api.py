import requests

url = 'http://127.0.0.1:5000/calculate_balance'

# Define the data for the POST request
data = {
    "principal": 100000,
    "term_years": 30,
    "interest_rates": [4.3, 6.0],
    "period_years": [5, 25]
}

# Send the POST request
response = requests.post(url, json=data)

# Print the response from the API
if response.status_code == 200:
    print("Balances:", response.json())
else:
    print("Error:", response.text)
