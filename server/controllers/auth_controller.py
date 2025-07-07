from server.services.auth_service import AuthService
from server.schemas.auth import UserCredentials
from server.schemas.user import UserCreate


class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def login(self, user_data: UserCredentials):
        return self.auth_service.login(user_data)

    def register(self, user: UserCreate):
        db_user = self.auth_service.register_user(user)
        return {
            "user_id": db_user["user_id"],
            "user_name": db_user["user_name"],
            "email": db_user["email"],
            "role": db_user["role"],
            "created_at": db_user["created_at"]
        }

