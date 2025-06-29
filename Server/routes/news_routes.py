from fastapi import APIRouter
from Server.Controllers.news_controller import NewsController

router = APIRouter(prefix="/news", tags=["news"])
controller = NewsController()

@router.get("/sync")
def sync_news():
    return controller.fetch_news()

@router.get("/today_news")
def get_today_news():
    return controller.fetch_today_news()

@router.get("/date_range_news")
def get_today_news_by_date_range(start_date,
                                 end_date, category_name):
    return controller.fetch_news_by_date_range(start_date, end_date, category_name)

@router.get("/search")
def search_articles(keyword):
    return controller.fetch_news_by_keyword(keyword)