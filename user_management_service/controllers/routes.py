from flask_restful import Resource, reqparse

from user_management_service.services.userService import PostService, GetService


class UserManagementService(Resource):

    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument()

        self.get_parser = reqparse.RequestParser()


    def post(self):
        return None


    def get(self):
        return None