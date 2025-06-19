from pydantic import BaseModel, EmailStr

class CategoryCreate(BaseModel):
    category_id: int
    category_name: str

class CategoryArticleMapping(BaseModel):
    mapping_id: int
    article_id: int
    category_id: int

