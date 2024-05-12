class CommunicationService:

    def __init__(self, reader):
        self.reader = reader

    def start(self):
        self.reader.read_queue()
    
    def send_group_addition_email(self, users, group_id):
        for user in users:
            print(f"Sending group {group_id} addition email to {user.user_name} on {user.user_email}")
    
    def send_group_removal_email(self, users, group_id):
        for user in users:
            print(f"Sending group {group_id} removal email to {user.user_name} on {user.user_email}")
    
    def send_event_invitation_email(self, users, event_id):
        for user in users:
            print(f"Sending event {event_id} invitation email to {user.user_name} on {user.user_email}")
    
    def send_event_cancellation_email(self, users, event_id):
        for user in users:
            print(f"Sending event {event_id} cancellation email to {user.user_name} on {user.user_email}")

    def parse_memory(self):
        for request in self.reader.memory:
            print(f"Request: {request}")
            if request.source_type == "user_management":
                if request.request_type == "group_addition":
                    self.send_group_addition_email(request.request_data, request.group_id)
                elif request.request_type == "group_removal":
                    self.send_group_removal_email(request.request_data, request.group_id)
            elif request.source_type == "planning":
                if request.request_type == "event_invitation":
                    self.send_event_invitation_email(request.request_data, request.event_id)
                elif request.request_type == "event_cancellation":
                    self.send_event_cancellation_email(request.request_data, request.event_id)
