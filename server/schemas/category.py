from pydantic import BaseModel
from typing import List

class CategoryCreate(BaseModel):
    category_name: str
    keywords: List[str]

class CategoryArticleMapping(BaseModel):
    mapping_id: int
    article_id: int
    category_id: int

class CategoryUpdate(BaseModel):
    category_id: int
    category_name: str
    keywords: List[str]