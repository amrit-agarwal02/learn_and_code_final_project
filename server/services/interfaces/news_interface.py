from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from server.schemas.news import NewsArticleCreate
from server.services.interfaces.external_api_interface import IExternalAPIService


class INewsService(ABC):
    """Interface for news service operations."""
    
    @abstractmethod
    def get_all_apis(self) -> List[Dict[str, Any]]:
        """Get all available external APIs."""
        pass
    
    @abstractmethod
    def find_working_api_with_data(self) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], Optional[IExternalAPIService]]:
        """
        Find the first working API and return its data.
        Returns tuple of (working_api, fetched_data, api_service) or (None, None, None) if all fail.
        """
        pass
    
    @abstractmethod
    def classify_article(self, article: NewsArticleCreate, article_id: int) -> None:
        """Classify an article and map it to a category."""
        pass
    
    @abstractmethod
    def fetch_news(self, url: str, active_server_id: int) -> Dict[str, Any]:
        """Fetch news from external API."""
        pass
    
    @abstractmethod
    def parse_articles_newsapi(self, data: Dict[str, Any], server_id: int) -> List[NewsArticleCreate]:
        """Parse articles from NewsAPI response."""
        pass
    
    @abstractmethod
    def store_articles_thenewsapi(self, data: Dict[str, Any], server_id: int) -> List[NewsArticleCreate]:
        """Store articles from TheNewsAPI response."""
        pass
    
    @abstractmethod
    def store_articles(self, articles: List[NewsArticleCreate], active_api: Dict[str, Any]) -> Dict[str, Any]:
        """Store articles in the database."""
        pass
    
    @abstractmethod
    def sync_news_from_api(self) -> Dict[str, Any]:
        """Synchronize news from external APIs."""
        pass
    
    @abstractmethod
    def today_news(self, user_id: int) -> List[Dict[str, Any]]:
        """Get today's news for a user."""
        pass
    
    @abstractmethod
    def get_news_by_date_range(self, user_id: int, start_date: str, end_date: str, category_name: str) -> List[Dict[str, Any]]:
        """Get news articles within a date range for a specific category."""
        pass
    
    @abstractmethod
    def get_news_by_keyword(self, user_id: int, search_request: str) -> List[Dict[str, Any]]:
        """Search news articles by keyword."""
        pass
    
    @abstractmethod
    def save_news_article_for_user(self, user_id: int, article_id: int) -> Dict[str, Any]:
        """Save an article for a specific user."""
        pass
    
    @abstractmethod
    def get_saved_articles_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get saved articles for a user."""
        pass
    
    @abstractmethod
    def delete_saved_articles_for_user(self, user_id: int, article_id: int) -> Dict[str, Any]:
        """Delete a saved article for a user."""
        pass
    
    @abstractmethod
    def get_article_by_id(self, user_id: int, article_id: int) -> Dict[str, Any]:
        """Get a specific article by ID."""
        pass
    
    @abstractmethod
    def mark_article_as_read(self, user_id: int, article_id: int) -> Dict[str, Any]:
        """Mark an article as read for a user."""
        pass
    
    @abstractmethod
    def filter_blocked_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out articles containing blocked keywords."""
        pass
    
    @abstractmethod
    def personalize_articles(self, user_id: int, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Personalize articles based on user preferences."""
        pass 