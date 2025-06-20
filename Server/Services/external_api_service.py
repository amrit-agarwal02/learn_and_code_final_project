import requests
from Server.Repositories.news_repo import NewsRepository
from Server.Repositories.category_repo import CategoryRepository
from Server.schemas.news import NewsArticleCreate
from Server.Repositories.external_server_repo import ExternalServerRepository
from Server.config.constants import API_URL
from Server.Services.category_classifier import CategoryClassifier
from Server.Services.category_service import CategoryService
from abc import ABC, abstractmethod
from loguru import logger


class ExternalAPIService(ABC):

    @abstractmethod
    def get_news_articles(self):
        pass

    @abstractmethod
    def fetch_news(self):
        pass

class NewsAPIService(ExternalAPIService):

    def __init__(self, active_api):
        self.api_url = API_URL.get("NewsAPI")
        active_api_url = API_URL.get(active_api["server_name"])
        active_api_server_id = active_api["server_id"]

    def get_news_articles(self):
        pass

    def fetch_news(self, active_api):
        try:
            response = requests.get(active_api["url"])
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
        return None

    def fetch_news_from_API(self):
        pass

    # def parse_news(self, ):

class TheNewsAPIService(ExternalAPIService):

    def get_news_articles(self):
        pass

    def fetch_news(self, active_api):
        pass

    def parse_news(self):
        pass

    def store_news_articles(self):
        pass


