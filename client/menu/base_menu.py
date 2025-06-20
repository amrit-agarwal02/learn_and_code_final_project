from abc import ABC, abstractmethod
from client.api import APIClient

class BaseMenu(ABC):
    def __init__(self, api: APIClient):
        self.api = api

    @abstractmethod
    def show(self):
        pass

    def pause(self):
        input("Press Enter to continue...")
