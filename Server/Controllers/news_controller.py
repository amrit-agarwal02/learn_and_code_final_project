from Server.Services.news_service import NewsService
from Server.Services.report_service import ReportService

class NewsController:
    def __init__(self):
        self.news_service = NewsService()
        self.report_service = ReportService()

    def fetch_news(self):
        return self.news_service.sync_news_from_api()

    def fetch_today_news(self, user_id):
        return self.news_service.today_news(user_id)

    def fetch_news_by_date_range(self, user_id, start_date, end_date, category_name):
        return self.news_service.get_news_by_date_range(user_id, start_date,end_date, category_name)

    def fetch_news_by_keyword(self, user_id, keyword):
        return self.news_service.get_news_by_keyword(user_id, keyword)

    def save_news_article_for_user(self, user_id, article_id):
        return self.news_service.save_news_article_for_user(user_id, article_id)

    def get_saved_articles_for_user(self, user_id):
        return self.news_service.get_saved_articles_for_user(user_id)

    def delete_saved_articles_for_user(self, user_id, article_id):
        return self.news_service.delete_saved_articles_for_user(user_id, article_id)

    def report_article(self, article_id, user_id, reason):
        return self.report_service.report_article(article_id, user_id, reason)

    def get_reported_articles(self):
        return self.report_service.get_reported_articles()

    def hide_article(self, article_id):
        return self.report_service.hide_article(article_id)

    def get_article_by_id(self, user_id:int, article_id: int):
        return self.news_service.get_article_by_id(user_id, article_id)