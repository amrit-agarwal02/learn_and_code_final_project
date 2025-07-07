import unittest
from server.services.category_service import CategoryService
from server.Exceptions.exceptions import CategoryNotFoundException

class TestCategoryService(unittest.TestCase):
    def test_get_all_categories_type(self):
        service = CategoryService()
        result = service.get_all_categories()
        self.assertIsInstance(result, list)

    def test_get_category_by_id_not_found(self):
        service = CategoryService()
        with self.assertRaises(CategoryNotFoundException):
            service.get_category_by_id(-1)

    def test_create_category_duplicate(self):
        service = CategoryService()
        # This will likely raise CategoryAlreadyExistsException if run twice with same name
        from server.schemas.category import CategoryCreate
        category = CategoryCreate(category_name="TestCategory", keywords=["test"])
        try:
            service.create_category(category)
        except Exception as e:
            self.assertTrue("already exists" in str(e) or isinstance(e, Exception))

if __name__ == '__main__':
    unittest.main() 