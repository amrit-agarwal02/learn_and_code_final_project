from fastapi import FastAPI, HTTPException
from Server.Models.user import User
from Server.Services.auth_service import AuthService
from Server.Exceptions.exceptions import UserAlreadyExistsException, UserNotFoundException
from Server.config.http_status_code import HTTP_BAD_REQUEST, HTTP_NOT_FOUND
from Server.schemas.auth import UserCredentials
from Server.schemas.user import UserCreate


class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def login(self, user_data: UserCredentials) -> User:
        try:
            return self.auth_service.login(user_data)
        except Exception as e:
            raise HTTPException(status_code=HTTP_BAD_REQUEST, detail=str(e))

    def register(self, user: UserCreate):
            try:
                db_user = self.auth_service.register_user(user)
                return {
                    "user_id": db_user["user_id"],
                    "user_name": db_user["user_name"],
                    "email": db_user["email"],
                    "role": db_user["role"],
                    "created_at": db_user["created_at"]
                }
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
