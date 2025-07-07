from pydantic import EmailStr
from server.repositories.user_repo import UserRepository
from server.schemas.auth import UserCredentials
from server.schemas.user import UserCreate
from server.utils.password_utils import verify_password
from server.utils.jwt_handler import create_access_token
from server.services.interfaces.auth_interface import IAuthService
from server.Exceptions.exceptions import UserAlreadyExistsException,UserNotFoundException


class AuthService(IAuthService):
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, user: UserCreate):
        if self.user_repo.get_by_email(user.email):
            raise UserAlreadyExistsException("Email already registered")
        return self.user_repo.create(user)

    def get_user_by_email(self, email: EmailStr):
        user = self.user_repo.get_by_email(email)
        if user is None:
            raise UserNotFoundException("Invalid Email")
        return user

    def login(self, user_data: UserCredentials):
        user = self.get_user_by_email(user_data.email)
        if not user:
            raise ValueError("Incorrect Email")
        if(verify_password(plain_password= user_data.password,
                           hashed_password= user['password'])):
           status = "User Logged in Successfully"
           token_payload = {
               "sub": user["email"],
               "user_id": user["user_id"],
               "user_name": user["user_name"],
               "role": user["role"]
           }
           access_token = create_access_token(token_payload)
        else:
            raise ValueError("Incorrect Password")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_name": user["user_name"],
            "user_role": user["role"]
        }