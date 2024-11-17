from flask import jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import json_util
import json

def verify_bank_session(session_token):
    """Helper function to verify bank's session token"""
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["users"]
    banks_collection = db["banks"]

    bank = banks_collection.find_one({"session_token": session_token})
    client.close()
    return bank is not None

def get_all_drivers(body):
    """Route to get all drivers"""
    if not body or "session_token" not in body:
        return jsonify({"error": "No session token provided"}), 401

    if not verify_bank_session(body["session_token"]):
        return jsonify({"error": "Unauthorized"}), 401

    client = None
    try:
        client = MongoClient(os.getenv("MONGO_URL"))
        db = client["users"]
        drivers_collection = db["drivers"]

        drivers = list(drivers_collection.find({}, {"_id": 0}))
        return jsonify({"drivers": drivers}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if client:
            client.close()

def get_all_orders(body):
    """Route to get all orders"""
    if not body or "session_token" not in body:
        return jsonify({"error": "No session token provided"}), 401

    if not verify_bank_session(body["session_token"]):
        return jsonify({"error": "Unauthorized"}), 401

    client = None
    try:
        client = MongoClient(os.getenv("MONGO_URL"))
        db = client["orders"]

        all_orders = {}
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            orders = list(collection.find({}, {"_id": 0}))
            all_orders[collection_name] = orders

        return jsonify({"orders": all_orders}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if client:
            client.close()

def assign_order_to_driver(body):
    """Route to assign an order to a driver"""
    if not body or "session_token" not in body:
        return jsonify({"error": "No session token provided"}), 401

    if not verify_bank_session(body["session_token"]):
        return jsonify({"error": "Unauthorized"}), 401

    required_fields = ["driver_email", "order_details", "collection_name"]
    if not all(field in body for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    client = None
    try:
        client = MongoClient(os.getenv("MONGO_URL"))
        db = client["users"]
        drivers_collection = db["drivers"]

        # Update driver's assigned orders
        result = drivers_collection.update_one(
            {"email": body["driver_email"]},
            {"$push": {"assigned_orders": {
                "order_details": body["order_details"],
                "collection_name": body["collection_name"]
            }}}
        )

        if result.modified_count == 0:
            return jsonify({"error": "Driver not found"}), 404

        return jsonify({"message": "Order assigned successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if client:
            client.close()

def create_bank_order(body):
    """Route to create a new order"""
    if not body or "session_token" not in body:
        return jsonify({"error": "No session token provided"}), 401

    if not verify_bank_session(body["session_token"]):
        return jsonify({"error": "Unauthorized"}), 401

    required_fields = ["food_info", "date", "business_name"]
    if not all(field in body for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    client = None
    try:
        client = MongoClient(os.getenv("MONGO_URL"))
        db = client["orders"]

        # Get bank details for the collection name
        banks_db = client["users"]
        bank = banks_db["banks"].find_one({"session_token": body["session_token"]})

        if bank is None:
            return jsonify({"error": "Bank not found"}), 404

        collection_name = f"bank_{bank['name'].lower().replace(' ', '_')}"
        collection = db[collection_name]

        order_data = {
            "food_info": body["food_info"],
            "date": body["date"],
            "business_name": body["business_name"],
            "status": "pending"
        }

        collection.insert_one(order_data)

        return jsonify({
            "message": "Order created successfully",
            "order": order_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if client is not None:
            client.close()
