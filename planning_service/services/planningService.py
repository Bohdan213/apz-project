from planning_service import messages_queue
from planning_service.repository.dbManipulation import communicateWithDB


class PostService:

    @staticmethod
    def create_event(event_description, user_list, group_token):
        communicateWithDB.create_event(event_description, user_list, group_token)
        messages_queue.put(("send_email", user_list, "Event created"))
        return f"Event with description: {event_description} created and users: {user_list} added"

    @staticmethod
    def cancel_event(event_id):
        user_list = communicateWithDB.get_user_list(event_id)
        communicateWithDB.cancel_event(event_id)
        messages_queue.put(("send_email", user_list, "Event cancelled"))
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
