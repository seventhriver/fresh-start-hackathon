from flask import jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from routes.providers.provider import Provider
import os


def createProvider(body):
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["users"]
    collection = db["providers"]

    provider = Provider(
        body["name"],
        body["address"],
        body["city"],
        body["state"],
        body["description"],
        body["email"],
        body["phone"],
        body["manager"],
       ""
    )
    import random
    import string

    token_length = 32
    characters = string.ascii_letters + string.digits
    provider.session_token = ''.join(random.choice(characters) for _ in range(token_length))


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
                "session_token": provider.session_token
            }
        )

        response = jsonify({"status": "success"})

        return response, 200
    except:
        return jsonify({"status": "failed"}), 200
