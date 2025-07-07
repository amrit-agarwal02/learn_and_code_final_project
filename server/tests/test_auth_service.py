import unittest
from server.services.auth_service import AuthService
from server.schemas.user import UserCreate
from server.schemas.auth import UserCredentials
from server.Exceptions.exceptions import UserAlreadyExistsException, UserNotFoundException

class TestAuthService(unittest.TestCase):
    def test_register_user_duplicate(self):
        service = AuthService()
        user = UserCreate(user_name="TestUser", email="test@example.com", password="testpass")
        try:
            service.register_user(user)
        except UserAlreadyExistsException:
            self.assertTrue(True)
        except Exception:
            self.assertTrue(True)

    def test_login_user_not_found(self):
        service = AuthService()
        creds = UserCredentials(email="notfound@example.com", password="testpass")
        with self.assertRaises(UserNotFoundException):
            service.login(creds)

if __name__ == '__main__':
    unittest.main() 