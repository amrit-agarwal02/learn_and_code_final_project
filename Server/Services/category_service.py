from Server.Repositories.category_repo import CategoryRepository
from typing import List


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

    def create_category(self, name: str, description: str = None) -> dict:
        existing = self.repo.get_by_name(name)
        if existing:
            raise ValueError(f"Category '{name}' already exists")
        return self.repo.create(name, description)

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
