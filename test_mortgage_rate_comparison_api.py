import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the API URL
url = 'http://127.0.0.1:5000/calculate_balance'

# Define multiple scenarios with principal, term_years, interest rates, and periods
scenarios = [
    {
        "name": "Scenario 1: 5 years at 4.3%, then 25 years at 6.0%",
        "data": {
            "principal": 100000,
            "term_years": 30,
            "interest_rates": [4.3, 6.0],
            "period_years": [5, 25]
        }
    },
    {
        "name": "Scenario 2: 2 years at 4.8%, 2 years at 3.5%, 2 years at 3.0%, then 24 years at 6.0%",
        "data": {
            "principal": 100000,
            "term_years": 30,
            "interest_rates": [4.8, 3.5, 3.0, 6.0],
            "period_years": [2, 2, 2, 24]
        }
    },
    {
        "name": "Scenario 3: 2 years at 4.8%, 2 years at 5.5%, 2 years at 5.5%, then 24 years at 6.0%",
        "data": {
            "principal": 100000,
            "term_years": 30,
            "interest_rates": [4.8, 5.5, 5.5, 6.0],
            "period_years": [2, 2, 2, 24]
        }
    }
]

# Store the results of the balances for plotting
results = []

# Loop through each scenario and send POST requests
for scenario in scenarios:
    response = requests.post(url, json=scenario["data"])
    if response.status_code == 200:
        balances = response.json()["balances"]
        results.append({
            "name": scenario["name"],
            "balances": balances[:60]  # We are only interested in the first 5 years (60 months)
        })
    else:
        print(f"Error in {scenario['name']}: {response.text}")

# Prepare the data for seaborn
data = []
months = np.arange(60)  # First 5 years (60 months)

for result in results:
    for month, balance in zip(months, result["balances"]):
        data.append({
            "Month": month,
            "Balance": balance,
            "Scenario": result["name"]
        })

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(data)

# Set Seaborn style
sns.set_theme(style="whitegrid")

# Set a color palette
palette = sns.color_palette("husl", len(scenarios))

# Create the seaborn lineplot with markers
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x="Month", y="Balance", hue="Scenario", palette=palette, linewidth=2.5, marker='o')

# Customize the plot
plt.title("Mortgage Balance Over the First 5 Years for Different Scenarios", fontsize=18, weight='bold')
plt.xlabel("Months", fontsize=14)
plt.ylabel("Remaining Balance (£)", fontsize=14)

# Improve the legend
plt.legend(title="Scenarios", fontsize=12, title_fontsize=14, loc='upper right')

# Set larger ticks
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Add grid
plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7)

# Show the plot
plt.tight_layout()
plt.show()
