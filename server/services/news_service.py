import requests
from server.repositories.news_repo import NewsRepository
from server.repositories.category_repo import CategoryRepository
from server.repositories.personalization_repo import PersonalizationRepo
from server.services.blocked_keywords_service import BlockedKeywordsService
from server.schemas.news import NewsArticleCreate
from server.repositories.external_server_repo import ExternalServerRepository
from server.config.constants import API_URL
from server.services.category_classifier import CategoryClassifier
from server.services.category_service import CategoryService
from server.services.notification_service import NotificationService
from server.utils.logger import logger
from server.services.interfaces.news_interface import INewsService
from server.services.external_api_factory import ExternalAPIFactory
from typing import Dict, List, Any, Optional
from server.services.interfaces.external_api_interface import IExternalAPIService

class NewsService(INewsService):
    def __init__(self):
        self.news_repo = NewsRepository()
        self.external_api_repo = ExternalServerRepository()
        self.category_repo = CategoryRepository()
        self.classifier = CategoryClassifier()
        self.notification_service = NotificationService()
        self.blocked_keywords_service = BlockedKeywordsService()
        self.personalization_repo = PersonalizationRepo()

    def get_all_apis(self):
        return self.external_api_repo.fetch_all_external_servers()

    def get_news_from_first_available_api(self, apis):
        if not apis:
            logger.error("No external APIs configured")
            return None, None, None
        for api in apis:
            result = self._attempt_fetch_from_api(api)
            if result:
                return result
        logger.error("All APIs failed")
        return None, None, None

    def _attempt_fetch_from_api(self, api):
        server_id = api["server_id"]
        server_name = api["server_name"]
        api_url = API_URL.get(server_name)
        if not api_url:
            logger.warning(f"No URL configured for API: {server_name}")
            return None
        api_config = self._create_api_config(api, api_url)
        logger.info(f"Attempting API: {server_name}")

        try:
            external_api_service = self._create_api_service(server_name, api_config)
            fetched_data = self._fetch_api_data(external_api_service, api_config)
            if fetched_data:
                self._handle_successful_api(server_id, server_name)
                return api, fetched_data, external_api_service
            else:
                self._handle_failed_api(server_id, server_name)
                return None
        except Exception as e:
            logger.error(f"Error testing API {server_name}: {e}")
            self._handle_failed_api(server_id, server_name)
            return None

    def _create_api_config(self, api: Dict[str, Any], api_url: str) -> Dict[str, Any]:
        return {
            "url": api_url,
            "api_key": api["api_key"],
            "server_id": api["server_id"],
            "server_name": api["server_name"]
        }

    def _create_api_service(self, server_name: str, api_config):
        return ExternalAPIFactory.create_api_service(server_name, api_config)

    def _fetch_api_data(self, api_service: IExternalAPIService, api_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return api_service.fetch_news(api_config)

    def _handle_successful_api(self, server_id: int, server_name: str) -> None:
        logger.info(f"API {server_name} is working")
        self.external_api_repo.update_api_status(server_id, True)
        self.external_api_repo.update_last_accessed(server_id)

    def _handle_failed_api(self, server_id: int, server_name: str) -> None:
        logger.warning(f"API {server_name} failed - marking as inactive")
        self.external_api_repo.update_api_status(server_id, False)

    def sync_news_from_api(self):
        logger.info("Starting sync from external API")
        working_api, fetched_data, external_api_service = self.get_news_from_first_available_api(self.get_all_apis())

        if not working_api or not fetched_data or not external_api_service:
            return {"error": "All external APIs are unavailable"}

        working_api_server_id = working_api["server_id"]
        working_api_server_name = working_api["server_name"]

        logger.info(f"Processing news from {working_api_server_name}")

        try:
            external_api_service.orchestrate_store_articles(fetched_data, working_api_server_id)
            notifications_stored = self.notification_service.store_notifications()
            logger.info(f"Notifications Stored result: {notifications_stored}")
            self.notification_service.send_unread_notifications()

        except Exception as e:
            logger.error(f"Error during news sync: {e}")
            return {"error": f"Failed to sync news: {str(e)}"}

    def today_news(self, user_id:int):
        today_articles = self.news_repo.get_today_news()
        today_articles = self.filter_blocked_articles(today_articles)
        return self.personalize_articles(user_id, today_articles)

    def get_news_by_date_range(self,user_id, start_date, end_date, category_name):
        if category_name.lower() != "all":
            category_id_response = self.category_repo.get_id_by_name(category_name)
            category_id = int(category_id_response.get('category_id'))
        else:
            category_id = None
        news_articles = self.news_repo.get_news_by_date_range(start_date,end_date,category_id)
        news_articles = self.filter_blocked_articles(news_articles)
        return self.personalize_articles(user_id, news_articles)

    def get_news_by_keyword(self, user_id, search_request):
        articles = self.news_repo.get_news_by_keyword(search_request)
        articles = self.filter_blocked_articles(articles)
        return self.personalize_articles(user_id, articles)

    def save_news_article_for_user(self, user_id, article_id):
        return self.news_repo.save_news_article_for_user(user_id, article_id)

    def get_saved_articles_for_user(self, user_id):
        return self.news_repo.get_saved_articles_for_user(user_id)

    def delete_saved_articles_for_user(self, user_id, article_id):
        return self.news_repo.delete_saved_articles_for_user(user_id, article_id)

    def get_article_by_id(self,user_id ,article_id: int):
        article = self.news_repo.get_article_by_id(article_id)
        if article:
            self.news_repo.mark_article_as_read(user_id, article_id)
        return article

    def mark_article_as_read(self, user_id: int, article_id: int):
        return self.news_repo.mark_article_as_read(user_id, article_id)

    def filter_blocked_articles(self, articles):
        blocked_keywords = self.blocked_keywords_service.get_all_blocked_keywords()
        filtered = []
        for article in articles:
            title = (article.get('title') or '').lower()
            content = (article.get('content') or '').lower()
            if any(kw.lower() in title or kw.lower() in content for kw in blocked_keywords):
                continue
            filtered.append(article)
        return filtered

    def personalize_articles(self, user_id, articles):
        category_counts = self.personalization_repo.get_user_category_counts(user_id)
        personalized = []
        for article in articles:
            score = 0
            category = article.get('category_name')
            score += category_counts.get(category, 0) * 3  # weight as you like
            personalized.append((score, article))
        personalized.sort(reverse=True, key=lambda x: x[0])
        return [a for score, a in personalized[:20]]
