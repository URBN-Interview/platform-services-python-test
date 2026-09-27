from pymongo import ReturnDocument

HIDE_ID = {"_id": 0}

class CustomersRepository:
    """ Shared repository class for interacting with the customers collection """
    def __init__(self, db):
        self.collection = db["customers"]

    async def get_customer(self, email):
        query = {"email_address": email}

        # Return the customer or return none if there's no results, the handler
        # will provide a not-found response
        return await self.collection.find_one(query, HIDE_ID)
    
    async def update_customer(self, email, new_values):
        query = {"email": email},

        return await self.collection.find_one_and_update(
            query,
            {"$set": new_values},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

    async def get_all_customers(self):
        return await self.collection.find({}, HIDE_ID).sort("email_address").to_list(length=None)
