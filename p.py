import pandas as pd

# Cargar los datos de los archivos CSV
movies = pd.read_csv('Movies.csv', dayfirst=True)
user_ratings = pd.read_csv('UserRatings.csv')

# Renombrar las columnas para que coincidan con los nombres proporcionados
movies.columns = ['movie_id', 'user_id', 'rating', 'date']
user_ratings.columns = ['movie_id', 'release_year', 'name', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5']

# Eliminar las columnas innecesarias en el archivo de películas
user_ratings = user_ratings[['movie_id', 'release_year', 'name']]

# Asegurarse de que las columnas 'movie_id' tengan el mismo tipo de datos
movies['movie_id'] = movies['movie_id'].astype(str)
user_ratings['movie_id'] = user_ratings['movie_id'].astype(str)

# Convertir la columna 'date' a datetime y extraer el año
movies['date'] = pd.to_datetime(movies['date'], dayfirst=True)
movies['year'] = movies['date'].dt.year

# 1. Especificar la cantidad de calificaciones que tiene cada película, las calificaciones promedio, máximas, mínimas y su desviación.
ratings_summary = movies.groupby('movie_id')['rating'].agg(['count', 'mean', 'max', 'min', 'std']).reset_index()
ratings_summary = ratings_summary.merge(user_ratings, left_on='movie_id', right_on='movie_id')

# Filtrar las películas calificadas en el mismo año de su estreno
same_year_ratings = ratings_summary[ratings_summary['release_year'] == ratings_summary['year']]

# Encontrar la película con la calificación promedio más alta
best_rated_same_year = same_year_ratings.loc[same_year_ratings['mean'].idxmax()]

print(f"La película mejor calificada en su año de estreno es '{best_rated_same_year['name']}' con una calificación promedio de {best_rated_same_year['mean']}")