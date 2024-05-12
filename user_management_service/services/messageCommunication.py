from user_management_service.repository.dbManipulation import communicateWithDB
from global_classes import User, Request
from communication_service.controllers.queue import QueueWriter
from user_management_service import queue_writer

class UserGroupNotifier:
    def __init__(self, user_names: list, group_name: str):
        self.user_names = user_names
        self.group_name = group_name
        self.user_emails = [communicateWithDB.get_user(user_name).email for user_name in user_names]
        self.users_list = [User(user_name, user_email) for user_name, user_email in zip(self.user_names, self.user_emails)]
        self.queue_writer = queue_writer
    
    def notify_addition(self):
        request_data = {'users_list': self.users_list, 'group_name': self.group_name}
        request = Request('user_management', 'group_addition', request_data)
        self.queue_writer.write_queue(request)
    
    def notify_removal(self):
        request_data = {'users_list': self.users_list, 'group_name': self.group_name}
        request = Request('user_management', 'group_removal', request_data)
        self.queue_writer.write_queue(request)
