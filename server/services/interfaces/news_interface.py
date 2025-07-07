from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from server.schemas.news import NewsArticleCreate
from server.services.interfaces.external_api_interface import IExternalAPIService


class INewsService(ABC):
    
    @abstractmethod
    def get_all_apis(self) -> List[Dict[str, Any]]:
        pass

    
    @abstractmethod
    def sync_news_from_api(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def today_news(self, user_id: int) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_news_by_date_range(self, user_id: int, start_date: str, end_date: str, category_name: str) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_news_by_keyword(self, user_id: int, search_request: str) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def save_news_article_for_user(self, user_id: int, article_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_saved_articles_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def delete_saved_articles_for_user(self, user_id: int, article_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_article_by_id(self, user_id: int, article_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def mark_article_as_read(self, user_id: int, article_id: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def filter_blocked_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def personalize_articles(self, user_id: int, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass 