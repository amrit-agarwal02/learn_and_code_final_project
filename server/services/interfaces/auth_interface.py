from abc import ABC, abstractmethod
from server.schemas.auth import UserCredentials
from server.schemas.user import UserCreate


class IAuthService(ABC):
    
    @abstractmethod
    def register_user(self, user: UserCreate):
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str):
        pass
    
    @abstractmethod
    def login(self, user_data: UserCredentials):
        pass 