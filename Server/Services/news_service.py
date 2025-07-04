import requests
from Server.Repositories.news_repo import NewsRepository
from Server.Repositories.category_repo import CategoryRepository
from Server.Repositories.personalization_repo import PersonalizationRepo
from Server.Services.blocked_keywords_service import BlockedKeywordsService
from Server.schemas.news import NewsArticleCreate
from Server.Repositories.external_server_repo import ExternalServerRepository
from Server.config.constants import API_URL
from Server.Services.category_classifier import CategoryClassifier
from Server.Services.category_service import CategoryService
from Server.Services.notification_service import NotificationService
from loguru import logger
from Server.config.constants import REPORT_THRESHOLD


class NewsService:
    def __init__(self):
        self.news_repo = NewsRepository()
        self.external_api_repo = ExternalServerRepository()
        self.category_repo = CategoryRepository()
        self.classifier = CategoryClassifier()
        self.notification_service = NotificationService()
        self.blocked_keywords_service = BlockedKeywordsService()
        self.personalization_repo = PersonalizationRepo()

    def get_active_api(self):
        apis = self.external_api_repo.get_api_status()
        return next((api for api in apis if api["is_active"]==1), None)

    def classify_article(self,article:NewsArticleCreate,article_id):
        title = article.title
        description = article.description
        content = article.content

        category_name = self.classifier.classify(title, description, content)

        category = self.category_repo.get_by_name(category_name)
        category_id = category["category_id"] if category else None

        if article_id and category_id:
            self.category_repo.insert_article_category(category_id,article_id)
            logger.info(f"Mapped Article {article_id} to Category '{category_name}'")

    def fetch_news(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
        return None

    def parse_articles_newsapi(self, data, server_id):
        articles = data.get("articles", [])
        parsed_articles = []
        for article in articles:
            source = article.get("source", {}).get("name")
            news = NewsArticleCreate(
                title=article.get("title"),
                server_id= server_id,
                description=article.get("description"),
                content=article.get("content"),
                source=source,
                url=article.get("url"),
                published_at=article.get("publishedAt")
            )
            parsed_articles.append(news)
        return parsed_articles

    def store_articles_thenewsapi(self, data, server_id):
        articles = data.get("data", [])
        parsed_articles = []
        for article in articles:
            source = article.get("source")
            title = article.get("title")
            server_id = server_id
            description = article.get("description")
            content = article.get("content")
            source = source
            url = article.get("url")
            published_at = article.get("published_at")
            categories = article.get("categories",[])


            news = NewsArticleCreate(
                title=article.get("title"),
                server_id=server_id,
                description=article.get("description"),
                content=article.get("content"),
                source=source,
                url=article.get("url"),
                published_at=article.get("published_at")
            )
            parsed_articles.append(news)
            article_id = self.news_repo.save(news)
            for category_name in categories:
                if category_name:
                    category = self.category_repo.get_by_name(category_name)
                    if category:
                        category_id = category.get('category_id')
                        self.category_repo.insert_article_category(category_id, article_id)
                    else:
                        category_name= CategoryClassifier.DEFAULT_CATEGORY
                        category_id = self.category_repo.get_id_by_name(category_name).get('category_id')
                        self.category_repo.insert_article_category(category_id, article_id)

        return parsed_articles

    def store_articles(self, articles, active_api):
        for article in articles:
            article_id = self.news_repo.save(article)
            self.classify_article(article, article_id)

        return{
            "message": f"{len(articles)} articles stored from {active_api['server_name']}",
            "source": active_api["server_name"]
        }

    def sync_news_from_api(self):
        logger.info("Starting sync from external API...")
        active_api = self.get_active_api()

        if not active_api:
            return {"error": "No active external APIs available"}

        active_api_server_name = active_api["server_name"]
        active_api_url = API_URL.get(active_api_server_name)
        active_api_server_id = active_api["server_id"]

        logger.info(f"Fetching news from {active_api_url}")

        data = self.fetch_news(active_api_url+active_api["api_key"])

        if not data:
            return {"error": f"Failed to fetch news from {active_api['name']}"}

        if "thenewsapi" in active_api_url.lower():
            articles = self.store_articles_thenewsapi(data, active_api_server_id)
            logger.info(f"Fetched and stored {len(articles)} articles from {active_api['server_name']}")
            logger.success("News sync completed.")
            return {
                "message": f"{len(articles)} articles stored from {active_api['server_name']}",
                "source": active_api["server_name"]
            }
        else:
            articles = self.parse_articles_newsapi(data, active_api_server_id)
            result = self.store_articles(articles, active_api)
            notifications_stored = self.notification_service.store_notifications()
            print("Notifications Stored :", notifications_stored)
            logger.info(f"Notifications Stored result: {notifications_stored}")
            self.notification_service.send_unread_notifications()
            return result

    def today_news(self, user_id:int):
        today_articles = self.news_repo.get_today_news()
        today_articles = self.filter_blocked_articles(today_articles)
        return self.personalize_articles(user_id, today_articles)

    def get_news_by_date_range(self,user_id, start_date, end_date, category_name):
        category_id_response = self.category_repo.get_id_by_name(category_name)
        category_id = int(category_id_response.get('category_id'))
        news_articles = self.news_repo.get_news_by_date_range(start_date,end_date,category_id)
        news_articles = self.filter_blocked_articles(news_articles)
        return self.personalize_articles(user_id, news_articles)

    def get_news_by_keyword(self, user_id, keyword):
        articles = self.news_repo.get_news_by_keyword(keyword)
        articles = self.filter_blocked_articles(articles)
        return self.personalize_articles(user_id, news_articles)

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
            print("\n"*10,category)
            score += category_counts.get(category, 0) * 3  # weight as you like
            personalized.append((score, article))
        personalized.sort(reverse=True, key=lambda x: x[0])
        return [a for score, a in personalized[:20]]