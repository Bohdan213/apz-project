class User:
    """
    Represents a user with a name and email address.
    """

    def __init__(self, user_name: str, user_email: str):
        """
        Initializes a new instance of the User class.

        Args:
            user_name (str): The name of the user.
            user_email (str): The email address of the user.
        """
        self.user_name = user_name
        self.user_email = user_email

    def __str__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object.
        """
        return f"User Name: {self.user_name}, User Email: {self.user_email}"

    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object.
        """
        return f"User Name: {self.user_name}, User Email: {self.user_email}"

    def __eq__(self, other):
        """
        Checks if the User object is equal to another User object.

        Args:
            other (User): The other User object to compare.

        Returns:
            bool: True if the User objects are equal, False otherwise.
        """
        return self.user_name == other.user_name


class Request:
    """
    Represents a request made by a service.

    Args:
        source_service (str): The source service making the request. Must be either 'user_management' or 'planning'.
        request_type (str): The type of request. For 'user_management' service, must be either 'group_addition' or 'group_removal'.
                            For 'planning' service, must be either 'event_invitation' or 'event_cancellation'.
        request_data (dict): The data associated with the request. Should contain a list of User instances in the 'users_list' key.
                             Optional keys include 'event_name', 'event_time', and 'group_name'.

    Attributes:
        source_service (str): The source service making the request.
        request_type (str): The type of request.
        users_list (list): A list of User instances associated with the request.
        event_name (str): The name of the event (if applicable).
        event_time (str): The time of the event (if applicable).
        group_name (str): The name of the group (if applicable).
    """

    def __init__(self, source_service: str, request_type: str, request_data: dict):
        if not source_service in ["user_management", "planning"]:
            raise ValueError("Invalid source service. Please provide either 'user_management' or 'planning' as the source service.")
        if source_service == "user_management" and not request_type in ["group_addition", "group_removal"]:
            raise ValueError("Invalid request type. Please provide either 'group_addition' or 'group_removal' as the request type.")
        if source_service == "planning" and not request_type in ['event_invitation', 'event_cancellation']:
            raise ValueError("Invalid request type. Please provide either 'event_invitation' or 'event_cancellation' as the request type.")
        if not all(isinstance(user, User) for user in request_data['users_list']):
            raise ValueError("Invalid request data. All request data should be instances of the User class.")
        self.source_service = source_service
        self.request_type = request_type
        self.users_list = request_data['users_list']
        self.event_name = request_data.get('event_name', None)
        self.event_time = request_data.get('event_time', None)
        self.group_name = request_data.get('group_name', None)
