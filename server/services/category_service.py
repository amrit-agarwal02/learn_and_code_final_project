from server.repositories.category_repo import CategoryRepository
from typing import List
from server.schemas.news import NewsArticleCreate
from server.schemas.category import CategoryCreate
from loguru import logger

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def get_all_categories(self) -> List[dict]:
        return self.repo.get_all()

    def get_category_by_id(self, category_id: int) -> dict:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category with ID {category_id} not found")
        return category

    def create_category(self, category: CategoryCreate) -> dict:
        existing = self.repo.get_by_name(category.category_name)
        if existing:
            raise ValueError(f"Category '{category.category_name}' already exists")
        payload = self.repo.create(category.category_name)
        self.repo.insert_category_keywords(category.category_name, category.keywords)
        return payload

    def update_category(self, category_id: int, name: str = None, description: str = None) -> dict:
        existing = self.repo.get_by_id(category_id)
        if not existing:
            raise ValueError(f"Category with ID {category_id} not found")

        if name and name != existing['name']:
            name_conflict = self.repo.get_by_name(name)
            if name_conflict:
                raise ValueError(f"Category '{name}' already exists")

        return self.repo.update(category_id, name, description)

    def delete_category(self, category_id: int):
        existing = self.repo.get_by_id(category_id)
        if not existing:
            raise ValueError(f"Category with ID {category_id} not found")
        return self.repo.delete(category_id)

    # def classify_article(self,article:NewsArticleCreate,article_id):
    #     title = article.title
    #     description = article.description
    #     content = article.content
    #
    #     category_name = self.classifier.classify(title, description, content)
    #
    #     category = self.category_repo.get_by_name(category_name)
    #     category_id = category["category_id"] if category else None
    #
    #     if article_id and category_id:
    #         self.category_repo.insert_article_category(category_id,article_id)
    #         logger.info(f"Mapped Article {article_id} to Category '{category_name}'")

    def hide_category(self, category_id):
        return self.repo.hide_category(category_id)

    def set_category_visibility(self, category_id: int, is_visible: bool):
        return self.repo.update_visibility(category_id, is_visible)
