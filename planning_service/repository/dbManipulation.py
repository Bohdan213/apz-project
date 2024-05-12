import pymongo
from bson.objectid import ObjectId
from global_classes import User

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "test"

client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

events_collection = db["events"]
users_collection = db["users"]


class communicateWithDB:
    @staticmethod
    def create_event(creator_token, group_token, event_description, users_list, group_name, event_time, event_name):
        event_data = {
            "creator_token": creator_token,
            "group_token": group_token,
            "description": event_description,
            "users_list": [{"user_name": user.user_name, "user_email": user.user_email} for user in users_list],
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
