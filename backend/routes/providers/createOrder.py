from flask import jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from routes.providers.order import Order
import os


def createOrder(body):
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["orders"]
    collection = db["test_provider"]

    order = Order(body["food_info"], body["date"], body["business_name"])

    try:
        collection.insert_one(
            {
                "food_info": order.food_info,
                "date": order.date,
                "business_name": order.business_name,
            }
        )
        response = jsonify({"status": "success"})
        return response, 200
    except:
        return jsonify({"status": "failed"}), 200
