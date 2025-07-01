from apscheduler.schedulers.background import BackgroundScheduler
from Server.Controllers.news_controller import NewsController
from Server.Controllers.notification_controller import NotificationController
from loguru import logger

def sync_news_job():
    logger.info("Scheduled news sync started...")
    controller = NewsController()
    result = controller.fetch_news()
    print("Scheduled News Sync:", result)
    logger.info(f"Scheduled sync result: {result}")

def generate_notifications_job():
    notification_controller = NotificationController()
    result = notification_controller.store_notifications()
    print("Notifications Stored :", result)
    logger.info(f"Notifications Stored result: {result}")

def start_news_sync_scheduler():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(sync_news_job, 'interval', hours=4)
    # scheduler.add_job(generate_notifications_job, 'interval', hours=4, minutes=5)
    scheduler.add_job(sync_news_job, 'interval', minutes=4)
    scheduler.add_job(generate_notifications_job, 'interval', minutes=5)
    scheduler.start()
    print("News sync scheduler started: will run every 4 hours.")
