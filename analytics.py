import pandas as pd

# Cargar los datos de los archivos CSV
movies = pd.read_csv('Movies.csv')
user_ratings = pd.read_csv('UserRatings.csv')

# Renombrar las columnas para que coincidan con los nombres proporcionados
movies.columns = ['movie_id', 'user_id', 'rating', 'date']
user_ratings.columns = ['movie_id', 'release_year', 'name', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5']

# Eliminar las columnas innecesarias en el archivo de películas
user_ratings = user_ratings[['movie_id', 'release_year', 'name']]

# Asegurarse de que las columnas 'movie_id' tengan el mismo tipo de datos
movies['movie_id'] = movies['movie_id'].astype(str)
user_ratings['movie_id'] = user_ratings['movie_id'].astype(str)

# 1. Especificar la cantidad de calificaciones que tiene cada película, las calificaciones promedio, máximas, mínimas y su desviación.
ratings_summary = movies.groupby('movie_id')['rating'].agg(['count', 'mean', 'max', 'min', 'std']).reset_index()
ratings_summary = ratings_summary.merge(user_ratings, left_on='movie_id', right_on='movie_id')

# 2. Según la calificación promedio de las películas, listar las 3 mejores y peores.
top_3_movies = ratings_summary.nlargest(3, 'mean')[['name', 'mean']]
peores_3_movies = ratings_summary.nsmallest(3, 'mean')[['name', 'mean']]

# 3. Contar cuántas películas tienen calificaciones en el mismo año de su estreno.
movies['year'] = pd.to_datetime(movies['date']).dt.year
merged_data = movies.merge(user_ratings, left_on='movie_id', right_on='movie_id')
same_year_ratings = merged_data[merged_data['year'] == merged_data['release_year']]
same_year_count = same_year_ratings['movie_id'].nunique()

# 4. Calcular la calificación promedio en el año de estreno y comparar con años posteriores.
same_year_avg_rating = same_year_ratings.groupby('movie_id')['rating'].mean().reset_index()
same_year_avg_rating = same_year_avg_rating.merge(user_ratings, left_on='movie_id', right_on='movie_id')

subsequent_years_avg_rating = merged_data[merged_data['year'] > merged_data['release_year']].groupby(['movie_id', 'year'])['rating'].mean().reset_index()
subsequent_years_avg_rating = subsequent_years_avg_rating.merge(user_ratings, left_on='movie_id', right_on='movie_id')

# Comparar calificaciones
comparison = same_year_avg_rating[['movie_id', 'rating']].merge(subsequent_years_avg_rating[['movie_id', 'rating']], on='movie_id', suffixes=('_release_year', '_subsequent_years'))
avg_rating_release_year = same_year_avg_rating['rating'].mean()

i_spy_ratings_count = ratings_summary[ratings_summary['name'] == 'I Spy']['count'].values[0]
innocents_avg_rating = ratings_summary[ratings_summary['name'] == 'Innocents']['mean'].values[0]
death_of_a_salesman_std = ratings_summary[ratings_summary['name'] == 'Death of a Salesman']['std'].values[0]
# Calcular la calificación promedio en el año de estreno para "Breakin' All The Rules" y "Bulletproof Monk"
breakin_all_the_rules_avg_release_year = same_year_avg_rating[same_year_avg_rating['name'] == "Breakin' All The Rules"]['rating'].mean()
bulletproof_monk_avg_release_year = same_year_avg_rating[same_year_avg_rating['name'] == "Bulletproof Monk"]['rating'].mean()

# Calcular la calificación promedio en los años posteriores para "Breakin' All The Rules" y "Bulletproof Monk"
breakin_all_the_rules_avg_subsequent_years = subsequent_years_avg_rating[subsequent_years_avg_rating['name'] == "Breakin' All The Rules"]['rating'].mean()
bulletproof_monk_avg_subsequent_years = subsequent_years_avg_rating[subsequent_years_avg_rating['name'] == "Bulletproof Monk"]['rating'].mean()

# Determinar si las calificaciones aumentan o disminuyen
breakin_all_the_rules_trend = "aumenta" if breakin_all_the_rules_avg_subsequent_years > breakin_all_the_rules_avg_release_year else "disminuye"
bulletproof_monk_trend = "aumenta" if bulletproof_monk_avg_subsequent_years > bulletproof_monk_avg_release_year else "disminuye"



# Mostrar resultados
print("\nTop 3 películas:")
print(top_3_movies)

print("\peores 3 películas:")
print(peores_3_movies)

print("\nCantidad de películas con calificaciones en el mismo año de su estreno:")
print(same_year_count)

print("\nComparación de calificaciones promedio en el año de estreno y años posteriores:")
print(comparison)

print(f"\nCantidad de calificaciones de 'I Spy': {i_spy_ratings_count}")
print(f"Calificación promedio de 'Innocents': {innocents_avg_rating}")
print(f"Desviación estándar de 'Death of a Salesman': {death_of_a_salesman_std}")

print("\nCalificación promedio de las películas en su año de estreno:")
print(avg_rating_release_year)

print(f"\n'Breakin' All The Rules' - Promedio año de estreno: {breakin_all_the_rules_avg_release_year}, Promedio años posteriores: {breakin_all_the_rules_avg_subsequent_years}, Tendencia: {breakin_all_the_rules_trend}")