from flask import Flask, render_template, request, jsonify
import pickle
import requests

app = Flask(__name__)

def fetch_poster_and_overview(movie_id):
    api_key = "c2cfb543a34719673b39337b90d98c9b" 
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=es-MX"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    movie_overview = data.get('overview')
    if poster_path and movie_overview:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path, movie_overview
    return None, None


movies = pickle.load(open("ListaDePelis.pkl", 'rb'))
similarity = pickle.load(open("similitudes.pkl", 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    titles = movies['title'].tolist()
    suggestions = [title for title in titles if search.lower() in title.lower()][:5]
    return jsonify(suggestions)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form['movie']
    if movie not in movies['title'].values:
        return jsonify({'error': 'No se encontró ninguna película'})
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommend_movies = []
    recommend_posters = []
    movie_overview = []

    for i in distances[1:7]:
        movie_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        poster, overview = fetch_poster_and_overview(movie_id)

        if poster and overview:
            recommend_posters.append(poster)
            movie_overview.append(overview)
        else:
            if not poster:
                recommend_posters.append('/static/img/noencontro.png')
            else:
                recommend_posters.append(poster)
            
            if not overview:
                movie_overview.append('No se encontro descripción')
            else:
                movie_overview.append(overview)

            # Manejar el caso en el que no se encuentra un póster
            


        #recommend_posters.append(poster if poster else 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pngegg.com%2Fen%2Fsearch%3Fq%3Dnot%2BFound&psig=AOvVaw255_y-_Tw8lK8EBpaJDAW2&ust=1718491279459000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMixk4mV3IYDFQAAAAAdAAAAABAK')
    return jsonify({'movies': recommend_movies, 'overview' : movie_overview,'posters': recommend_posters})

if __name__ == '__main__':
    app.run(debug=True)