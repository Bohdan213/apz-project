from user_management_service.repository import dbManipulation


class PostService:

    @staticmethod
    def add_user(user_name, password):
        return "Add user"

    @staticmethod
    def create_group(user_token, group_name):
        return "Create group"

    @staticmethod
    def add_user_to_group(group_token, user_token):
        return "Add user to group"


class GetService:

    @staticmethod
    def user_authentication(user_name, password):
        return "Get messages"

    @staticmethod
    def get_group_users(group_token):
        return "Get messages"

    @staticmethod
    def get_user_groups(user_token):
        return "Get messages"
