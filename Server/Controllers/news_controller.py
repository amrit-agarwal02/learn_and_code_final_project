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

    def fetch_news_by_keyword(self, keyword):
        return self.news_service.get_news_by_keyword(keyword)

    def save_news_article_for_user(self, user_id, article_id):
        return self.news_service.save_news_article_for_user(user_id, article_id)

    def get_saved_articles_for_user(self, user_id):
        return self.news_service.get_saved_articles_for_user(user_id)

    def delete_saved_articles_for_user(self, user_id, article_id):
        return self.news_service.delete_saved_articles_for_user(user_id, article_id)