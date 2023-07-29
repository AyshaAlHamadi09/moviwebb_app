import json
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


    def add_user(self):
        pass