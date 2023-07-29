from flask import Flask, request, render_template
from moviwebb_app.data_manager.json_data_manager import JSONdata_manager

app = Flask(__name__)
data_manager = JSONdata_manager('movies.json')

@app.route('/')
def home():
    return "welcome to the moviweb app home page"

@app.route('/users')
def list_users():
    all_users = data_manager.get_all_users()
    return str(all_users)


@app.route('/user/<int:user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return str(movies)

@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    if request.method == 'POST':
        pass

@app.route('/users/<int:user_id>/add_movie',methods=['GET','POST'])
def add_movie():
    if request.method == 'GET':
        return render_template('add_movie.html')
    if request.method == 'POST':
        pass


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET','PUT'])
def update_movie():
    if request.method == 'GET':
        return render_template('update_movie.html')
    if request.method == 'PUT':
        pass


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_movie():
    if request.method == 'DELETE':
        pass



if __name__ == "__main__":
    app.run(debug=True)