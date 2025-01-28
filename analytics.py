import pandas as pd

# Load the datasets
user_ratings = pd.read_csv('UserRatings.csv')
movies = pd.read_csv('Movies.csv')

# Ensure the columns have the same data type
user_ratings['MOVIE_ID'] = user_ratings['MOVIE_ID'].astype(str)
movies['ID_MOVIE'] = movies['ID_MOVIE'].astype(str)

# Merge the datasets on MOVIE_ID and ID_MOVIE
merged_data = pd.merge(user_ratings, movies, left_on='MOVIE_ID', right_on='ID_MOVIE')

# Calculate the number of ratings, average, max, min, and standard deviation for each movie
movie_stats = merged_data.groupby('MOVIE_TITLE')['RATING'].agg(
    num_ratings='count',
    avg_rating='mean',
    max_rating='max',
    min_rating='min',
    std_rating='std'
).reset_index()

# Display the statistics
print("Movie Statistics:")
print(movie_stats)

# Identify the 3 best and worst movies based on average rating
top_3_movies = movie_stats.nlargest(3, 'avg_rating')[['MOVIE_TITLE', 'avg_rating']]
bottom_3_movies = movie_stats.nsmallest(3, 'avg_rating')[['MOVIE_TITLE', 'avg_rating']]

print("\nTop 3 Movies:")
print(top_3_movies)

print("\nBottom 3 Movies:")
print(bottom_3_movies)

# Determine how many movies have ratings in the same year as their release
# Fix: Specify the correct date format for RATING_DATE
merged_data['RATING_YEAR'] = pd.to_datetime(merged_data['RATING_DATE'], format='%d/%m/%Y').dt.year
same_year_ratings = merged_data[merged_data['MOVIE_YEAR'] == merged_data['RATING_YEAR']]
num_same_year = same_year_ratings['MOVIE_ID'].nunique()
avg_rating_same_year = same_year_ratings['RATING'].mean()

print(f"\nNumber of movies with ratings in the same year as release: {num_same_year}")
print(f"Average rating in the year of release: {avg_rating_same_year:.2f}")

# Analyze the trend of average ratings in subsequent years
yearly_avg_ratings = merged_data.groupby('RATING_YEAR')['RATING'].mean().reset_index()
yearly_avg_ratings['rating_change'] = yearly_avg_ratings['RATING'].diff()

print("\nYearly Average Ratings and Changes:")
print(yearly_avg_ratings)