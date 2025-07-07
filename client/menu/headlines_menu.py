from client.api.user_client import UserClient
from client.menu.base_menu import BaseMenu
from datetime import datetime


class HeadlinesMenu(BaseMenu):

    def __init__(self, api_client: UserClient):
        self.api_client = api_client

    def show(self):
        print("\nHeadlines Menu:")
        print("1. Today")
        print("2. Date range")
        print("3. Back")
        print("4. Logout")

    def handle_input(self):
        while True:
            self.show()
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.show_today_headlines()
            elif choice == "2":
                self.show_date_range_headlines()
            elif choice == "3":
                break
            elif choice == "4":
                print("Logging out...")
                exit(0)
            else:
                print("Invalid choice. Please try again.")

    def show_today_headlines(self):
        response = self.api_client.get_today_articles()
        if "error" in response:
            print(f"Error: {response['error']}")
            return

        articles = response.json()
        if not articles:
            print("No articles found for today.")
            return

        self.display_articles(articles)
        self.show_article_actions(articles)

    def show_date_range_headlines(self):
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        self.show_headlines_by_date_range(start_date, end_date)

    def show_headlines_by_date_range(self, start_date, end_date):
        category = self.get_category_from_user()
        if not category:
            return

        self.fetch_articles(start_date, end_date, category)

    def get_category_from_user(self):
        categories_response = self.fetch_categories()
        categories = categories_response.json()
        if not categories:
            print("No categories available.")
            return None

        self.show_category_menu(categories)
        return self.get_user_category_choice(categories)

    def fetch_categories(self):
        response = self.api_client.get_categories()
        if "error" in response:
            print(f"Error fetching categories: {response['error']}")
            return []
        return response

    def show_category_menu(self, categories):
        print("\nSelect category:")
        print("1. All")
        for idx, category in enumerate(categories, 2):
            print(f"{idx}. {category.get('category_name', 'Unknown')}")
        print(f"{len(categories) + 2}. Back")

    def get_user_category_choice(self, categories):
        """Get user's category choice"""
        while True:
            choice = int(input("Choose category: "))
            if choice == len(categories) + 2:
                return None
            if choice == 1:
                return "all"
            try:
                idx = int(choice) - 2
                if 0 <= idx < len(categories):
                    return categories[idx].get('category_name', 'all')
            except ValueError:
                pass
            print("Invalid choice. Please try again.")

    def fetch_articles(self, start_date, end_date, category):
        response = self.api_client.get_article_by_date_range(start_date, end_date, category)
        if "error" in response:
            print(f"Error: {response['error']}")
            return

        articles = response.json()
        if not articles:
            print("No articles found.")
            return

        self.display_articles(articles)
        self.show_article_actions(articles)

    def display_articles(self, articles):
        for article in articles:
            print(f"\nArticle Id: {article.get('article_id')}")
            print(f"\nTitle: {article.get('title')}")
            print(f"\nDescription: {article.get('description', '')}\n\n")

    def show_article_actions(self, articles):

        while True:
            print("\n1. View Article")
            print("2. Save Article")
            print("3. Back")
            print("4. Logout")
            action = input("Choose an action: ").strip()
            if action == "1":
                article_id = input("Enter Article Id to view: ")
                self.view_article(article_id)
            elif action == "2":
                article_id = input("Enter Article Id to save: ")
                self.save_article(article_id)
            elif action == "3":
                return
            elif action == "4":
                print("Logging out...")
                # self.auth_handler.logout()
                exit(0)
            else:
                print("Invalid choice. Please try again.")

    def view_article(self, article_id):
        response = self.api_client.get_article_by_id(article_id)
        if "error" in response:
            print(f"Error: {response['error']}")
            return

        article = response.json()
        if not article:
            print("Article not found.")
            return

        # Display full article
        print(f"\nArticle Id: {article.get('article_id')}")
        print(f"\nTitle: {article.get('title')}")
        print(f"\nDescription: {article.get('description', '')}")
        print(f"\nContent: {article.get('content', '')}")
        print(f"\nSource: {article.get('source')}")
        print(f"\nURL: {article.get('url')}")

        self.show_article_interaction_options(article_id)

    def show_article_interaction_options(self, article_id):

        while True:
            print("\n1. Like Article")
            print("2. Dislike Article")
            print("3. Report Article")
            print("4. Back")
            choice = input("Choose an action: ").strip()
            if choice == "1":
                self.like_article(article_id)
            elif choice == "2":
                self.dislike_article(article_id)
            elif choice == "3":
                self.report_article(article_id)
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")

    def like_article(self, article_id):
        response = self.api_client.like_article(article_id)
        if "error" in response:
            print(f"Error: {response['error']}")
        else:
            print("Article liked successfully!")

    def dislike_article(self, article_id):
        response = self.api_client.dislike_article(article_id)
        if "error" in response:
            print(f"Error: {response['error']}")
        else:
            print("Article disliked successfully!")

    def report_article(self, article_id, reason):
        response = self.api_client.report_article(article_id, reason)
        if "error" in response:
            print(f"Error: {response['error']}")
        else:
            print("Article reported successfully!")

    def save_article(self, article_id):
        response = self.api_client.save_article(article_id)
        if "error" in response:
            print(f"Error: {response['error']}")
        else:
            print("Article saved.")

