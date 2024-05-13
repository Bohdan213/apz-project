# simple CLI interface for this RESTful API

import requests

class Client:
    def __init__(self):
        self.commands = {
            "authenticate": {"method": "GET", "args": ["user_name", "password"]},
            "get_group_users": {"method": "GET", "args": ["group_token"]},
            "user_existance": {"method": "GET", "args": ["user_name"]},
            "view_events_user_name": {"method": "GET", "args": ["user_name"]},
            "view_events_group": {"method": "GET", "args": ["group_token"]},
            "view_events_creator": {"method": "GET", "args": ["user_token"]},
            "add_user": {"method": "POST", "args": ["user_name", "password", "email"]},
            "create_group": {"method": "POST", "args": ["user_token", "group_name", "users_list"]},
            "add_user_to_group": {"method": "POST", "args": ["group_token", "user_name", "user_token"]},
            "delete_user_from_group": {"method": "POST", "args": ["group_token", "user_name", "user_token"]},
            "create_event": {"method": "POST", "args": ["user_token", "group_token", "description", "users_list", "group_name", "event_time", "event_name"]},
            "cancel_event": {"method": "DELETE", "args": ["user_token", "event_token"]},
            "delete_group": {"method": "DELETE", "args": ["group_token", "user_token"]},
            "delete_user": {"method": "DELETE", "args": ["user_token"]}
        }
        self.user_token = None
        self.group_token = None

    def run(self):
        while True:
            command = input("Enter command: ")
            if command == "exit":
                break
            if command not in self.commands:
                print("Invalid command")
                continue
            method = self.commands[command]["method"]
            args = self.commands[command]["args"]
            data = {}
            for arg in args:
                if arg == "user_token":
                    data[arg] = self.user_token
                elif arg == "group_token":
                    data[arg] = self.group_token
                else:
                    data[arg] = input(f"Enter {arg}: ")
            response = self.request(method, command, data)
            if response.status_code == 500:
                print("Internal server error")
                continue
            if (command == "add_user"):
                self.user_token = response.json().get("user_token").get("user_token")
            if (command == "create_group"):
                self.group_token = response.json().get("group_token").get("group_token")
            print(response.json())

    def request(self, method, operation, data):
        if method == "GET":
            return requests.get(f"http://localhost:8080/api/v1/facade_service/{operation}", json=data)
        elif method == "POST":
            return requests.post(f"http://localhost:8080/api/v1/facade_service/{operation}", json=data)
        elif method == "DELETE":
            return requests.delete(f"http://localhost:8080/api/v1/facade_service/{operation}", json=data)
        else:
            return "Invalid method"
        
client = Client()
client.run()