from Server.Services.news_service import NewsService

class NewsController:
    def __init__(self):
        self.news_service = NewsService()

    def fetch_news(self):
        return self.news_service.sync_news_from_api()

    def fetch_today_news(self):
        return self.news_service.today_news()

    def fetch_news_by_date_range(self, start_date, end_date, category_name):
        return self.news_service.get_news_by_date_range(start_date,end_date, category_name)