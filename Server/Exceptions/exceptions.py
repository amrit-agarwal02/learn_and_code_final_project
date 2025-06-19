class UserAlreadyExistsException(Exception):

    def __init__(self, message="User with this ID already exists"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self, message="User with this ID not found"):
        self.message = message
        super().__init__(self.message)