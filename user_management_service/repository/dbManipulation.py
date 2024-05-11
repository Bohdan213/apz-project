from user_management_service import session, User, Group
import json


class communicateWithDB:

    @staticmethod
    def add_user(user_name, password):
        user = User(user_name=user_name, password=password)
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def get_user(user_name):
        user = session.query(User).filter_by(user_name=user_name).first()
        return user

    @staticmethod
    def create_group(creator_token, group_name, users_list):
        json_users_list = json.dumps(users_list)
        try:
            group = Group(creator_token=creator_token, group_name=group_name, users_list=json_users_list)
            session.add(group)
            session.commit()
            return f"Group with name: {group_name} created and users: {users_list} added"
        except Exception as e:
            return f"Error: {e}"

    def add_user_to_group(group_token, user_token):
        try:
            group = session.query(Group).filter_by(group_token=group_token).first()
            users_list_json = group.users_list
            users_list = json.loads(users_list_json)
            users_list.append(user_token)
            group.users_list = json.dumps(users_list)
            session.commit()
            return f"User with token: {user_token} added to group with token: {group_token}"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def get_group_users(group_token):
        try:
            group = session.query(Group).filter_by(group_token=group_token).first()
            return group.users_list
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def get_user_groups(user_token):
        try:
            groups = session.query(Group).filter_by(creator_token=user_token).all()
            return groups
        except Exception as e:
            return f"Error: {e}"
