from abc import ABC, abstractmethod
from typing import List, Dict, Any
from server.schemas.news import NewsArticleCreate


class IExternalAPIService(ABC):
    
    @abstractmethod
    def fetch_news(self, api_config: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def parse_articles(self, data: Dict[str, Any], server_id: int) -> List[NewsArticleCreate]:
        pass
    
    @abstractmethod
    def get_api_name(self) -> str:
        pass

    @abstractmethod
    def orchestrate_store_articles(self, articles_data, server_id):
        pass