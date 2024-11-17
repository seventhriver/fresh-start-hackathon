from flask import jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from routes.banks.bank import Bank
import os
import random
import string

def createBank(body):
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["users"]
    collection = db["banks"]

    bank = Bank(
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

    # Generate session token
    token_length = 32
    characters = string.ascii_letters + string.digits
    session_token = ''.join(random.choice(characters) for _ in range(token_length))

    try:
        collection.insert_one({
            "name": bank.name,
            "address": bank.address,
            "city": bank.city,
            "state": bank.state,
            "description": bank.description,
            "email": bank.email,
            "phone": bank.phone,
            "manager": bank.manager,
            "session_token": session_token,
        })

        response = jsonify({
            "status": "success",
            "session_token": session_token
        })
        return response, 200
    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500
