from fastapi import APIRouter,Depends
from Server.Utils.jwt_handler import get_current_user

from Server.Controllers.notification_controller import NotificationController
from Server.Utils.jwt_handler import get_current_user
from Server.schemas.notification import NotificationRequest

router = APIRouter(prefix="/user", tags=["user"])
controller = NotificationController()


@router.post("/notification/setting")
def set_notification_config(data: NotificationRequest, user = Depends(get_current_user)):
    category = data.category
    keyword = data.keyword
    return controller.save_user_notification_setting(user["user_id"],category,keyword)

@router.get("/notification/settings")
def get_notification_config(user = Depends(get_current_user)):
    return controller.get_user_notification_setting(user)

@router.get("/today_news")
def get_today_news(user = Depends(get_current_user)):
    return controller.fetch_today_news()

@router.get("/date_range_news")
def get_today_news_by_date_range(start_date,
                                 end_date, category_name,user = Depends(get_current_user)):
    return controller.fetch_news_by_date_range(start_date, end_date, category_name)

@router.get("/search")
def search_articles(keyword, user = Depends(get_current_user)):
    return controller.fetch_news_by_keyword(keyword)

