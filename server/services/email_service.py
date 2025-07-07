from server.utils.email_utils import send_email
from server.services.interfaces.email_interface import IEmailService


class EmailService(IEmailService):
    def send_notification_email(self, to_email: str, message: str):
        subject = "Notification From News Aggregation App"
        body = f"Hello,\n\nYou have new notifications:\n\n{message}"
        send_email(to_email, subject, body)