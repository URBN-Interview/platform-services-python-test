from pymongo import MongoClient


# Singleton design pattern for database connection
class DBConnection:
    __client = None

    @classmethod
    def get_client(cls):
        if not cls.__client:
            cls.__client = MongoClient("mongodb", 27017)
        return cls.__client
