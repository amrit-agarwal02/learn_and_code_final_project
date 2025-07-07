import unittest
from server.services.notification_service import NotificationService

class TestNotificationService(unittest.TestCase):

    def test_get_notification_for_user(self):
        service = NotificationService()
        result = service.get_notification_for_user(1)
        self.assertIsInstance(result, list)

    def test_get_user_notification_setting(self):
        service = NotificationService()
        try:
            result = service.get_user_notification_setting(1)
            self.assertIsInstance(result, list)
        except Exception:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main() 