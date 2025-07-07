from pydantic import BaseModel
from typing import List

class CategoryCreate(BaseModel):
    category_name: str
    keywords: List[str]


class CategoryUpdate(BaseModel):
    category_id: int
    category_name: str
    keywords: List[str]