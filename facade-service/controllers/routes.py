from flask_restful import Resource, reqparse

from facade_service.services.facadeService import PostService, GetService


class FacadeService(Resource):

    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument()

        self.get_parser = reqparse.RequestParser()


    def post(self):
        return PostService.post_message()


    def get(self):
        return GetService.get_messages()