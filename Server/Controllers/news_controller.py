from Server.Services.news_service import NewsService

class NewsController:
    def __init__(self):
        self.news_service = NewsService()

    def fetch_news(self):
        return self.news_service.sync_news_from_api()

    def fetch_today_news(self):
        return self.news_service.today_news()