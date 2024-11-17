from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
from google.auth.transport import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get environment variables
MONGODB_URL = os.getenv("MONGO_URL")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Connect to MongoDB
client = MongoClient(MONGODB_URL)
db = client["users"]


class MultiCollection:
    def __init__(self, db, collection_names):
        self.db = db
        self.collection_names = collection_names

    def find_one(self, query):
        for collection_name in self.collection_names:
            collection = self.db[collection_name]
            result = collection.find_one(query)
            if result:
                return result
        return None


# Assign users_collection to an instance of MultiCollection
users_collection = MultiCollection(
    db, ["providers", "banks", "drivers"]
)  # Adjust collection name as needed


def handle_google_auth(request_data):
    try:
        # Get access token from request body
        if not request_data or "access_token" not in request_data:
            return (
                jsonify(
                    {
                        "user": None,
                        "exists": False,
                        "error": "Access token not provided",
                    }
                ),
                400,
            )

        access_token = request_data["access_token"]

        # Create credentials object
        credentials = Credentials(
            token=access_token,
            refresh_token=None,
            token_uri=None,
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            scopes=[
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
        )

        # Verify the token and get user info
        try:
            id_info = id_token.verify_oauth2_token(
                access_token, requests.Request(), GOOGLE_CLIENT_ID
            )

            email = id_info["email"]
        except Exception as e:
            return (
                jsonify(
                    {"user": None, "exists": False, "error": "Invalid access token"}
                ),
                400,
            )

        # Search for user in MongoDB
        user = users_collection.find_one({"email": email})
        # Convert MongoDB document to JSON serializable format
        if user:
            user_dict = dict(user)
            del user_dict["_id"]  # Remove _id field
            print(user_dict)
            return jsonify({"user": user_dict, "exists": True})
        else:
            return jsonify({"user": {"name": id_info["name"], "email": email}, "exists": False})

    except Exception as e:
        return jsonify({"user": None, "exists": False, "error": str(e)}), 400
