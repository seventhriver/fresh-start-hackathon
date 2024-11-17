from flask import jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import json
from bson import json_util
import os


def getUserType(body):
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["users"]

    try:
        all_documents = []
        collections = db.list_collection_names()

        if not collections:
            return {}

        for collection_name in collections:
            try:
                collection = db[collection_name]
                documents = list(collection.find({"email": body["email"]}))
                # Convert ObjectId to string for JSON serialization
                documents = json.loads(json_util.dumps(documents))
                all_documents["type"] = collection_name

            except:
                all_documents[collection_name] = {}
                continue

        return jsonify(all_documents), 200

    except:
        return None
    finally:
        if "client" in locals():
            client.close()
