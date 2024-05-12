from user_management_service import db, User, Group
import json, uuid


class communicateWithDB:

    @staticmethod
    def add_user(user_name, password, email):
        user = User(user_name=user_name, password=password, email=email, user_token=str(uuid.uuid4()))
        db.session.add(user)
        db.session.commit()
        return user.user_token

    @staticmethod
    def get_user(user_name):
        user = User.query.filter_by(user_name=user_name).first()
        return user

    @staticmethod
    def create_group(creator_token, group_name, users_list):
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
        try:
            group = Group.query.filter_by(group_token=group_token).first()
            if group is None:
                return f"Group with token: {group_token} does not exist"
            return group.users_list
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def get_user_groups(user_token):
        try:
            groups = Group.query.filter_by(creator_token=user_token).all()
            return groups
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def delete_user(user_token):
        try:
            user = User.query.filter_by(user_token=user_token).first()
            db.session.delete(user)
            db.session.commit()
            return f"User with token: {user_token} deleted"
        except Exception as e:
            return f"Error: {e}"
