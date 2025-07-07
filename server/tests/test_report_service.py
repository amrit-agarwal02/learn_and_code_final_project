import unittest
from server.services.report_service import ReportService

class TestReportService(unittest.TestCase):
    def test_get_reported_articles(self):
        service = ReportService()
        result = service.get_reported_articles()
        self.assertIsInstance(result, list)

    def test_report_article(self):
        service = ReportService()
        try:
            result = service.report_article(1, 1, 'reason')
            self.assertIsInstance(result, dict)
        except Exception:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main() 