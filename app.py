from flask import Flask, request, render_template, url_for, redirect
from moviwebb_app.data_manager.json_data_manager import JSONdata_manager

app = Flask(__name__)
data_manager = JSONdata_manager('movies.json')

@app.route('/')
def home():
    return "welcome to the moviweb app home page"

@app.route('/users')
def list_users():
    all_users = data_manager.get_all_users()
    return render_template('users.html', all_users=all_users)


@app.route('/user/<int:user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', movies=movies)

@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    if request.method == 'POST':
        new_user_name = request.form['new_user']
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
        return render_template('update_movie.html')
    if request.method == 'POST':
        name = request.form['name']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']
        updated_movie = {'name': name, 'director': director, 'year': year, 'rating': rating}
        data_manager.update_movie(user_id, movie_id, updated_movie)
        return redirect(url_for('user_movies', user_id=user_id))




@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_movie():
    if request.method == 'DELETE':
        pass



if __name__ == "__main__":
    app.run(debug=True)