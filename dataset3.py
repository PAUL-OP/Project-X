import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset (default separator is comma for CSV, so '\t' is removed)
df = pd.read_csv('AnnualTicketSales.csv')

# --- Data Cleaning ---
# Clean 'AVERAGE TICKET PRICE': remove '$', remove commas, and convert to float
df['AVERAGE TICKET PRICE'] = (
    df['AVERAGE TICKET PRICE'].astype(str)
    .str.replace('$', '', regex=False)
    .str.replace(',', '', regex=False)
    .astype(float)
)

# The following lines are removed as they were not needed:
# df_exploded = df.assign(Year=df['YEAR'].str.split(',')).explode('YEAR')
# df_exploded['YEAR'] = df_exploded['Year'].str.strip()

# Calculate the mean ticket price for each YEAR
# (Since the data is already aggregated by year, this returns the original price)
YEAR_avg_price = df.groupby('YEAR')['AVERAGE TICKET PRICE'].mean().sort_values(ascending=False)

# Convert the resulting Series to a DataFrame for plotting and printing
YEAR_avg_price_df = YEAR_avg_price.reset_index()
YEAR_avg_price_df.columns = ['YEAR', 'AVERAGE TICKET PRICE']

# --- Plotting ---
plt.figure(figsize=(12, 7))

# Convert YEAR to string for plotting to ensure proper categorical display
plt.bar(YEAR_avg_price_df['YEAR'].astype(str), YEAR_avg_price_df['AVERAGE TICKET PRICE'], color='skyblue')

# Corrected Title and Labels
plt.title('Average Ticket Price by Year', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Average Ticket Price ($)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot (corrected file name)
plt.savefig('average_ticket_price_by_year.png')

# Optional: Print the results
print(YEAR_avg_price_df.to_string())