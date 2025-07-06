from abc import ABC, abstractmethod
from typing import List, Dict, Any
from server.schemas.news import NewsArticleCreate


class IExternalAPIService(ABC):
    """Interface for external API service operations."""
    
    @abstractmethod
    def fetch_news(self, api_config: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch news from external API."""
        pass
    
    @abstractmethod
    def parse_articles(self, data: Dict[str, Any], server_id: int) -> List[NewsArticleCreate]:
        """Parse articles from API response."""
        pass
    
    @abstractmethod
    def get_api_name(self) -> str:
        """Get the name of the API service."""
        pass 