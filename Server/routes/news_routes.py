from fastapi import APIRouter, Depends
from Server.Controllers.news_controller import NewsController
from Server.Utils.jwt_handler import get_current_user

router = APIRouter(prefix="/news", tags=["news"])
controller = NewsController()

@router.get("/sync")
def sync_news():
    return controller.fetch_news()