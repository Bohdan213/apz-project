from user_management_service import db, User, Group
import json, uuid


class communicateWithDB:
    """
    A class that provides methods to communicate with the database for user management.

    Methods:
    - add_user(user_name, password, email): Adds a new user to the database.
    - get_user(user_name): Retrieves a user from the database based on the username.
    - create_group(creator_token, group_name, users_list): Creates a new group and adds users to it.
    - delete_group(group_token, creator_token): Deletes a group from the database.
    - add_user_to_group(group_token, user_name, creator_token): Adds a user to a group.
    - delete_user_from_group(group_token, user_name, creator_token): Deletes a user from a group.
    - get_group_users(group_token): Retrieves the list of users in a group.
    - get_group(group_token): Retrieves a group from the database based on the group token.
    - get_user_groups(user_token): Retrieves the groups created by a user.
    - delete_user(user_token): Deletes a user from the database.
    """
    @staticmethod
    def add_user(user_name, password, email):
        """
        Adds a new user to the database.

        Args:
        - user_name (str): The username of the user.
        - password (str): The password of the user.
        - email (str): The email address of the user.

        Returns:
        - str: The user token of the newly created user if successful, or an error message if unsuccessful.
        """
        try:
            user = User(user_name=user_name, password=password, email=email, user_token=str(uuid.uuid4()))
            db.session.add(user)
            db.session.commit()
            return user.user_token
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def get_user(user_name):
        """
        Retrieves a user from the database based on the username.

        Args:
        - user_name (str): The username of the user to retrieve.

        Returns:
        - User: The user object if found, or an error message if not found.
        """
        try:
            user = User.query.filter_by(user_name=user_name).first()
            return user
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def create_group(creator_token, group_name, users_list):
        """
        Create a new group with the given creator token, group name, and list of users.

        Parameters:
        - creator_token (str): The token of the user creating the group.
        - group_name (str): The name of the group.
        - users_list (list): A list of users to be added to the group.

        Returns:
        - tuple: A tuple containing a success message and the group token if the group is created successfully, 
                 otherwise an error message and None.
        """
        json_users_list = json.dumps(users_list)
        print(json_users_list)
        try:
            group = Group(creator_token=creator_token, group_name=group_name, users_list=json_users_list, group_token=str(uuid.uuid4()))
            db.session.add(group)
            db.session.commit()
            return f"Group with name: {group_name} created and users: {users_list} added", group.group_token
        except Exception as e:
            return f"Error: {e}", None

    @staticmethod
    def delete_group(group_token, creator_token):
        """
        Deletes a group from the database.

        Args:
            group_token (str): The token of the group to be deleted.
            creator_token (str): The token of the creator of the group.

        Returns:
            str: A message indicating the result of the deletion.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            group = Group.query.filter_by(group_token=group_token).first()
            if group is None:
                return f"Group with token: {group_token} does not exist"
            if group.creator_token == creator_token:
                db.session.delete(group)
                db.session.commit()
                return f"Group with token: {group_token} deleted"
            else:
                return "You are not the creator of this group"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def add_user_to_group(group_token, user_name, creator_token):
        """
        Adds a user to a group.

        Args:
            group_token (str): The token of the group.
            user_name (str): The name of the user to be added.
            creator_token (str): The token of the creator of the group.

        Returns:
            str: A message indicating the result of the operation.

        Raises:
            Exception: If an error occurs during the operation.
        """
        try:
            group = Group.query.filter_by(group_token=group_token).first()
            if group.creator_token == creator_token:
                if group is None:
                    return f"Group with token: {group_token} does not exist"
                # check if user exists
                user = User.query.filter_by(user_name=user_name).first()
                if user is None:
                    return f"User with name: {user_name} does not exist"
                users_list_json = group.users_list
                users_list = json.loads(users_list_json)
                users_list.append(user_name)
                group.users_list = json.dumps(users_list)
                db.session.commit()
                return f"User with name: {user_name} added to group with token: {group_token}"
            else:
                print(group.creator_token, creator_token)
                return "You are not the creator of this group"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def delete_user_from_group(group_token, user_name, creator_token):
        """
        Delete a user from a group.

        Args:
            group_token (str): The token of the group.
            user_name (str): The name of the user to be deleted.
            creator_token (str): The token of the group creator.

        Returns:
            str: A message indicating the result of the operation.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            group = Group.query.filter_by(group_token=group_token).first()
            if group is None:
                return f"Group with token: {group_token} does not exist"
            if group.creator_token == creator_token:
                # check if user exists
                user = User.query.filter_by(user_name=user_name).first()
                if user is None:
                    return f"User with name: {user_name} does not exist"
                users_list_json = group.users_list
                users_list = json.loads(users_list_json)
                users_list.remove(user_name)
                group.users_list = json.dumps(users_list)
                db.session.commit()
                return f"User with name: {user_name} deleted from group with token: {group_token}"
            else:
                return "You are not the creator of this group"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def get_group_users(group_token):
        """
        Retrieves the list of users belonging to a specific group.

        Parameters:
        - group_token (str): The token of the group.

        Returns:
        - list: The list of users belonging to the group.

        Raises:
        - str: If the group with the specified token does not exist.
        - str: If an error occurs during the retrieval process.
        """        
        try:
            group = Group.query.filter_by(group_token=group_token).first()
            if group is None:
                return f"Group with token: {group_token} does not exist"
            return group.users_list
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def get_group(group_token):
        """
        Retrieve a group from the database based on the given group token.

        Parameters:
        - group_token (str): The token of the group to retrieve.

        Returns:
        - group (Group): The group object retrieved from the database.

        Raises:
        - Exception: If an error occurs while retrieving the group.

        """
        try:
            group = Group.query.filter_by(group_token=group_token).first()
            return group
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def get_user_groups(user_token):
        """
        Retrieves all groups created by a user.

        Args:
            user_token (str): The token of the user.

        Returns:
            list: A list of Group objects created by the user.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        
        try:
            groups = Group.query.filter_by(creator_token=user_token).all()
            return groups
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def delete_user(user_token):
        """
        Deletes a user from the database based on the provided user token.

        Args:
            user_token (str): The token of the user to be deleted.

        Returns:
            str: A message indicating the success or failure of the deletion.

        Raises:
            Exception: If an error occurs during the deletion process.
        
        """
        try:
            user = User.query.filter_by(user_token=user_token).first()
            db.session.delete(user)
            db.session.commit()
            return f"User with token: {user_token} deleted"
        except Exception as e:
            return f"Error: {e}"
