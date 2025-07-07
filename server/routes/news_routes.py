from fastapi import APIRouter, Depends, HTTPException
from server.controllers.news_controller import NewsController
from server.utils.jwt_handler import get_current_user, admin_required
from server.controllers.category_controller import CategoryController
from typing import Optional
from server.Exceptions.exceptions import ArticleNotFoundException
from server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED, HTTP_NOT_FOUND

router = APIRouter(prefix="/news", tags=["news"])
news_controller = NewsController()
category_controller = CategoryController()

@router.get("/sync")
def sync_news():
    try:
        return news_controller.fetch_news()
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/articles/{article_id}/report")
def report_article(article_id: int, user = Depends(get_current_user), reason: Optional[str] = None):
    try:
        return news_controller.report_article(article_id, user["user_id"], reason)
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/admin/reported-articles")
def get_reported_articles(user= Depends(admin_required)):
    try:
        return news_controller.get_reported_articles()
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/admin/hide/article")
def hide_article(article_id: int,user=Depends(admin_required)):
    try:
        return news_controller.hide_article(article_id)
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/article/view")
def get_article_by_id(article_id: int, user=Depends(get_current_user)):
    try:
        article = news_controller.get_article_by_id(user["user_id"], article_id)
        if not article:
            raise ArticleNotFoundException("Article not found")
        return article
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")