from pymongo.database import Database


class CustomersRepository:
    """ Shared repository class for interacting with the customers collection """
    def __init__(self, db: Database):
        self.collection = db["customers"]
