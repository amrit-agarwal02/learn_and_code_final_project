from fastapi import APIRouter, Depends, HTTPException
from server.controllers.news_controller import NewsController
from server.utils.jwt_handler import get_current_user, admin_required
from server.controllers.category_controller import CategoryController
from typing import Optional

router = APIRouter(prefix="/news", tags=["news"])
news_controller = NewsController()
category_controller = CategoryController()

@router.get("/sync")
def sync_news():
    return news_controller.fetch_news()

@router.put("/admin/category/{category_id}/hide")
def hide_category(category_id: int,user=Depends(admin_required)):
    return category_controller.hide_category(category_id)

@router.post("/articles/{article_id}/report")
def report_article(article_id: int, user = Depends(get_current_user), reason: Optional[str] = None):
    return news_controller.report_article(article_id, user["user_id"], reason)

@router.get("/admin/reported-articles")
def get_reported_articles(user= Depends(admin_required)):
    return news_controller.get_reported_articles()

@router.put("/admin/hide/article/{article_id}")
def hide_article(article_id: int,user=Depends(admin_required)):
    return news_controller.hide_article(article_id)

@router.get("/article/view")
def get_article_by_id(article_id: int, user=Depends(get_current_user)):
    article = news_controller.get_article_by_id(user["user_id"],article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article