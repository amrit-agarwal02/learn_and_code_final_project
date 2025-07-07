from fastapi import HTTPException

from server.schemas.notification import NotificationRequest
from server.services.notification_service import NotificationService
from server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR

class NotificationController:
    def __init__(self):
        self.notification_service = NotificationService()

    def get_user_notification_setting(self, user):
        return self.notification_service.get_user_notification_setting(user)

    def save_user_notification_setting(self, user_id, notification_setting_data: NotificationRequest):
        return self.notification_service.save_user_notification_setting(user_id, notification_setting_data)

    def store_notifications(self):
        return self.notification_service.store_notifications()

    def get_notification_for_user(self, user_id):
        return self.notification_service.get_notification_for_user(user_id)

    def update_notification_setting(self, user_id, setting_id, notification_setting):
        return self.notification_service.update_notification_setting(user_id, setting_id, notification_setting)

