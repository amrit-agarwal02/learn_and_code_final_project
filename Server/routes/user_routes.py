from fastapi import APIRouter,Depends
from Server.Utils.jwt_handler import get_current_user
from Server.schemas.article import ArticleSave, ArticleDelete
from Server.Controllers.notification_controller import NotificationController
from Server.Utils.jwt_handler import get_current_user
from Server.schemas.notification import NotificationRequest, NotificationSettingUpdate
from Server.Controllers.news_controller import NewsController

router = APIRouter(prefix="/user", tags=["user"])
controller = NotificationController()
news_controller = NewsController()

@router.post("/notification/setting")
def set_notification_config(data: NotificationRequest, user = Depends(get_current_user)):
    category = data.category
    keyword = data.keyword
    return controller.save_user_notification_setting(user["user_id"],category,keyword)

@router.get("/notification/settings")
def get_notification_config(user = Depends(get_current_user)):
    return controller.get_user_notification_setting(user)

@router.put("/notification/settings/{setting_id}")
def update_notification_setting(setting_id: int, notification_setting: NotificationSettingUpdate, user=Depends(get_current_user)):
    return controller.update_notification_setting(user["user_id"], setting_id, notification_setting)

@router.get("/today_news")
def get_today_news(user = Depends(get_current_user)):
    return news_controller.fetch_today_news(user["user_id"])

@router.get("/date_range_news/{start_date}/{end_date}")
def get_today_news_by_date_range(start_date,
                                 end_date, category_name,user = Depends(get_current_user)):
    return news_controller.fetch_news_by_date_range(user["user_id"],start_date, end_date, category_name)

@router.get("/search")
def search_articles(keyword, user = Depends(get_current_user)):
    return news_controller.fetch_news_by_keyword(user["user_id"], keyword)

@router.get("/notifications/view")
def get_notification_for_user(user = Depends(get_current_user)):
    return controller.get_notification_for_user(user["user_id"])

@router.post("/article/save")
def save_news_article_for_user(article_data: ArticleSave,user = Depends(get_current_user)):
    article_id = article_data.article_id
    return news_controller.save_news_article_for_user(user["user_id"], article_id)

@router.get("/saved-articles/view")
def get_saved_articles_for_user(user = Depends(get_current_user)):
    return news_controller.get_saved_articles_for_user(user["user_id"])

@router.delete("/saved-articles/delete")
def delete_saved_articles_for_user(article_data: ArticleDelete,user = Depends(get_current_user)):
    article_id = article_data.article_id
    return news_controller.delete_saved_articles_for_user(user["user_id"], article_id)
