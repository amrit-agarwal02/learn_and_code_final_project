from fastapi import FastAPI
from Server.routes import auth_routes,news_routes,external_server_routes
from Server.Scheduler.news_sync_scheduler import start_news_sync_scheduler

app = FastAPI(title="News Aggregation API")

app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(news_routes.router, prefix="/api/v1")
app.include_router(external_server_routes.router, prefix="/api/v1")

start_news_sync_scheduler()

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Aggregation API!"}