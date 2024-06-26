from flask_restful import Resource, reqparse

from planning_service.services.planningService import PostService, GetService


class PlanningService(Resource):
    """
    This class represents the Planning Service resource.

    Attributes:
        post_parser (RequestParser): The request parser for POST requests.
        delete_parser (RequestParser): The request parser for DELETE requests.
        view_events_user_name_parser (RequestParser): The request parser for GET requests to view events by user name.
        view_events_group_parser (RequestParser): The request parser for GET requests to view events by group.
        view_events_creator_parser (RequestParser): The request parser for GET requests to view events by creator.
    """

    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('user_token', required=True, help="User token is required")
        self.post_parser.add_argument('group_token', required=True, help="Group name is required")
        self.post_parser.add_argument('description', required=True, help="Description is required")
        self.post_parser.add_argument('users_list', required=True, help="List of users", type=list, location='json')
        self.post_parser.add_argument('group_name', required=True, help="Group name is required")
        self.post_parser.add_argument('event_time', required=True, help="Event time is required")
        self.post_parser.add_argument('event_name', required=True, help="Event name is required")

        self.delete_parser = reqparse.RequestParser()
        self.delete_parser.add_argument('user_token', required=True, help="User token is required")
        self.delete_parser.add_argument('event_token', required=True, help="Event token is required")

        self.view_events_user_name_parser = reqparse.RequestParser()
        self.view_events_user_name_parser.add_argument('user_name', required=True, help="User token is required")

        self.view_events_group_parser = reqparse.RequestParser()
        self.view_events_group_parser.add_argument('group_token', required=True, help="Group token is required")

        self.view_events_creator_parser = reqparse.RequestParser()
        self.view_events_creator_parser.add_argument('user_token', required=True, help="User token is required")


    def post(self, operation=None):
        """
        Handles POST requests.

        Args:
            operation (str, optional): The operation to perform. Defaults to None.

        Returns:
            dict: The response data.
        """
        if operation == "create_event":
            args = self.post_parser.parse_args()
            user_token = args['user_token']
            group_token = args['group_token']
            description = args['description']
            users_list = args['users_list']
            group_name = args['group_name']
            event_time = args['event_time']
            event_name = args['event_name']

            event_token = PostService.create_event(user_token, group_token, description,
                                                   users_list, group_name, event_time, event_name)
            return {'event_token': event_token}, 200
        return None

    def delete(self, operation=None):
        """
        Handles DELETE requests.

        Args:
            operation (str, optional): The operation to perform. Defaults to None.

        Returns:
            dict: The response data.
        """
        if operation == "cancel_event":
            args = self.delete_parser.parse_args()
            user_token = args['user_token']
            event_token = args['event_token']
            return PostService.cancel_event(user_token, event_token)
        return None

    def get(self, operation=None):
        """
        Handles GET requests.

        Args:
            operation (str, optional): The operation to perform. Defaults to None.

        Returns:
            dict: The response data.
        """
        if operation == "view_events_user_name":
            args = self.view_events_user_name_parser.parse_args()
            user_name = args['user_name']
            events = GetService.view_events_user_name(user_name)
            return {'events': events}, 200
        elif operation == "view_events_group":
            args = self.view_events_group_parser.parse_args()
            group_token = args['group_token']
            events = GetService.view_events_group(group_token)
            return {'events': events}, 200
        elif operation == "view_events_creator":
            args = self.view_events_creator_parser.parse_args()
            user_token = args['user_token']
            events = GetService.view_events_creator(user_token)
            return {'events': events}, 200

        return None