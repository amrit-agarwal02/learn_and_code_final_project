from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class NewsArticleCreate(BaseModel):
    server_id: int
    title: str
    description: Optional[str]
    content: Optional[str]
    source: Optional[str]
    url: str
    published_at: Optional[datetime]

class NewsArticle(BaseModel):
    article_id: int
    server_id: int
    title: str
    description: Optional[str]
    content: Optional[str]
    source: Optional[str]
    url: str
    published_at: Optional[datetime]

class SearchArticleRequest(BaseModel):
    keyword: str
    start_date: str
    end_date: str