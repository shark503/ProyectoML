import pandas as pd
import requests
import time

# Carga el conjunto de datos TMDB 10000 Movies Dataset
df = pd.read_csv('data/top_1000_popular_movies_tmdb.csv')

# clave API de TMDB
api_key = ''

# Función para traducir un título al español
def espanol(movie_id, api_key):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=es-MX'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('title', None)
    else:
        return None

# Itera sobre cada fila del DataFrame y traduce el título
total_movies = len(df)
for index, row in df.iterrows():
    movie_id = row['id']
    titulo = espanol(movie_id, api_key)
    if titulo:
        df.at[index, 'title'] = titulo
        print(str(index)+ "  de  " + str(total_movies))

    time.sleep(0.2)  # Para evitar superar el límite de la API

# Guarda el DataFrame actualizado en un nuevo archivo CSV
df.to_csv('data/tmdb_10000_movies.csv', index=False)



