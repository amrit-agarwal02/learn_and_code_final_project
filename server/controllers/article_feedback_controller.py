from server.services.article_feedback_service import ArticleFeedbackService


class ArticleFeedbackController:
    def __init__(self):
        self.feedback_service = ArticleFeedbackService()

    def like_article(self, user_id: int, article_id: int):
        return self.feedback_service.like_article(user_id, article_id)

    def dislike_article(self, user_id: int, article_id: int):
        return self.feedback_service.dislike_article(user_id, article_id)
