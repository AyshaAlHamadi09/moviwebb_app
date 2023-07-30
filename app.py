from flask import Flask, request, render_template, url_for, redirect
from moviwebb_app.data_manager.json_data_manager import JSONdata_manager


app = Flask(__name__)
data_manager = JSONdata_manager('movies.json')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def home():
    return render_template("homepage.html")

@app.route('/users')
def list_users():
    all_users = data_manager.get_all_users()
    return render_template('users.html', all_users=all_users)


@app.route('/user/<int:user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    if movies != []:
        return render_template('user_movies.html', user_id=user_id, movies=movies)
    return render_template('user_has_no_movies.html', user_id=user_id)

@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    if request.method == 'POST':
        new_user_name = request.form['new_user']
        all_users = data_manager.get_all_users()
        for user in all_users:
            if user['name'] == new_user_name:
                return f"Error: User '{new_user_name}' already exists."
        data_manager.add_user(new_user_name)
        return redirect(url_for('list_users'))

@app.route('/users/<int:user_id>/add_movie',methods=['GET','POST'])
def add_movie(user_id):
    if request.method == 'GET':
        return render_template('add_movie.html')
    if request.method == 'POST':
        title = request.form['new_movie']
        data_manager.add_movie(user_id, title)
        return redirect(url_for('user_movies', user_id=user_id))

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET','POST'])
def update_movie(user_id, movie_id):
    if request.method == 'GET':
        movies = data_manager.get_user_movies(user_id) #list of dicts
        movie_to_update = {}
        for movie in movies:
            if movie['id'] == movie_id:
                movie_to_update = movie
        return render_template('update_movie.html', movie=movie_to_update)
    if request.method == 'POST':
        name = request.form['name']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']
        updated_movie = {}
        if name:
            updated_movie['name'] = name
        if director:
            updated_movie['director'] = director
        if year:
            updated_movie['year'] = year
        if rating:
            updated_movie['rating'] = rating
        data_manager.update_movie(user_id, movie_id, updated_movie)
        return redirect(url_for('user_movies', user_id=user_id))



@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('user_movies', user_id=user_id))



if __name__ == "__main__":
    app.run(debug=True)