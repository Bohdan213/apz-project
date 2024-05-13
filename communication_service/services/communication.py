class CommunicationService:

    def __init__(self, reader):
        self.reader = reader

    def start(self):
        print("Starting communication service")
        self.reader.read_queue()
    
    def send_group_addition_email(self, users, group_name):
        for user in users:
            print(f"Sending group {group_name} addition email to {user.user_name} on {user.user_email}")
    
    def send_group_removal_email(self, users, group_name):
        for user in users:
            print(f"Sending group {group_name} removal email to {user.user_name} on {user.user_email}")
    
    def send_event_invitation_email(self, users, event_name, event_time):
        for user in users:
            print(f"Sending event {event_name} at {event_time} invitation email to {user.user_name} on {user.user_email}")
    
    def send_event_cancellation_email(self, users, event_name, event_time):
        for user in users:
            print(f"Sending event {event_name} at {event_time} cancellation email to {user.user_name} on {user.user_email}")

    def parse_memory(self):
        for request in self.reader.memory:
            print(f"Request: {request}")
            if request.source_service == "user_management":
                if request.request_type == "group_addition":
                    self.send_group_addition_email(request.users_list, request.group_name)
                elif request.request_type == "group_removal":
                    self.send_group_removal_email(request.users_list, request.group_name)
            elif request.source_service == "planning":
                if request.request_type == "event_invitation":
                    self.send_event_invitation_email(request.users_list, request.event_name, request.event_time)
                elif request.request_type == "event_cancellation":
                    self.send_event_cancellation_email(request.users_list, request.event_name, request.event_time)

            self.reader.memory.remove(request)
