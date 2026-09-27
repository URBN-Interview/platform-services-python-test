from pymongo.database import Database


class RewardsRepository:
    """ Shared repository class for interacting with the rewards collection """
    def __init__(self, db: Database):
        self.collection = db["rewards"]        

