from fastapi import APIRouter,Depends, HTTPException
from server.utils.jwt_handler import get_current_user
from server.schemas.article import ArticleSave, ArticleDelete
from server.controllers.notification_controller import NotificationController
from server.utils.jwt_handler import get_current_user
from server.schemas.notification import NotificationRequest, NotificationSettingUpdate
from server.controllers.news_controller import NewsController
from server.schemas.news import SearchArticleRequest
from server.Exceptions.exceptions import ArticleNotFoundException
from server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_NOT_FOUND


router = APIRouter(prefix="/user", tags=["user"])
controller = NotificationController()
news_controller = NewsController()

@router.post("/notification/setting")
def set_notification_config(notification_setting_data: NotificationRequest, user = Depends(get_current_user)):
    try:
        return controller.save_user_notification_setting(user["user_id"], notification_setting_data)
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/notification/settings")
def get_notification_config(user = Depends(get_current_user)):
    try:
        return controller.get_user_notification_setting(user)
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/notification/settings/{setting_id}")
def update_notification_setting(setting_id: int, notification_setting: NotificationSettingUpdate, user=Depends(get_current_user)):
    try:
        return controller.update_notification_setting(user["user_id"], setting_id, notification_setting)
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/today_news")
def get_today_news(user = Depends(get_current_user)):
    try:
        return news_controller.fetch_today_news(user["user_id"])
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/date_range_news/{start_date}/{end_date}")
def get_news_by_date_range(start_date,
                                 end_date, category_name,user = Depends(get_current_user)):
    try:
        return news_controller.fetch_news_by_date_range(user["user_id"], start_date, end_date, category_name)
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/search")
def search_articles(search_request: SearchArticleRequest = Depends(), user = Depends(get_current_user)):
    try:
        return news_controller.fetch_news_by_keyword(user["user_id"], search_request)
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/notifications/view")
def get_notification_for_user(user = Depends(get_current_user)):
    try:
        return controller.get_notification_for_user(user["user_id"])
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/article/save")
def save_news_article_for_user(article_data: ArticleSave,user = Depends(get_current_user)):
    try:
        article_id = article_data.article_id
        return news_controller.save_news_article_for_user(user["user_id"], article_id)
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/saved-articles/view")
def get_saved_articles_for_user(user = Depends(get_current_user)):
    try:
        return news_controller.get_saved_articles_for_user(user["user_id"])
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/saved-articles/delete")
def delete_saved_articles_for_user(article_data: ArticleDelete,user = Depends(get_current_user)):
    try:
        article_id = article_data.article_id
        return news_controller.delete_saved_articles_for_user(user["user_id"], article_id)
    except ArticleNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")
