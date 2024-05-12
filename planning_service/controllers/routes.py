from flask_restful import Resource, reqparse

from planning_service.services.planningService import PostService, GetService


class PlanningService(Resource):

    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument()

        self.get_parser = reqparse.RequestParser()


    def post(self):
        return None


    def get(self):
        return None