from planning_service import messages_queue
from planning_service.repository.dbManipulation import communicateWithDB
from global_classes import Request


class PostService:

    @staticmethod
    def create_event(event_description, user_list, group_token):
        communicateWithDB.create_event(event_description, user_list, group_token)
        queue_request = Request("planning", "event_invitation", user_list)
        messages_queue.put(queue_request)
        return f"Event with description: {event_description} created and users: {user_list} added"

    @staticmethod
    def cancel_event(event_id):
        user_list = communicateWithDB.get_user_list(event_id)
        communicateWithDB.cancel_event(event_id)
        queue_request = Request("planning", "event_cancellation", user_list)
        messages_queue.put(queue_request)
        return f"Event with id: {event_id} cancelled"


class GetService:

    @staticmethod
    def view_user_events(user_token):
        user_events = communicateWithDB.view_user_events(user_token)
        return user_events

    @staticmethod
    def view_event_info(event_id):
        event_info = communicateWithDB.view_event_info(event_id)
        return event_info
