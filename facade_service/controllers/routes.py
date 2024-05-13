from flask_restful import Resource, reqparse

from facade_service.services.facadeService import PostService, GetService, DeleteService


class FacadeService(Resource):

    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.get_parser = reqparse.RequestParser()
        
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
        
        self.auth_parser = reqparse.RequestParser()
        self.auth_parser.add_argument('user_name', required=True, help="Username is required")
        self.auth_parser.add_argument('password', required=True, help="Password is required")

        self.group_parser = reqparse.RequestParser()
        self.group_parser.add_argument('user_token', required=True, help="User token is required")
        self.group_parser.add_argument('group_name', required=True, help="Group name is required")
        self.group_parser.add_argument(
            'users_list', required=True, help="List of users is required", type=list, location='json')

        self.group_token_parser = reqparse.RequestParser()
        self.group_token_parser.add_argument('group_token', required=True, help="Group token is required")
        self.group_token_parser.add_argument('user_token', required=True, help="User token is required")

        self.add_user_to_group_parser = reqparse.RequestParser()
        self.add_user_to_group_parser.add_argument('group_token', required=True, help="Group token is required")
        self.add_user_to_group_parser.add_argument('user_name', required=True, help="User name is required")
        self.add_user_to_group_parser.add_argument('user_token', required=True, help="User token is required")

        self.add_user_parser = reqparse.RequestParser()
        self.add_user_parser.add_argument('user_name', required=True, help="Username is required")
        self.add_user_parser.add_argument('password', required=True, help="Password is required")
        self.add_user_parser.add_argument('email', required=True, help="Email is required")

        self.delete_user_parser = reqparse.RequestParser()
        self.delete_user_parser.add_argument('user_token', required=True, help="User token is required")

        self.group_users_parser = reqparse.RequestParser()
        self.group_users_parser.add_argument('group_token', required=True, help="Group token is required")

        self.user_existance_parser = reqparse.RequestParser()
        self.user_existance_parser.add_argument('user_name', required=True, help="Username is required")


    def get(self, operation):
        if operation == "authenticate":
            args = self.auth_parser.parse_args()
            user_name = args['user_name']
            password = args['password']

            user_token = GetService.user_authentication(user_name, password)
            return {'user_token': user_token}, 200

        if operation == "get_group_users":
            args = self.group_users_parser.parse_args()
            group_token = args['group_token']
            # Retrieve the list of users in the group (stubbed response)
            users_list = GetService.get_group_users(group_token)
            return {'users_list': users_list}, 200

        elif operation == "user_existance":
            args = self.user_existance_parser.parse_args()
            user_name = args['user_name']
            user_exists = GetService.check_user_existence(user_name)
            return {'exists': user_exists}, 200
        
        elif operation == "view_events_usÍer_name":
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

    def post(self, operation):
        if operation == "create_group":
            args = self.group_parser.parse_args()
            user_token = args['user_token']
            group_name = args['group_name']
            users_list = args['users_list']
            _, group_token = PostService.create_group(user_token, group_name, users_list)
            print(_)
            return {'group_token': group_token}, 201

        elif operation == "add_user_to_group":
            args = self.add_user_to_group_parser.parse_args()
            group_token = args['group_token']
            user_name = args['user_name']
            creator_token = args['user_token']
            print(PostService.add_user_to_group(group_token, user_name, creator_token))
            return "added", 200

        elif operation == "delete_user_from_group":
            args = self.add_user_to_group_parser.parse_args()
            group_token = args['group_token']
            user_name = args['user_name']
            user_token = args['user_token']
            print(PostService.delete_user_from_group(group_token, user_name, user_token))
            return "deleted", 200

        elif operation == "add_user":
            args = self.add_user_parser.parse_args()
            user_name = args['user_name']
            password = args['password']
            email = args['email']
            user_token = PostService.add_user(user_name, password, email)
            return {'user_token': user_token}, 201

        elif operation == "create_event":
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

    def delete(self, operation):
        if operation == "delete_group":
            args = self.group_token_parser.parse_args()
            group_token = args['group_token']
            user_token = args['user_token']
            print(DeleteService.delete_group(group_token, user_token))
            return "deleted", 200

        elif operation == "delete_user":
            args = self.delete_user_parser.parse_args()
            user_token = args['user_token']
            print(DeleteService.delete_user(user_token))
            return "user_deleted", 200
        
        elif operation == "cancel_event":
            args = self.delete_parser.parse_args()
            user_token = args['user_token']
            event_token = args['event_token']
            return PostService.cancel_event(user_token, event_token)
        return None