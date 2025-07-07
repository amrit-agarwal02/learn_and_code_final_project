import unittest
from server.services.news_service import NewsService

class TestNewsService(unittest.TestCase):
    def test_get_all_apis_type(self):
        service = NewsService()
        result = service.get_all_apis()
        self.assertIsInstance(result, list)

    def test_today_news_type(self):
        service = NewsService()
        result = service.today_news(1)
        self.assertIsInstance(result, list)

if __name__ == '__main__':
    unittest.main() 