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
                HeadlinesMenu(self.api_client).handle_input()
            elif choice == "2":
                self.view_saved_articles()
            elif choice == "3":
                self._search_art()
            elif choice == "4":
                NotificationMenu(self.api_client).show()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    def _view_articles(self):
        response = self.api_client.get_articles()
        if response.ok:
            for article in response.json():
                print(f"{article['article_id']}: {article['title']}")
        else:
            print("Failed to fetch art.")


    def _view_categories(self):
        response = self.api_client.get_categories()
        if response.ok:
            for cat in response.json():
                print(f"{cat['category_id']}: {cat['category_name']}")
        else:
            print("Failed to fetch categories.")


    def _save_article(self):
        article_id = input("Enter Article ID to save: ")
        response = self.api_client.save_article(article_id)
        print("Article saved." if response.ok else "Failed to save article.")

    def view_saved_articles(self):
        response = self.api_client.get_saved_articles()
        if response.ok:
            self.display_articles(response.json())
        else:
            print("Failed to fetch saved art.")

    def _delete_saved_article(self):
        saved_id = input("Enter Saved Article ID to delete: ")
        response = self.api_client.delete_saved_article(saved_id)
        print("Saved article deleted." if response.ok else "Failed to delete saved article.")

    def display_articles(self, articles):
        for article in articles:
            print(f"\nArticle Id: {article.get('article_id')}")
            print(f"\nTitle: {article.get('title')}")
            print(f"\nDescription: {article.get('description', '')}\n\n")
            print(f"\nContent: {article.get('content', '')}")
            print(f"\nSource: {article.get('source')}")
            print(f"\nURL: {article.get('url')}")

    def _search_art(self):
        keyword = input("Enter search keyword: ")
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")
        sort_by = input("Sort_by (likes or dislikes): ")
        params = {
            "keyword": keyword,
            "start_date": start_date,
            "end_date": end_date,
            "sort_by": sort_by
        }
        response = self.api_client.search_articles(params)
        if response.ok:
            articles = response.json()
            self.display_articles(articles)
        else:
            print("Search failed.")
