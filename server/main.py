from fastapi import FastAPI
from server.routes import auth_routes,news_routes,external_server_routes, category_routes, user_routes, article_feedback_routes, blocked_keywords_routes
from server.scheduler.news_sync_scheduler import start_news_sync_scheduler

app = FastAPI(title="News Aggregation API")

app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(news_routes.router, prefix="/api/v1")
app.include_router(external_server_routes.router, prefix="/api/v1")
app.include_router(category_routes.router, prefix="/api/v1")
app.include_router(user_routes.router, prefix="/api/v1")
app.include_router(article_feedback_routes.router, prefix="/api/v1")
app.include_router(blocked_keywords_routes.router, prefix="/api/v1")
start_news_sync_scheduler()

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Aggregation API!"}