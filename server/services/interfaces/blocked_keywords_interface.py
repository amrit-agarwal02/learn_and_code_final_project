from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IBlockedKeywordsService(ABC):
    
    @abstractmethod
    def add_keyword(self, keyword: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def remove_keyword(self, keyword: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_all_blocked_keywords(self) -> List[str]:
        pass 