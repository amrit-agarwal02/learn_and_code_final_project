from abc import ABC, abstractmethod
from client.api.api_client import APIClient

class BaseMenu(ABC):
    def __init__(self, api: APIClient):
        self.api = api

    @abstractmethod
    def show(self):
        pass
