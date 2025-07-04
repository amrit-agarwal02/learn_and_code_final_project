from fastapi import APIRouter, Depends
from Server.Controllers.article_feedback_controller import ArticleFeedbackController
from Server.Utils.jwt_handler import get_current_user

router = APIRouter(prefix="/feedback", tags=["feedback"])
controller = ArticleFeedbackController()

@router.post("/like/{article_id}")
def like_article(article_id: int, user=Depends(get_current_user)):
    return controller.like_article(user_id=user["user_id"], article_id=article_id)

@router.post("/dislike/{article_id}")
def dislike_article(article_id: int, user=Depends(get_current_user)):
    return controller.dislike_article(user_id=user["user_id"], article_id=article_id)
