from user_management_service.repository.dbManipulation import communicateWithDB
from user_management_service.services.messageCommunication import UserGroupNotifier

class PostService:
    """
    This class provides methods for managing users and groups in the user management service.
    """

    @staticmethod
    def add_user(user_name, password, email):
        """
        Adds a new user to the user management service.

        Args:
            user_name (str): The name of the user.
            password (str): The password of the user.
            email (str): The email address of the user.

        Returns:
            bool: True if the user was successfully added, False otherwise.
        """
        return communicateWithDB.add_user(user_name, password, email)

    @staticmethod
    def create_group(user_token, group_name, users_list):
        """
        Creates a new group in the user management service.

        Args:
            user_token (str): The token of the user creating the group.
            group_name (str): The name of the group.
            users_list (list): A list of user names to be added to the group.

        Returns:
            bool: True if the group was successfully created, False otherwise.
        """
        notifier = UserGroupNotifier(users_list, group_name)
        notifier.notify_addition()
        return communicateWithDB.create_group(creator_token=user_token, group_name=group_name, users_list=users_list)

    @staticmethod
    def add_user_to_group(group_token, user_name, creator_token):
        """
        Adds a user to a group in the user management service.

        Args:
            group_token (str): The token of the group.
            user_name (str): The name of the user to be added to the group.
            creator_token (str): The token of the user performing the action.

        Returns:
            bool: True if the user was successfully added to the group, False otherwise.
        """
        group = communicateWithDB.get_group(group_token)
        if group is None:
            return "Group does not exist", 400
        notifier = UserGroupNotifier([user_name], group.group_name)
        notifier.notify_addition()
        return communicateWithDB.add_user_to_group(group_token, user_name, creator_token), 200

    @staticmethod
    def delete_user_from_group(group_token, user_name, creator_token):
        """
        Deletes a user from a group in the user management service.

        Args:
            group_token (str): The token of the group.
            user_name (str): The name of the user to be deleted from the group.
            creator_token (str): The token of the user performing the action.

        Returns:
            bool: True if the user was successfully deleted from the group, False otherwise.
        """
        group = communicateWithDB.get_group(group_token)
        if group is None:
            return "Group does not exist", 400
        notifier = UserGroupNotifier([user_name], communicateWithDB.get_group(group_token).group_name)
        notifier.notify_removal()
        return communicateWithDB.delete_user_from_group(group_token, user_name, creator_token)


class GetService:
    """
    This class provides methods for retrieving user information and performing user authentication.
    """

    @staticmethod
    def user_authentication(user_name, password):
        """
        Authenticates a user based on the provided username and password.

        Args:
            user_name (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool or str: Returns the user token if authentication is successful, otherwise False.
        """
        user = communicateWithDB.get_user(user_name)
        if user is None:
            return False
        if user.password == password:
            return user.user_token
        return False

    @staticmethod
    def get_group_users(group_token):
        """
        Retrieves the users belonging to a specific group.

        Args:
            group_token (str): The token of the group.

        Returns:
            list: A list of users belonging to the group.
        """
        return communicateWithDB.get_group_users(group_token)

    @staticmethod
    def get_user_groups(user_token):
        """
        Retrieves the groups that a user belongs to.

        Args:
            user_token (str): The token of the user.

        Returns:
            list: A list of groups that the user belongs to.
        """
        return communicateWithDB.get_user_groups(user_token)

    @staticmethod
    def check_user_existence(user_name):
        """
        Checks if a user with the given username exists.

        Args:
            user_name (str): The username to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        user = communicateWithDB.get_user(user_name)
        if user is None:
            print(f"User with name: {user_name} does not exist")
        return user is not None


class DeleteService:
    """
    This class provides methods to delete users and groups from the user management service.

    Methods:
        delete_user(user_token): Deletes a user with the given user token.
        delete_group(group_token, creator_token): Deletes a group with the given group token, 
            and notifies the group members about the removal.
    """

    @staticmethod
    def delete_user(user_token):
        """
        Deletes a user from the database.

        Args:
            user_token (str): The token of the user to be deleted.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """
        return communicateWithDB.delete_user(user_token)

    @staticmethod
    def delete_group(group_token, creator_token):
            """
            Deletes a group.

            Args:
                group_token (str): The token of the group to be deleted.
                creator_token (str): The token of the user who created the group.

            Returns:
                bool: True if the group was successfully deleted, False otherwise.
            """
            group = communicateWithDB.get_group(group_token)
            if group is None:
                return "Group does not exist", 400
            group_users = group.users_list
            notifier = UserGroupNotifier(group_users, group.group_name)
            notifier.notify_removal()
            return communicateWithDB.delete_group(group_token, creator_token)
