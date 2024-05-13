from planning_service import messages_queue
from planning_service.repository.dbManipulation import communicateWithDB
from global_classes import Request


class PostService:

    @staticmethod
    def create_event(creator_token, group_token, event_description, users_list, group_name, event_time, event_name):
        event_id = communicateWithDB.create_event(creator_token, group_token, event_description,
                                                  users_list, group_name, event_time, event_name)
        event_info = communicateWithDB.get_event_info(event_id)
        if event_info is None:
            return {"result": "something went wrong, event not created"}, 400
        queue_request = Request("planning", "event_invitation", event_info)
        messages_queue.put(queue_request)
        return {"event_id": event_id}

    @staticmethod
    def cancel_event(user_token, event_token):
        event_info = communicateWithDB.get_event_info(event_token)
        if event_info is None:
            return {"result": "event not found with this event token"}, 400
        result = communicateWithDB.cancel_event(user_token, event_token)
        if result:
            queue_request = Request("planning", "event_cancellation", event_info)
            messages_queue.put(queue_request)
            return {"result": "success"}
        return {"result": "failure"}


class GetService:

    @staticmethod
    def view_events_user_name(user_name):
        event_tuples = communicateWithDB.view_user_events(user_name)
        if not event_tuples:
            return {"result": "no events found with this user name"}, 400
        return event_tuples

    @staticmethod
    def view_events_group(group_token):
        event_tuples = communicateWithDB.view_events_group(group_token)
        if not event_tuples:
            return {"result": "no events found with this group token"}, 400
        return event_tuples

    @staticmethod
    def view_events_creator(user_token):
        event_tuples = communicateWithDB.view_events_creator(user_token)
        if not event_tuples:
            return {"result": "no events found with this user token"}, 400
        return event_tuples
