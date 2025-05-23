from dotenv import load_dotenv
import os
import pymongo
load_dotenv()  # This line brings all environment variables from .env into os.environ

#Takes in the name of desired database and collection as string, then returns database.
#Simplifies process of connecting to databases and removes code redundancy.
def mongoConnect(database,collection,OP=None):
    operator=True if OP else False
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi
    # Create a new client and connect to the server
    client = MongoClient(os.getenv("CONNECTION_STRING"), server_api=ServerApi('1'),uuidRepresentation='standard')
    database= client[database]
    collection= database[collection]
    if operator:
        return database,collection
    else:
        return collection
