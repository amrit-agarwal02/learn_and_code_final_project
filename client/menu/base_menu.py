from abc import ABC, abstractmethod
from client.api.user_client import UserClient

class BaseMenu(ABC):
    def __init__(self, api: UserClient):
        self.api = api

    @abstractmethod
    def show(self):
        pass
