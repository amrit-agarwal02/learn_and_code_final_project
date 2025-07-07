import unittest
from server.services.category_classifier import CategoryClassifier

class TestCategoryClassifier(unittest.TestCase):
    def test_classify_type(self):
        service = CategoryClassifier()
        result = service.classify('sample title', 'sample description', 'sample content')
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main() 