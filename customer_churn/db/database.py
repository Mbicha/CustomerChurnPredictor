import os
from dotenv import load_dotenv

from .config import client
from pymongo.errors import PyMongoError

load_dotenv()

db = client[os.getenv("MONGO_DB_NAME")]
db_collection = db[os.getenv("MONGO_COLLECTION_NAME")]


def insert_document(document, collection=db_collection):
    try:
        collection.insert_one(document)
        return {
            "status": "success",
            "message": "Document inserted successfully"
        }
    except PyMongoError as e:
        return {
            "status": "failure",
            "message": f"An error occurred: {e}"
        }
