from fastapi import HTTPException
from Server.Services.notification_service import NotificationService
from Server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR

class NotificationController:
    def __init__(self):
        self.notification_service = NotificationService()

    def get_user_notification_setting(self, user):
        try:
            return self.notification_service.get_user_notification_setting(user)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def save_user_notification_setting(self, user_id, category, keyword):
        try:
            return self.notification_service.save_user_notification_setting(user_id, category, keyword)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def store_notifications(self):
        try:
            return self.notification_service.store_notifications()
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_notification_for_user(self, user_id):
        try:
            return self.notification_service.get_notification_for_user(user_id)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def update_notification_setting(self, user_id, setting_id, notification_setting):
        try:
            return self.notification_service.update_notification_setting(user_id, setting_id, notification_setting)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

