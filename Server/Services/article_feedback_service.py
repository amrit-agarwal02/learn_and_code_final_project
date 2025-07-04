from Server.Repositories.article_feedback_repo import ArticleFeedbackRepository

class ArticleFeedbackService:
    def __init__(self):
        self.feedback_repo = ArticleFeedbackRepository()

    def like_article(self, user_id: int, article_id: int):
        return self.feedback_repo.like_article_by_user(user_id, article_id)

    def dislike_article(self, user_id: int, article_id: int):
        return self.feedback_repo.dislike_article_by_user(user_id, article_id)
