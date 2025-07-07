from abc import ABC, abstractmethod
from typing import List, Dict, Any
from server.schemas.category import CategoryCreate


class ICategoryService(ABC):
    
    @abstractmethod
    def get_all_categories(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def create_category(self, category: CategoryCreate) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def update_category(self, category_id: int, name: str = None, description: str = None) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def delete_category(self, category_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def hide_category(self, category_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def set_category_visibility(self, category_id: int, is_visible: bool) -> Dict[str, Any]:
        pass 