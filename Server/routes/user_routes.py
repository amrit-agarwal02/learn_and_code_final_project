from fastapi import APIRouter,Depends
from unicodedata import category

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

