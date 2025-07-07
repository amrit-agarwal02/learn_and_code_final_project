from getpass import getpass
from client.api.user_client import UserClient
from client.utils import validate_email


class AuthHandler:
    def __init__(self, api: UserClient):
        self.api = api

    def login(self) -> bool:
        print("\nLogin ")
        email = input("Email: ")
        password = getpass("Password: ")
        response = self.api.login(email, password)
        if response.ok:
            print("Login successful!")
            return True
        print(f"Login failed: Try again with correct Email and password")
        return False

    def signup(self):
        print("\nSign Up")
        username = input("Username: ")
        email = input("Email: ")
        if not validate_email(email):
            print("Invalid email format.")
            return
        password = getpass("Password: ")
        response = self.api.register(username, email, password)
        if response.ok:
            print("Registration successful! Please log in.")
        else:
            print(f"Registration failed: Try again")
