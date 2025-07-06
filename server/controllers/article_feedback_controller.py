from fastapi import HTTPException
from server.services.article_feedback_service import ArticleFeedbackService
from server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR

class ArticleFeedbackController:
    def __init__(self):
        self.feedback_service = ArticleFeedbackService()

    def like_article(self, user_id: int, article_id: int):
        try:
            return self.feedback_service.like_article(user_id, article_id)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def dislike_article(self, user_id: int, article_id: int):
        try:
            return self.feedback_service.dislike_article(user_id, article_id)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))
