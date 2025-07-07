import requests
from typing import List, Dict, Any

from server.repositories.category_repo import CategoryRepository
from server.repositories.news_repo import NewsRepository
from server.services.interfaces.external_api_interface import IExternalAPIService
from server.schemas.news import NewsArticleCreate
from server.repositories.external_server_repo import ExternalServerRepository
from server.services.category_classifier import CategoryClassifier
from loguru import logger


class NewsAPIService(IExternalAPIService):

    def __init__(self, api_config: Dict[str, Any]):
        self.api_config = api_config
        self.external_api_repo = ExternalServerRepository()
        self.news_repo = NewsRepository()
        self.category_repo = CategoryRepository()
        self.classifier = CategoryClassifier()


    def get_api_name(self) -> str:
        return "NewsAPI"

    def fetch_news(self, api_config: Dict[str, Any]):
        try:
            url = api_config.get("url", "")
            api_key = api_config.get("api_key", "")
            full_url = f"{url}{api_key}"

            logger.info(f"Fetching news from NewsAPI: {url}")
            response = requests.get(full_url)

            if response.status_code == 200:
                server_id = api_config.get("server_id")
                if server_id:
                    self.external_api_repo.update_last_accessed(server_id)

                return response.json()
            else:
                logger.error(f"NewsAPI request failed with status code: {response.status_code}")
                return None

        except requests.RequestException as e:
            logger.error(f"Error fetching news from NewsAPI: {e}")
            return None

    def orchestrate_store_articles(self, articles_data, server_id):
        parsed_articles = self.parse_articles(articles_data, server_id)
        result = self.store_articles(parsed_articles)
        logger.info(result.get('message'))

    def parse_articles(self, data: Dict[str, Any], server_id: int) -> List[NewsArticleCreate]:
        articles = data.get("articles", [])
        parsed_articles = []

        for article in articles:
            source = article.get("source", {}).get("name", "")

            news_article = NewsArticleCreate(
                title=article.get("title", ""),
                server_id=server_id,
                description=article.get("description", ""),
                content=article.get("content", ""),
                source=source,
                url=article.get("url", ""),
                published_at=article.get("publishedAt", "")
            )
            parsed_articles.append(news_article)

        logger.info(f"Parsed {len(parsed_articles)} articles from NewsAPI")
        return parsed_articles

    def store_articles(self, articles):
        for article in articles:
            article_id = self.news_repo.save(article)
            self.classify_article(article, article_id)

        return {
            "message": f"{len(articles)} articles stored from NewsAPI"
        }

    def classify_article(self,article:NewsArticleCreate,article_id):
        title = article.title
        description = article.description
        content = article.content

        category_name = self.classifier.classify(title, description, content)

        category = self.category_repo.get_by_name(category_name)
        category_id = category["category_id"] if category else None
        if article_id and category_id:
            self.store_article_category(article_id, category_id, category_name)

    def store_article_category(self, article_id, category_id, category_name):
        self.category_repo.insert_article_category(category_id, article_id)
        logger.info(f"Mapped Article {article_id} to Category '{category_name}'")