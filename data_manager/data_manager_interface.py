from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self):
        pass

    @abstractmethod
    def add_user(self):
        pass


    @abstractmethod
    def add_movie(self):
        pass


    @abstractmethod
    def update_movie(self):
        pass

    @abstractmethod
    def delete_movie(self):
        pass