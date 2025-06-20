# client/menus/user_menu.py
from client.menu.base_menu import BaseMenu
from client.menu.notification_menu import NotificationMenu

class UserMenu(BaseMenu):
    def show(self):
        while True:
            print("\nUser Menu:")
            print("1. View Headlines")
            print("2. View Categories")
            print("3. Save Article")
            print("4. View Saved Articles")
            print("5. Delete Saved Article")
            print("6. Search Articles")
            print("7. Notifications")
            print("8. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self._display_list(self.api.get_articles(), 'article_id', 'title')
            elif choice == "2":
                self._display_list(self.api.get_categories(), 'category_id', 'category_name')
            elif choice == "3":
                article_id = input("Enter Article ID to save: ")
                self._simple_action(self.api.save_article(article_id), "Article saved.")
            elif choice == "4":
                self._display_list(self.api.get_saved_articles(), 'saved_id', 'article_id')
            elif choice == "5":
                saved_id = input("Enter Saved Article ID to delete: ")
                self._simple_action(self.api.delete_saved_article(saved_id), "Saved article deleted.")
            elif choice == "6":
                query = input("Enter search query: ")
                start = input("Start date (YYYY-MM-DD, optional): ")
                end = input("End date (YYYY-MM-DD, optional): ")
                self._display_list(self.api.search_articles(query, start or None, end or None), 'article_id', 'title')
            elif choice == "7":
                NotificationMenu(self.api).show()
            elif choice == "8":
                print("Logging out...")
                break
            else:
                print("Invalid choice.")
            self.pause()

    def _display_list(self, resp, key_field, value_field):
        if resp.ok:
            for item in resp.json():
                print(f"{item[key_field]}: {item[value_field]}")
        else:
            print("Failed to fetch data.")

    def _simple_action(self, resp, success_message):
        if resp.ok:
            print(success_message)
        else:
            print("Operation failed.")
