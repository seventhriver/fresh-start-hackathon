from flask import jsonify from pymongo import MongoClient 
from dotenv import load_dotenv 
from routes.providers.provider import Provider import os


def getProvider(body):
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["users"]
    collection = db["providers"]

    try:
        collection.insert_one(
            {
                "name": provider.name,
                "address": provider.address,
                "city": provider.city,
                "state": provider.description,
                "email": provider.email,
                "phone": provider.phone,
                "manager": provider.manager,
            }
        )

        response = jsonify({"status": "success"})

        return response, 200
    except:
        return jsonify({"status": "failed"}), 200
