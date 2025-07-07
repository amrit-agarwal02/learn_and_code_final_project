from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IReportService(ABC):
    
    @abstractmethod
    def report_article(self, article_id: int, user_id: int, reason: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_reported_articles(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def hide_article(self, article_id: int) -> Dict[str, Any]:
        pass 