from fastapi import APIRouter, Depends, HTTPException
from server.controllers.article_feedback_controller import ArticleFeedbackController
from server.utils.jwt_handler import get_current_user
from server.Exceptions.exceptions import ArticleNotFoundException
from server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_NOT_FOUND

router = APIRouter(prefix="/feedback", tags=["feedback"])
controller = ArticleFeedbackController()

@router.post("/like/{article_id}")
def like_article(article_id: int, user=Depends(get_current_user)):
    try:
        return controller.like_article(user_id=user["user_id"], article_id=article_id)
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/dislike/{article_id}")
def dislike_article(article_id: int, user=Depends(get_current_user)):
    try:
        return controller.dislike_article(user_id=user["user_id"], article_id=article_id)
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")
