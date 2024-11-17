from flask import jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
from bson import json_util


def getOrders(body):
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["orders"]

    try:
        all_documents = {}
        collections = db.list_collection_names()

        if not collections:
            return {}

        for collection_name in collections:
            try:
                collection = db[collection_name]
                documents = list(collection.find({}))
                # Convert ObjectId to string for JSON serialization
                documents = json.loads(json_util.dumps(documents))
                all_documents[collection_name] = documents

            except:
                all_documents[collection_name] = []
                continue

        return all_documents, 200

    except:
        return None
    finally:
        if "client" in locals():
            client.close()
