import pandas as pd

# Cargar los datos de los archivos CSV
user_ratings = pd.read_csv('UserRatings.csv')
movies = pd.read_csv('Movies.csv')

# Mostrar las columnas para verificar
print('UserRatings:',user_ratings.columns)
print('Movies: ',movies.columns)