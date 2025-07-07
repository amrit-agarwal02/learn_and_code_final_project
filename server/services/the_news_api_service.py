import requests
from typing import List, Dict, Any
from server.services.interfaces.external_api_interface import IExternalAPIService
from server.schemas.news import NewsArticleCreate
from server.repositories.external_server_repo import ExternalServerRepository
from server.repositories.news_repo import NewsRepository
from server.repositories.category_repo import CategoryRepository
from server.services.category_classifier import CategoryClassifier
from loguru import logger


class TheNewsAPIService(IExternalAPIService):

    def __init__(self, api_config: Dict[str, Any]):
        self.api_config = api_config
        self.external_api_repo = ExternalServerRepository()
        self.news_repo = NewsRepository()
        self.category_repo = CategoryRepository()
        self.classifier = CategoryClassifier()

    def get_api_name(self) -> str:
        return "TheNewsAPI"

    def fetch_news(self, api_config: Dict[str, Any]) -> Dict[str, Any]:
        try:
            url = api_config.get("url", "")
            api_key = api_config.get("api_key", "")
            full_url = f"{url}{api_key}"

            logger.info(f"Fetching news from TheNewsAPI: {url}")
            response = requests.get(full_url)

            if response.status_code == 200:
                server_id = api_config.get("server_id")
                if server_id:
                    self.external_api_repo.update_last_accessed(server_id)

                return response.json()
            else:
                logger.error(f"TheNewsAPI request failed with status code: {response.status_code}")
                return None

        except requests.RequestException as e:
            logger.error(f"Error fetching news from TheNewsAPI: {e}")
            return None

    def orchestrate_store_articles(self, articles_data, server_id):
        self.parse_articles(articles_data, server_id)

    def parse_articles(self, data: Dict[str, Any], server_id: int) -> List[NewsArticleCreate]:
        articles = data.get("data", [])
        parsed_articles = []
        for article in articles:
            source = article.get("source", "")

            news_article = NewsArticleCreate(
                title=article.get("title", ""),
                server_id=server_id,
                description=article.get("description", ""),
                content=article.get("content", ""),
                source=source,
                url=article.get("url", ""),
                published_at=article.get("published_at", "")
            )
            parsed_articles.append(news_article)


            article_id = self.store_articles(news_article)

            self.store_article_category(article, article_id)

        logger.info(f"Parsed and stored {len(parsed_articles)} articles from TheNewsAPI")
        return parsed_articles

    def store_articles(self, news_article):
        article_id = self.news_repo.save(news_article)
        return article_id

    def store_article_category(self, article, article_id):
        categories = article.get("categories", [])
        for category_name in categories:
            if category_name:
                category = self.category_repo.get_by_name(category_name)
                if category:
                    category_id = category.get('category_id')
                    self.category_repo.insert_article_category(category_id, article_id)
                    logger.info(f"Mapped Article {article_id} to Category '{category_name}'")
                else:
                    default_category = CategoryClassifier.DEFAULT_CATEGORY
                    category_id_response = self.category_repo.get_id_by_name(default_category)
                    if category_id_response:
                        category_id = category_id_response.get('category_id')
                        self.category_repo.insert_article_category(category_id, article_id)
                        logger.info(f"Mapped Article {article_id} to Category '{default_category}'")



