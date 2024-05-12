from user_management_service.repository.dbManipulation import communicateWithDB


class PostService:

    @staticmethod
    def add_user(user_name, password, email):
        return communicateWithDB.add_user(user_name, password, email)

    @staticmethod
    def create_group(user_token, group_name, users_list):
        return communicateWithDB.create_group(creator_token=user_token, group_name=group_name, users_list=users_list)

    @staticmethod
    def add_user_to_group(group_token, user_name, creator_token):
        return communicateWithDB.add_user_to_group(group_token, user_name, creator_token)

    @staticmethod
    def delete_user_from_group(group_token, user_name, creator_token):
        return communicateWithDB.delete_user_from_group(group_token, user_name, creator_token)


class GetService:

    @staticmethod
    def user_authentication(user_name, password):
        user = communicateWithDB.get_user(user_name)
        if user is None:
            return False
        if user.password == password:
            return user.user_token
        return False

    @staticmethod
    def get_group_users(group_token):
        return communicateWithDB.get_group_users(group_token)

    @staticmethod
    def get_user_groups(user_token):
        return communicateWithDB.get_user_groups(user_token)

    @staticmethod
    def check_user_existence(user_name):
        user = communicateWithDB.get_user(user_name)
        return user is not None


class DeleteService:

    @staticmethod
    def delete_user(user_token):
        return communicateWithDB.delete_user(user_token)

    @staticmethod
    def delete_group(group_token, creator_token):
        return communicateWithDB.delete_group(group_token, creator_token)
