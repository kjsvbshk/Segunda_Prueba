# Cargar las librerías necesarias
library(dplyr)
library(lubridate)

# Leer los archivos CSV
user_ratings <- read.csv("UserRatings.csv")
movies <- read.csv("Movies.csv")

# Asegurarse de que las columnas de ID sean del mismo tipo
user_ratings$MOVIE_ID <- as.character(user_ratings$MOVIE_ID)
movies$ID_MOVIE <- as.character(movies$ID_MOVIE)

# Unir los datos por MOVIE_ID e ID_MOVIE
merged_data <- merge(user_ratings, movies, by.x = "MOVIE_ID", by.y = "ID_MOVIE")

# Calcular estadísticas por película
movie_stats <- merged_data %>%
  group_by(MOVIE_TITLE) %>%
  summarise(
    num_ratings = n(),
    avg_rating = mean(RATING, na.rm = TRUE),
    max_rating = max(RATING, na.rm = TRUE),
    min_rating = min(RATING, na.rm = TRUE),
    std_rating = sd(RATING, na.rm = TRUE)
  )

# Mostrar las estadísticas
print("Estadísticas de las películas:")
print(movie_stats)

# Identificar las 3 mejores y peores películas según la calificación promedio
top_3_movies <- movie_stats %>%
  arrange(desc(avg_rating)) %>%
  slice(1:3) %>%
  select(MOVIE_TITLE, avg_rating)

bottom_3_movies <- movie_stats %>%
  arrange(avg_rating) %>%
  slice(1:3) %>%
  select(MOVIE_TITLE, avg_rating)

print("Top 3 películas:")
print(top_3_movies)

print("Bottom 3 películas:")
print(bottom_3_movies)

# Determinar cuántas películas tienen calificaciones en el mismo año de su lanzamiento
merged_data <- merged_data %>%
  mutate(RATING_YEAR = year(dmy(RATING_DATE)))  # Convertir RATING_DATE a año

same_year_ratings <- merged_data %>%
  filter(MOVIE_YEAR == RATING_YEAR)

num_same_year <- same_year_ratings %>%
  summarise(n_distinct(MOVIE_ID)) %>%
  pull()

avg_rating_same_year <- same_year_ratings %>%
  summarise(mean(RATING, na.rm = TRUE)) %>%
  pull()

print(paste("Número de películas con calificaciones en el mismo año de lanzamiento:", num_same_year))
print(paste("Calificación promedio en el año de lanzamiento:", round(avg_rating_same_year, 2)))

# Analizar la tendencia de las calificaciones promedio en años posteriores
yearly_avg_ratings <- merged_data %>%
  group_by(RATING_YEAR) %>%
  summarise(avg_rating = mean(RATING, na.rm = TRUE)) %>%
  mutate(rating_change = avg_rating - lag(avg_rating))

print("Tendencia de calificaciones promedio por año:")
print(yearly_avg_ratings)