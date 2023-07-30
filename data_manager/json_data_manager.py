import json
import requests
from moviwebb_app.data_manager.data_manager_interface import DataManagerInterface

class JSONdata_manager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        try:
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
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            return []

        except ValueError as e:
            print(f"Error: JSON parsing failed - {e}")
            return []



    def get_user_movies(self, user_id):
        try:
            with open(self.filename, 'r') as fileobject:
                data = fileobject.read()
                json_data = json.loads(data)
                for item in json_data:
                    if item.get('id') == user_id:
                        return item.get('movies')
                return f"no user with {user_id} id"
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            return []

        except ValueError as e:
            print(f"Error: JSON parsing failed - {e}")
            return []


    def add_user(self, user_name):
        try:
            with open(self.filename, 'r') as fileobject:
                data = fileobject.read()
                json_data = json.loads(data)
            for item in json_data:
                if 'name' in item and item['name'] == user_name:
                    return f"{user_name} already exists"
            new_user_id = max(item['id'] for item in json_data) + 1
            new_user_name = user_name
            new_user_movies = []
            new_profile = {'id': new_user_id, 'name': new_user_name, 'movies': new_user_movies}
            json_data.append(new_profile)
            with open(self.filename, 'w') as fileobject:
                json.dump(json_data, fileobject)
            return f"user {user_name} was added successfully "
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            return "Error: File not found"
        except ValueError as e:
            print(f"Error: JSON parsing failed - {e}")
            return "Error: JSON parsing failed"
        except KeyError as e:
            print(f"Error: Missing key in JSON data - {e}")
            return "Error: Missing key in JSON data"


    def add_movie(self, user_id, title):
        try:
            self.API_key = "c7645d92"
            URL = f'http://www.omdbapi.com/?apikey={self.API_key}&t={title}'
            response = requests.get(URL)
            if response.status_code != 200:
                return f"Error: Unable to fetch movie data. Status code: {response.status_code}"

            movie_info = response.json()
            name = movie_info.get("Title")
            director = movie_info.get("Director")
            year = movie_info.get("Year")
            rating = movie_info.get("imdbRating")
            poster = movie_info.get("Poster")

            if not name or not director or not year or not rating:
                return "Error: Movie data not found in the API response."

            with open(self.filename, 'r') as fileobject:
                data = fileobject.read()
                json_data = json.loads(data)

            new_movie_id = max((movie['id'] for item in json_data for movie in item['movies']), default=0) + 1
            new_movie = {"id": new_movie_id, "name": name, "director": director, "year": year, "rating": rating, "poster": poster}

            for item in json_data:
                if item['id'] == user_id:
                    item['movies'].append(new_movie)

            updated_data = json.dumps(json_data)

            with open(self.filename, 'w') as fileobject:
                fileobject.write(updated_data)
            return f"movie {name} was added successfully "
        except requests.exceptions.RequestException as e:
            return f"Error: Failed to make an API request - {e}"
        except ValueError as e:
            return f"Error: JSON parsing failed - {e}"
        except FileNotFoundError as e:
            return f"Error: File not found - {e}"
        except KeyError as e:
            return f"Error: Missing key in JSON data - {e}"


    def update_movie(self, user_id, movie_id, updated_movie):
        try:
            with open(self.filename, 'r') as fileobject:
                data = fileobject.read()
                json_data = json.loads(data)

            user_exists = False
            movie_exists = False

            for item in json_data:
                if item['id'] == user_id:
                    user_exists = True
                    for movie in item['movies']:
                        if movie['id'] == movie_id:
                            movie_exists = True
                            movie.update(updated_movie)
            if not user_exists:
                return f"Error: User with id {user_id} not found"
            if not movie_exists:
                return f"Error: Movie with id {movie_id} not found for user {user_id}."

            with open(self.filename, 'w') as fileobject:
                json.dump(json_data, fileobject)
            return f"movie was updated"
        except FileNotFoundError as e:
            return f"Error: File not found - {e}"
        except ValueError as e:
            return f"Error: JSON parsing failed - {e}"
        except KeyError as e:
            return f"Error: Missing key in JSON data - {e}"




    def delete_movie(self, user_id, movie_id):
        try:
            with open(self.filename, 'r') as fileobject:
                data = fileobject.read()
                json_data = json.loads(data)

            user_exists = False
            movie_exists = False

            for item in json_data:
                if item['id'] == user_id:
                    user_exists = True
                    for movie in item['movies']:
                        if movie['id'] == movie_id:
                            movie_exists = True
                            item['movies'].remove(movie)

            if not user_exists:
                return f"Error: User with id {user_id} not found"
            if not movie_exists:
                return f"Error: Movie with id {movie_id} not found for user {user_id}."

            with open(self.filename, 'w') as fileobject:
                json.dump(json_data, fileobject)
            return f"movie was deleted"

        except FileNotFoundError as e:
            return f"Error: File not found - {e}"
        except ValueError as e:
            return f"Error: JSON parsing failed - {e}"
        except KeyError as e:
            return f"Error: Missing key in JSON data - {e}"



