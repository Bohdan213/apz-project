from bson.objectid import ObjectId
from global_classes import User
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


MONGO_URI = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.5"
DATABASE_NAME = "test"

try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    events_collection = db["events"]
    users_collection = db["users"]
    print("Connected to MongoDB")
except ConnectionFailure:
    print("Failed to connect to MongoDB")

class communicateWithDB:
    """
    A class that provides methods for communicating with the database.

    Methods:
        create_event(creator_token, group_token, event_description, users_list, group_name, event_time, event_name):
            Creates a new event in the database.
        cancel_event(user_token, event_token):
            Cancels an event in the database.
        view_user_events(user_name):
            Retrieves events associated with a specific user.
        view_events_group(group_token):
            Retrieves events associated with a specific group.
        view_events_creator(user_token):
            Retrieves events created by a specific user.
        get_event_info(event_token):
            Retrieves detailed information about a specific event.
    """
    @staticmethod
    def create_event(creator_token, group_token, event_description, users_list, group_name, event_time, event_name):
        event_data = {
            "creator_token": creator_token,
            "group_token": group_token,
            "description": event_description,
            "users_list": [{"user_name": user[0], "user_email": user[1]} for user in users_list],
            "group_name": group_name,
            "event_time": event_time,
            "event_name": event_name
        }
        inserted_event = events_collection.insert_one(event_data)
        return str(inserted_event.inserted_id)

    @staticmethod
    def cancel_event(user_token, event_token):
        event = events_collection.find_one({"_id": ObjectId(event_token)})
        if event and event["creator_token"] == user_token:
            events_collection.delete_one({"_id": ObjectId(event_token)})
            return True
        return False

    @staticmethod
    def view_user_events(user_name):
        events = events_collection.find({"users_list.user_name": user_name})
        event_tuples = [(str(event["_id"]), event["description"]) for event in events]
        return event_tuples

    @staticmethod
    def view_events_group(group_token):
        events = events_collection.find({"group_token": group_token})
        event_tuples = [(str(event["_id"]), event["description"]) for event in events]
        return event_tuples

    @staticmethod
    def view_events_creator(user_token):
        events = events_collection.find({"creator_token": user_token})
        event_tuples = [(str(event["_id"]), event["description"]) for event in events]
        return event_tuples

    @staticmethod
    def get_event_info(event_token):
        event = events_collection.find_one({"_id": ObjectId(event_token)})
        event["event_id"] = str(event["_id"])
        del event["_id"]
        del event["creator_token"]
        event["users_list"] = [User(user["user_name"], user["user_email"]) for user in event["users_list"]]
        return event
