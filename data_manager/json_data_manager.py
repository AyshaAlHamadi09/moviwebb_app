import json
import requests
from moviwebb_app.data_manager.data_manager_interface import DataManagerInterface

class JSONdata_manager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        with open(self.filename, 'r') as fileobject:
            data = fileobject.read()
            json_data = json.loads(data)
            user_list = []
            for item in json_data:
                user = {}
                user['id'] = item['id']
                user['name'] = item['name']
                user_list.append(user)
            return user_list



    def get_user_movies(self, user_id):
        with open(self.filename, 'r') as fileobject:
            data = fileobject.read()
            json_data = json.loads(data)
            for item in json_data:
                if item['id'] == user_id:
                    return item['movies']
            return f"no user with {user_id} id"


    def add_user(self, user_name):
        with open(self.filename, 'r') as fileobject:
            data = fileobject.read()
            json_data = json.loads(data)
        for item in json_data:
            if item['name'] == user_name:
                return f"{user_name} already exists"
        new_user_id = max(item['id'] for item in json_data) + 1
        new_user_name = user_name
        new_user_movies = []
        new_profile = {'id': new_user_id, 'name': new_user_name, 'movies': new_user_movies}
        json_data.append(new_profile)
        with open(self.filename, 'w') as fileobject:
            json.dump(json_data, fileobject)
        return f"user {user_name} was added successfully "


    def add_movie(self, user_id, title):
        self.API_key = "c7645d92"
        URL = f'http://www.omdbapi.com/?apikey={self.API_key}&t={title}'
        response = requests.get(URL)
        movie_info = response.json()
        name = movie_info["Title"]
        director = movie_info["Director"]
        year = movie_info["Year"]
        rating = movie_info["imdbRating"]

        with open(self.filename, 'r') as fileobject:
            data = fileobject.read()
            json_data = json.loads(data)
        new_movie_id = max((movie['id'] for item in json_data for movie in item['movies']), default=0) + 1
        new_movie = {"id": new_movie_id, "name": name, "director": director, "year": year, "rating": rating}
        for item in json_data:
            if item['id'] == user_id:
                item['movies'].append(new_movie)
        updated_data = json.dumps(json_data)
        with open(self.filename, 'w') as fileobject:
            fileobject.write(updated_data)
        return f"movie {name} was added successfully "


    def update_movie(self, user_id, movie_id, updated_movie):
        with open(self.filename, 'r') as fileobject:
            data = fileobject.read()
            json_data = json.loads(data)
        for item in json_data:
            if item['id'] == user_id:
                for movie in item['movies']:
                    if movie['id'] == movie_id:
                        movie.update(updated_movie)
        with open(self.filename, 'w') as fileobject:
            json.dump(json_data, fileobject)
        return f"movie was updated"




    def delete_movie(self):
        pass



