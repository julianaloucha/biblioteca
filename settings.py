import configparser
import os
from api.db import get_db_collections

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

MONGO_URI = config['PROD']['DB_URI']
books_collection, users_collection, adm_collection = get_db_collections(MONGO_URI)