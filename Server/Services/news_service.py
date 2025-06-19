import requests
from Server.Repositories.news_repo import NewsRepository
from Server.Repositories.category_repo import CategoryRepository
from Server.schemas.news import NewsArticleCreate
from Server.Repositories.external_api_repo import ExternalAPIRepository
from Server.config.constants import API_URL
from loguru import logger

class NewsService:
    def __init__(self):
        self.news_repo = NewsRepository()
        self.external_api_repo = ExternalAPIRepository()
        self.category_repo = CategoryRepository()

    def get_active_api(self):
        apis = self.external_api_repo.get_api_status()
        return next((api for api in apis if api["is_active"]==1), None)

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

    def parse_articles_thenewsapi(self, data, server_id):
        articles = data.get("data", [])
        print(articles)
        parsed_articles = []
        for article in articles:
            source = article.get("source")
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
        return parsed_articles

    def store_categories(self,last_articles_stored):

        recent_stored_articles = self.news_repo.get_recent_news(last_articles_stored)

        for article in recent_stored_articles:
            self.category_repo.get_by_name(article)


        pass

    def store_articles(self, articles, active_api):
        for article in articles:
            self.news_repo.save(article)

        articles_inserted = len(articles)
        self.store_categories(articles_inserted)

        return{
            "message": f"{len(articles)} articles stored from {active_api['server_name']}",
            "source": active_api["server_name"]
        }

    def sync_news_from_api(self):
        logger.info("Starting sync from external API...")
        active_api = self.get_active_api()

        if not active_api:
            return {"error": "No active external APIs available"}

        active_api_url = API_URL.get(active_api["server_name"])
        active_api_server_id = active_api["server_id"]

        logger.info(f"Fetching news from {active_api_url}...")

        data = self.fetch_news(active_api_url+active_api["api_key"])

        if not data:
            return {"error": f"Failed to fetch news from {active_api['name']}"}

        if "thenewsapi" in active_api_url.lower():
            articles = self.parse_articles_thenewsapi(data,active_api_server_id)
        else:
            articles = self.parse_articles_newsapi(data,active_api_server_id)

        logger.info(f"Fetched {len(articles)} articles.")
        print(articles,active_api)
        result = self.store_articles(articles, active_api)
        logger.success("News sync completed.")
        return result



obj = NewsService()
obj.sync_news_from_api()