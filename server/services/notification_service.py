from server.repositories.notification_repo import NotificationRepository
from server.repositories.category_repo import CategoryRepository
from server.services.email_service import EmailService

class NotificationService:
    def __init__(self):
        self.notification_repo = NotificationRepository()
        self.category_repo = CategoryRepository()
        self.email_service = EmailService()

    def save_user_notification_setting(self, user_id, category, keyword):
        category_id = self.category_repo.get_id_by_name(category)['category_id']
        return self.notification_repo.save(user_id,category_id,keyword)

    def get_user_notification_setting(self,user):
        return self.notification_repo.get_notification_settings(user)

    def send_unread_notifications(self):
        data = self.notification_repo.get_unread_notifications_grouped_by_user()
        for entry in data:
            self.email_service.send_notification_email(entry['email'], entry['messages'])

    def store_notifications(self):
        return self.notification_repo.store_notifications()

    def get_notification_for_user(self, user_id):
        notifications = self.notification_repo.get_unread_notifications_by_user(user_id)
        self.mark_notifications_as_read(user_id)
        return notifications

    def update_notification_setting(self, user_id, setting_id, notification_setting):
        return self.notification_repo.update_notification_setting(user_id, setting_id, notification_setting)

    def mark_notifications_as_read(self, user_id):
        self.notification_repo.set_notifications_read_by_user(user_id)
