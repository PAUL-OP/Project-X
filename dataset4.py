import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Data Loading and Cleaning ---

# 1. Load the dataset
try:
    # The file name 'TopDistributors.csv' is accessible in the environment
    df = pd.read_csv('TopDistributors.csv')
    print("Successfully loaded TopDistributors.csv")
except FileNotFoundError:
    print("Error: TopDistributors.csv not found. Please ensure the file is correctly uploaded.")
    exit()

# 2. Clean 'TOTAL GROSS' and 'AVERAGE GROSS' columns
# Remove '$' and ',' characters, then convert to integer
def clean_currency(col):
    if df[col].dtype == 'object':
        return df[col].astype(str).str.replace(r'[$,]', '', regex=True).astype(np.int64)
    return df[col]

df['TOTAL_GROSS_CLEAN'] = clean_currency('TOTAL GROSS')
df['AVERAGE_GROSS_CLEAN'] = clean_currency('AVERAGE GROSS')

# 3. Clean 'MARKET SHARE' column
# Remove '%' character, convert to float, and divide by 100
df['MARKET_SHARE_CLEAN'] = df['MARKET SHARE'].astype(str).str.replace('%', '', regex=False).astype(float) / 100

# 4. Ensure 'MOVIES' is numeric (it seems clean, but good practice to ensure)
df['MOVIES'] = pd.to_numeric(df['MOVIES'], errors='coerce')


# --- Visualization ---

# Set up the figure and axes for three subplots
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))
plt.style.use('seaborn-v0_8-darkgrid') # Apply a clean style

# --- Plot 1: Bar Chart for Total Gross ---
ax0 = axes[0]
distributors = df['DISTRIBUTORS']
total_gross = df['TOTAL_GROSS_CLEAN']

# Create a color map based on rank (lower rank = darker color)
colors = plt.cm.plasma(np.linspace(0.2, 0.9, len(distributors)))

ax0.bar(distributors, total_gross, color=colors)
ax0.set_title('Total Box Office Gross by Distributor (Bar Chart)', fontsize=14, fontweight='bold')
ax0.set_ylabel('Total Gross (in Billions)')
# Format y-axis to show in billions
ax0.ticklabel_format(style='plain', axis='y')
ax0.set_yticklabels([f'{int(y/1e9)}B' for y in ax0.get_yticks()])
ax0.tick_params(axis='x', rotation=45, labelsize=10)
ax0.grid(axis='y', linestyle='--', alpha=0.7)


# --- Plot 2: Pie Chart for Market Share ---
ax1 = axes[1]
market_share = df['MARKET_SHARE_CLEAN'] * 100  # Convert back to percentage for display
labels = df['DISTRIBUTORS']

# FIX: Dynamically create the explode tuple based on the number of distributors.
# We explode the first slice (index 0) and leave the rest unexploded (0).
num_distributors = len(distributors)
# Create a list/array of zeros, and set the first element to 0.1
explode_list = [0] * num_distributors
if num_distributors > 0:
    explode_list[0] = 0.1
explode = tuple(explode_list)

# Use autopct to format the percentages (1 decimal place)
ax1.pie(
    market_share,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=explode,
    shadow=True,
    wedgeprops={'edgecolor': 'black', 'linewidth': 0.5}
)
ax1.set_title('Market Share Distribution (Pie Chart)', fontsize=14, fontweight='bold')
ax1.axis('equal')  # Ensures the pie is drawn as a circle.


# --- Plot 3: Scatter Plot (Movies vs. Average Gross) ---
ax2 = axes[2]
movies_count = df['MOVIES']
avg_gross = df['AVERAGE_GROSS_CLEAN']

# Use Total Gross for marker size (scaled down) for a third dimension of data
# Scatter plot: X=Number of Movies, Y=Average Gross, Size=Total Gross
sizes = df['TOTAL_GROSS_CLEAN'] / 1e8 # Scale down total gross for marker size
scatter = ax2.scatter(
    movies_count,
    avg_gross,
    s=sizes,
    c=df['RANK'],
    cmap='viridis',
    alpha=0.7,
    edgecolors='w',
    linewidths=1
)

ax2.set_title('Average Gross vs. Number of Movies', fontsize=14, fontweight='bold')
ax2.set_xlabel('Number of Movies Distributed')
ax2.set_ylabel('Average Gross Per Movie')
ax2.grid(True, linestyle=':', alpha=0.6)

# Format y-axis to show Average Gross with currency style
ax2.ticklabel_format(style='plain', axis='y')
ax2.set_yticklabels([f'${int(y/1e6)}M' for y in ax2.get_yticks()])

# Add labels to the points (Distributor name)
for i, name in enumerate(distributors):
    ax2.annotate(
        name,
        (movies_count[i], avg_gross[i]),
        textcoords="offset points",
        xytext=(5, 5),
        ha='left',
        fontsize=8,
        alpha=0.8
    )

# Create a colorbar for the rank
cbar = fig.colorbar(scatter, ax=ax2)
cbar.set_label('Distributor Rank (1 is highest)')


# Adjust layout to prevent subplot titles and labels from overlapping
plt.tight_layout(pad=3.0)

# Display the final plot
plt.show()

print("\nData preparation and plotting complete. Three charts have been generated:")
print("1. Bar Chart: Total Gross by Distributor.")
print("2. Pie Chart: Market Share Distribution.")
print("3. Scatter Plot: Average Gross vs. Number of Movies (Size of dot represents Total Gross).")