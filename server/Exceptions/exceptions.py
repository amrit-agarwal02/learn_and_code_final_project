class UserAlreadyExistsException(Exception):

    def __init__(self, message="User with this ID already exists"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self, message="User with this ID not found"):
        self.message = message
        super().__init__(self.message)

class ArticleNotFoundException(Exception):
    def __init__(self, message="Article not found"):
        self.message = message
        super().__init__(self.message)

class ArticleAlreadyExistsException(Exception):
    def __init__(self, message="Article already exists"):
        self.message = message
        super().__init__(self.message)

class CategoryNotFoundException(Exception):
    def __init__(self, message="Category not found"):
        self.message = message
        super().__init__(self.message)

class CategoryAlreadyExistsException(Exception):
    def __init__(self, message="Category already exists"):
        self.message = message
        super().__init__(self.message)


class ExternalServerNotFoundException(Exception):
    def __init__(self, message="External server not found"):
        self.message = message
        super().__init__(self.message)

class ExternalServerAPIKeyInvalidException(Exception):
    def __init__(self, message="External server API key is invalid"):
        self.message = message
        super().__init__(self.message)

class AdminPermissionDeniedException(Exception):
    def __init__(self, message="Admin permission denied"):
        self.message = message
        super().__init__(self.message)