from planning_service import messages_queue
from planning_service.repository.dbManipulation import communicateWithDB
from global_classes import Request


class PostService:

    @staticmethod
    def create_event(creator_token, group_token, event_description, users_list, group_name, event_time):
        event_id = communicateWithDB.create_event(creator_token, group_token, event_description,
                                                  users_list, group_name, event_time)
        queue_request = Request("planning", "event_invitation", users_list, event_id, group_name)
        messages_queue.put(queue_request)
        return {"event_id": event_id}

    @staticmethod
    def cancel_event(user_token, event_token):
        user_list = communicateWithDB.get_user_list(event_token)
        result, group_name = communicateWithDB.cancel_event(user_token, event_token)
        if result:
            queue_request = Request("planning", "event_cancellation", user_list, event_token, group_name)
            messages_queue.put(queue_request)
            return {"result": "success"}
        return {"result": "failure"}


class GetService:

    @staticmethod
    def view_events_user_name(user_name):
        event_tuples = communicateWithDB.view_user_events(user_name)
        return event_tuples

    @staticmethod
    def view_events_group(group_token):
        event_tuples = communicateWithDB.view_events_group(group_token)
        return event_tuples

    @staticmethod
    def view_events_creator(user_token):
        event_tuples = communicateWithDB.view_events_creator(user_token)
        return event_tuples
