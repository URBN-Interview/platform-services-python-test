from pymongo import MongoClient

class DBConnection:
    """
    Singleton class for managing MongoDB connections.
    """

    __client = None

    @classmethod
    def get_client(cls):
        """
        Returns a MongoClient instance. If an instance already exists, it returns the existing one.

        Returns:
            MongoClient: A MongoClient instance.
        """
        if not cls.__client:
            # If no client instance exists, create a new one
            cls.__client = MongoClient("mongodb://mongodb:27017")
        return cls.__client
