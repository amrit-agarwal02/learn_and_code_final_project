from pydantic import BaseModel

class ArticleBase(BaseModel):
    title: str
    content: str

class ArticleCreate(ArticleBase):
    pass

class ArticleRead(ArticleBase):
    id: int
    author_id: int


class ArticleSave(BaseModel):
    article_id: int

class ArticleDelete(BaseModel):
    article_id: int