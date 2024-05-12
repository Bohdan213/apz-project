from communication_service import consul_client
from communication_service.controllers.queue import QueueReader
from communication_service.services.utils import get_config, get_client
import sys
import threading
import atexit

class CommunicationService:

    def __init__(self, reader):
        self.reader = reader

    def start(self):
        self.reader.read_queue()
    
    def send_group_addition_email(self, users, group_id):
        for user in users:
            print(f"Sending group {group_id} addition email to {user.user_email}")
    
    def send_group_removal_email(self, users, group_id):
        for user in users:
            print(f"Sending group {group_id} removal email to {user.user_email}")
    
    def send_event_invitation_email(self, users, event_id):
        for user in users:
            print(f"Sending event {event_id} invitation email to {user.user_email}")
    
    def send_event_cancellation_email(self, users, event_id):
        for user in users:
            print(f"Sending event {event_id} cancellation email to {user.user_email}")

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

def exit_handler():
    consul_client.agent.service.deregister(service_id)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        service_num = sys.argv[1]
    else:
        raise ValueError("Please provide a service number.")

    atexit.register(exit_handler)

    service_id = f"communication_service_{service_num}"
    consul_client.agent.service.register(f"communication_service", port=6100+int(service_num), service_id=service_id)
    
    hz_config = get_config(consul_client, "hazelcast_config")
    hz_client = get_client(hz_config)

    communication = CommunicationService(QueueReader(hz_client.get_queue("communication").blocking()))
    threading.Thread(target=communication.start).start()

    while True:
        communication.parse_memory()
