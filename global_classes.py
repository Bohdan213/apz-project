class User:
    def __init__(self, user_token, user_name, user_email):
        self.user_name = user_name
        self.user_email = user_email

    def __str__(self):
        return f"User Name: {self.user_name}, User Email: {self.user_email}"

    def __repr__(self):
        return f"User Name: {self.user_name}, User Email: {self.user_email}"

    def __eq__(self, other):
        return self.user_name == other.user_name


class Request:
    def __init__(self, source_service, request_type, request_data, event_id=None, group_name=None):
        if not source_service in ["user_manadgement", "planning"]:
            raise ValueError("Invalid source service. Please provide either 'user_manadgement' or 'planning' as the source service.")
        if source_service == "user_manadgement" and not request_type in ["group_addition", "group_removal"]:
            raise ValueError("Invalid request type. Please provide either 'group_addition' or 'group_removal' as the request type.")
        if source_service == "planning" and not request_type in ['event_invitation', 'event_cancellation']:
            raise ValueError("Invalid request type. Please provide either 'event_invitation' or 'event_cancellation' as the request type.")
        if not all(isinstance(user, User) for user in request_data):
            raise ValueError("Invalid request data. All request data should be instances of the User class.")
        self.source_service = source_service
        self.request_type = request_type
        self.request_data = request_data
        self.event_id = event_id
        self.group_name = group_name
