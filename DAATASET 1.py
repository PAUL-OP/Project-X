import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('action.csv')


df_exploded = df.assign(genre=df['genre'].str.split(',')).explode('genre')


df_exploded['genre'] = df_exploded['genre'].str.strip()


genre_ratings = df_exploded.groupby('genre')['rating'].mean().sort_values(ascending=False)


genre_ratings_df = genre_ratings.reset_index()
genre_ratings_df.columns = ['Genre', 'Average Rating']



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
