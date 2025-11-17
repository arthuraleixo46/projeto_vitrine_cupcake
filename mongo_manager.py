from pymongo import MongoClient
from bson import ObjectId
import os

DB_URI = os.getenv('MONGO_URI', 'mongodb://mongo:mongoadmin@localhost:27017/')

class MongoManager:
    def __init__(self, uri=DB_URI, db_name='cupcake_store'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_cupcakes(self):
        docs = list(self.db.cupcakes.find().sort('_id', -1))
        for d in docs:
            d['_id'] = str(d['_id'])
        return docs

    def get_cupcake(self, cupcake_id):
        try:
            doc = self.db.cupcakes.find_one({'_id': ObjectId(cupcake_id)})
        except Exception:
            return None
        if not doc:
            return None
        doc['_id'] = str(doc['_id'])
        return doc

    def add_cupcake(self, data):
        return self.db.cupcakes.insert_one(data)

    def delete_cupcake(self, cupcake_id):
        return self.db.cupcakes.delete_one({'_id': ObjectId(cupcake_id)})

    def update_cupcake(self, cupcake_id, data):
        return self.db.cupcakes.update_one({'_id': ObjectId(cupcake_id)}, {'$set': data})

    # Métodos USERs
    def find_user_by_email(self, email):
        return self.db.users.find_one({'email': email})

    def create_user(self, email, password_hash):
        return self.db.users.insert_one({'email': email, 'password_hash': password_hash})
