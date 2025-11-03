import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('action.csv')

# Split the 'genre' column by comma, expand into a list, and then "explode" the DataFrame
df_exploded = df.assign(genre=df['genre'].str.split(',')).explode('genre')

# Clean up whitespace from the genre names
df_exploded['genre'] = df_exploded['genre'].str.strip()

# Calculate the mean rating for each genre
genre_ratings = df_exploded.groupby('genre')['rating'].mean().sort_values(ascending=False)

# Convert the resulting Series to a DataFrame for plotting and printing
genre_ratings_df = genre_ratings.reset_index()
genre_ratings_df.columns = ['Genre', 'Average Rating']

# --- Plotting ---

plt.figure(figsize=(12, 7))
plt.bar(genre_ratings_df['Genre'], genre_ratings_df['Average Rating'], color='skyblue')

plt.title('Average Movie Rating by Genre', fontsize=16)
plt.xlabel('Genre', fontsize=12)
plt.ylabel('Average Rating', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot
plt.savefig('average_rating_by_genre.png')