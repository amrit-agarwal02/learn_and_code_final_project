from fastapi import HTTPException
from server.services.category_service import CategoryService
from server.schemas.category import CategoryCreate, CategoryUpdate
from server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_NOT_FOUND
from typing import List

class CategoryController:
    def __init__(self):
        self.service = CategoryService()

    def get_all_categories(self) -> List[dict]:
        return self.service.get_all_categories()

    def get_category_by_id(self, category_id: int) -> dict:
        return self.service.get_category_by_id(category_id)

    def create_category(self, category: CategoryCreate) -> dict:
        return self.service.create_category(category)

    def update_category(self, category_id: int, category: CategoryUpdate) -> dict:
        return self.service.update_category(category_id, category.name, category.description)

    def delete_category(self, category_id: int):
        self.service.delete_category(category_id)

    def hide_category(self, category_id):
        return self.service.hide_category(category_id)

    def toggle_category_visibility(self, category_id: int, is_visible: bool):
        return self.service.set_category_visibility(category_id, is_visible)