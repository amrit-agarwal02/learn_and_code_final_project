from client.auth.auth_handler import AuthHandler
from client.menu.admin_menu import AdminMenu
from client.menu.user_menu import UserMenu
from client.menu.base_menu import BaseMenu
from client.api.admin_client import AdminClient

class MainMenu(BaseMenu):
    def __init__(self, api):
        super().__init__(api)
        self.auth = AuthHandler(api)

    def show(self):
        while True:
            print("\nWelcome to the News Aggregator")
            print("1. Login")
            print("2. Sign up")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1" and self.auth.login():
                self._show_role_related_menu()
            elif choice == "2":
                self.auth.signup()
            elif choice == "3":
                print("Exiting application")
                break
            else:
                print("Try Again.")

    def _show_role_related_menu(self):
        if self.api.user_role == "admin":
            admin_api = AdminClient(token=self.api.token)
            AdminMenu(admin_api).show()
        else:
            UserMenu(self.api).show()