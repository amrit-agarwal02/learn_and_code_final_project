from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

T = TypeVar('T')


class BaseDatabase(ABC, Generic[T]):

    @abstractmethod
    def insert(self, new_obj: T):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T:
        pass

    @abstractmethod
    def update_by_id(self, id: int, updated_obj: T):
        pass

    @abstractmethod
    def delete_by_id(self, id: int):
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass
