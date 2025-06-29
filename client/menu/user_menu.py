from client.api.api_client import APIClient
from client.menu.base_menu import BaseMenu
from client.menu.notification_menu import NotificationMenu
from client.menu.headlines_menu import HeadlinesMenu
from client.api.api_client import APIClient
from datetime import datetime

class UserMenu(BaseMenu):

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def show(self):
        print("Welcome to the News Application, ", self.api_client.user_name)
        print(datetime.now())
        while True:
            print("\nUser Menu:")
            print("1. Headlines")
            print("2. Saved Articles")
            print("3. Search")
            print("4. Notifications")
            print("5. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                HeadlinesMenu(self.api).show()
            elif choice == "2":
                self._view_saved_art()
            elif choice == "3":
                self._search_art()
            elif choice == "4":
                NotificationMenu(self.api).show()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    def _view_articles(self):
        response = self.api.get_articles()
        if response.ok:
            for article in response.json():
                print(f"{article['article_id']}: {article['title']}")
        else:
            print("Failed to fetch art.")


    def _view_categories(self):
        response = self.api.get_categories()
        if response.ok:
            for cat in response.json():
                print(f"{cat['category_id']}: {cat['category_name']}")
        else:
            print("Failed to fetch categories.")


    def _save_article(self):
        article_id = input("Enter Article ID to save: ")
        response = self.api.save_article(article_id)
        print("Article saved." if response.ok else "Failed to save article.")

    def _view_saved_art(self):
        response = self.api.get_saved_art()
        if response.ok:
            for art in response.json():
                print(f"{art['saved_id']}: {art['article_id']}")
        else:
            print("Failed to fetch saved art.")

    def _delete_saved_article(self):
        saved_id = input("Enter Saved Article ID to delete: ")
        response = self.api.delete_saved_article(saved_id)
        print("Saved article deleted." if response.ok else "Failed to delete saved article.")


    def _search_art(self):
        query = input("Enter search query: ")
        start_date = input("Start date (YYYY-MM-DD, optional): ")
        end_date = input("End date (YYYY-MM-DD, optional): ")
        response = self.api.search_art(query, start_date or None, end_date or None)
        if response.ok:
            for art in response.json():
                print(f"{art['article_id']}: {art['title']}")
        else:
            print("Search failed.")
