import requests
from facade_service import get_random_url
import logging

class PostService:

# user_management_service

    @staticmethod
    def add_user(user_name, password, email):
        print("add_user")
        user_management_service = get_random_url("user_management_service")
        if user_management_service is None:
            return 500
        print(user_management_service)
        response = requests.post(f"{user_management_service}/add_user", json={"user_name": user_name, "password": password, "email": email})
        logging.info(response.json())
        return response.json()


    @staticmethod
    def create_group(user_token, group_name, users_list):
        user_management_service = get_random_url("user_management_service")
        if user_management_service is None:
            return 500
        response = requests.post(f"{user_management_service}/create_group", json={"user_token": user_token, "group_name": group_name, "users_list": users_list})
        logging.info(response.json())
        return response.json()
        

    @staticmethod
    def add_user_to_group(group_token, user_name, creator_token):
        user_management_service = get_random_url("user_management_service")
        if user_management_service is None:
            return 500
        response = requests.post(f"{user_management_service}/add_user_to_group", json={"group_token": group_token, "user_name": user_name, "user_token": creator_token})
        logging.info(response.json())
        return response.json()

    @staticmethod
    def delete_user_from_group(group_token, user_name, creator_token):
        user_management_service = get_random_url("user_management_service")
        if user_management_service is None:
            return 500
        response = requests.post(f"{user_management_service}/delete_user_from_group", json={"group_token": group_token, "user_name": user_name, "user_token": creator_token})
        logging.info(response.json())
        return response.json()

# planning_service

    @staticmethod
    def create_event(creator_token, group_token, event_description, users_list, group_name, event_time, event_name):
        planning_service = get_random_url("planning_service")
        if planning_service is None:
            return 500
        response = requests.post(f"{planning_service}/create_event", json={"creator_token": creator_token, "group_token": group_token, "description": event_description, "users_list": users_list, "group_name": group_name, "event_time": event_time, "event_name": event_name})
        logging.info(response.json())
        return response.json()

    @staticmethod
    def cancel_event(user_token, event_token):
        planning_service = get_random_url("planning_service")
        if planning_service is None:
            return 500
        response = requests.delete(f"{planning_service}/cancel_event", json={"user_token": user_token, "event_token": event_token})
        logging.info(response.json())
        return response.json()

class GetService:

# user_management_service
    @staticmethod
    def user_authentication(user_name, password):
        user_management_service = get_random_url("user_management_service")
        if user_management_service is None:
            return 500
        response = requests.get(f"{user_management_service}/user_authentication", json={"user_name": user_name, "password": password})
        logging.info(response.json())
        return response.json()

    @staticmethod
    def get_group_users(group_token):
        user_management_service = get_random_url("user_management_service")
        if user_management_service is None:
            return 500
        response = requests.get(f"{user_management_service}/get_group_users", json={"group_token": group_token})
        logging.info(response.json())
        return response.json()

    @staticmethod
    def get_user_groups(user_token):
        user_management_service = get_random_url("user_management_service")
        if user_management_service is None:
            return 500
        response = requests.get(f"{user_management_service}/get_user_groups", json={"user_token": user_token})
        logging.info(response.json())
        return response.json()

    @staticmethod
    def check_user_existence(user_name):
        user_management_service = get_random_url("user_management_service")
        if user_management_service is None:
            return 500
        response = requests.get(f"{user_management_service}/check_user_existence", json={"user_name": user_name})
        logging.info(response.json())
        return response.json()
    
# planning_service
    
    @staticmethod
    def view_events_user_name(user_name):
        planning_service = get_random_url("planning_service")
        if planning_service is None:
            return 500
        response = requests.get(f"{planning_service}/view_events_user_name", json={"user_name": user_name})
        logging.info(response.json())
        return response.json()

    @staticmethod
    def view_events_group(group_token):
        planning_service = get_random_url("planning_service")
        if planning_service is None:
            return 500
        response = requests.get(f"{planning_service}/view_events_group", json={"group_token": group_token})
        logging.info(response.json())
        return response.json()

    @staticmethod
    def view_events_creator(user_token):
        planning_service = get_random_url("planning_service")
        if planning_service is None:
            return 500
        response = requests.get(f"{planning_service}/view_events_creator", json={"user_token": user_token})
        logging.info(response.json())
        return response.json()



class DeleteService:
# user_management_service
    @staticmethod
    def delete_user(user_token):
        user_management_service = get_random_url("user_management_service")
        if user_management_service is None:
            return 500
        response = requests.delete(f"{user_management_service}/delete_user", json={"user_token": user_token})
        logging.info(response.json())
        return response.json()

    @staticmethod
    def delete_group(group_token, creator_token):
        user_management_service = get_random_url("user_management_service")
        if user_management_service is None:
            return 500
        response = requests.delete(f"{user_management_service}/delete_group", json={"group_token": group_token, "user_token": creator_token})
        logging.info(response.json())
        return response.json()