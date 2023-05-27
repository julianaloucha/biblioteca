# api/db.py
from pymongo import MongoClient

def get_db_collections(mongo_uri):
    client = MongoClient(mongo_uri)
    db = client['biblioteca']
    books_collection = db['livros']
    users_collection = db['users']
    adm_collection = db['adms']
    return books_collection, users_collection, adm_collection
