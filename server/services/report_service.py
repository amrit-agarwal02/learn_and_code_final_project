from server.repositories.news_repo import NewsRepository
from server.config.constants import REPORT_THRESHOLD
from server.services.email_service import EmailService
from server.services.interfaces.report_interface import IReportService


class ReportService(IReportService):
    def __init__(self):
        self.email_service = EmailService()
        self.news_repo = NewsRepository()

    def report_article(self, article_id, user_id, reason):
        self.news_repo.insert_report(article_id, user_id, reason)

        report_count = self.news_repo.get_report_count(article_id)
        if report_count >= REPORT_THRESHOLD:
            self.news_repo.hide_article(article_id)
        if report_count<REPORT_THRESHOLD:
            self.email_service.send_notification_email(
                to_email="02amritagarwal@gmail.com",
                message=f"Article ID {article_id} was reported by User ID {user_id}.\nReason: {reason or 'No reason provided'}.\nTotal reports: {report_count}"
            )
        return {"message": "Report submitted successfully."}

    def get_reported_articles(self):
        return self.news_repo.get_reported_articles()

    def hide_article(self, article_id):
        return self.news_repo.hide_article(article_id)
