from flask_restful import Resource, reqparse

from user_management_service.services.userService import PostService, GetService, DeleteService

class UserManagementService(Resource):
    """
    Represents a user management service.

    This class handles various operations related to user management, such as authentication, group creation,
    adding users to groups, deleting users and groups, and more.

    Attributes:
        auth_parser (RequestParser): Parser for authentication endpoint.
        group_parser (RequestParser): Parser for group creation endpoint.
        group_token_parser (RequestParser): Parser for group token endpoint.
        add_user_to_group_parser (RequestParser): Parser for adding user to group endpoint.
        add_user_parser (RequestParser): Parser for adding user endpoint.
        delete_user_parser (RequestParser): Parser for deleting user endpoint.
        group_users_parser (RequestParser): Parser for getting group users endpoint.
        user_existance_parser (RequestParser): Parser for checking user existence endpoint.
    """

    def __init__(self):
        # Existing parsers
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

        # New parsers for additional endpoints
        self.group_users_parser = reqparse.RequestParser()
        self.group_users_parser.add_argument('group_token', required=True, help="Group token is required")

        self.user_existance_parser = reqparse.RequestParser()
        self.user_existance_parser.add_argument('user_name', required=True, help="Username is required")

    def get(self, operation):
        """
        Handles GET requests for different operations.

        Args:
            operation (str): The operation to perform.

        Returns:
            dict: The response data.

        Raises:
            KeyError: If the operation is not supported.
        """
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

    def post(self, operation):
        """
        Handles POST requests for different operations.

        Args:
            operation (str): The operation to perform.

        Returns:
            dict: The response data.

        Raises:
            KeyError: If the operation is not supported.
        """
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

    def delete(self, operation):
        """
        Handles DELETE requests for different operations.

        Args:
            operation (str): The operation to perform.

        Returns:
            str: The response message.

        Raises:
            KeyError: If the operation is not supported.
        """
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
