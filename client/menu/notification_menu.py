from client.api.user_client import UserClient
from client.menu.base_menu import BaseMenu


class NotificationMenu(BaseMenu):
    def __init__(self, api_client: UserClient):
        self.api_client = api_client

    def show(self):
        print("\nNOTIFICATIONS")
        print("1. View Notifications")
        print("2. Configure Notifications")
        print("3. Back")
        print("4. Logout")

    def handle_input(self):
        while True:
            self.show()
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.view_notifications()
            elif choice == "2":
                self.configure_notifications()
            elif choice == "3":
                break
            elif choice == "4":
                print("Logging out...")
                exit(0)
            else:
                print("Invalid choice. Please try again.")

    def view_notifications(self):
        print("VIEWING NOTIFICATIONS")

        response = self.api_client.get_notifications()
        if not response.ok:
            print("Error fetching notifications.")
            return

        notifications = response.json()
        if not notifications:
            print("No notifications found.")
            return

        for idx, notification in enumerate(notifications, 1):
            message = notification.get('message', 'No message')
            article_id = notification.get('article_id', '')
            print(f"{idx}.Article ID {article_id} {message}")

    def configure_notifications(self):
        while True:
            print("CONFIGURE NOTIFICATIONS")

            categories = self.get_available_categories()
            current_settings = self.get_current_settings()

            if not categories:
                print("No categories available.")
                return

            self.display_categories_with_status(categories, current_settings)
            print(f"{len(categories) + 1}. Keywords")
            print(f"{len(categories) + 2}. Back")
            print(f"{len(categories) + 3}. Logout")

            try:
                choice = int(input("\nEnter your choice: ").strip())

                if 1 <= choice <= len(categories):
                    selected_category = categories[choice - 1]
                    self.toggle_category_status(selected_category, current_settings)
                elif choice == len(categories) + 1:
                    self.handle_keywords_configuration()
                elif choice == len(categories) + 2:
                    break
                elif choice == len(categories) + 3:
                    print("Logging out...")
                    exit(0)
                else:
                    print("Invalid choice. Please try again.")

            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print(f"Error: {e}")

    def display_categories_with_status(self, categories, current_settings):
        print("\nAvailable Categories:")

        for idx, category in enumerate(categories, 1):
            category_name = category['category_name']
            status = self.get_category_status(category_name, current_settings)
            status_text = "Enabled" if status else "Disabled"

            print(f"{idx}. {category_name} - {status_text}")

    def get_category_status(self, category_name, current_settings):
        for setting in current_settings:
            if setting.get('category_name') == category_name and setting.get('is_enabled'):
                return True
        return False

    def get_current_settings(self):
        response = self.api_client.get_notification_setting()
        if response.ok:
            return response.json()
        return []

    def handle_keywords_configuration(self):
        print("KEYWORDS CONFIGURATION")
        current_settings = self.get_current_settings()

        print("\nCurrent Keyword Settings:")


        keyword_settings = [s for s in current_settings if s.get('keyword')]
        if keyword_settings:
            for idx, setting in enumerate(keyword_settings, 1):
                category = setting.get('category_name', 'Unknown')
                keyword = setting.get('keyword', '')
                status = "Enabled" if setting.get('is_enabled') else "Disabled"
                print(f"{idx}. {category} - Keyword: '{keyword}' - {status}")
        else:
            print("No keyword settings configured.")

        print("\nAdd New Keyword Setting:")

        categories = self.get_available_categories()
        if not categories:
            print("No categories available.")
            return

        print("\nAvailable Categories:")
        for idx, category in enumerate(categories, 1):
            print(f"{idx}. {category['category_name']}")

        try:
            category_choice = int(input("\nSelect category (enter number): ").strip())
            if not 1 <= category_choice <= len(categories):
                print("Invalid category selection.")
                return
            selected_category = categories[category_choice - 1]['category_name']
        except ValueError:
            print("Please enter a valid number.")
            return

        print(f"\nEnter keyword for '{selected_category}' category:")
        keyword = input("Keyword: ").strip()

        if not keyword:
            print("Keyword cannot be empty.")
            return

        response = self.api_client.configure_notification(
            category=selected_category,
            is_enabled=True,
            keyword=keyword
        )

        if response.ok:
            print(f"Keyword '{keyword}' added for '{selected_category}' category!")
        else:
            print("Failed to add keyword setting.")

    def toggle_category_status(self, category, current_settings):
        category_name = category['category_name']
        current_status = self.get_category_status(category_name, current_settings)
        new_status = not current_status

        existing_setting = None
        for setting in current_settings:
            if setting.get('category_name') == category_name:
                existing_setting = setting
                break

        keyword = existing_setting.get('keyword') if existing_setting else None

        response = self.api_client.configure_notification(
            category=category_name,
            is_enabled=new_status,
            keyword=keyword
        )

        if response.ok:
            status_text = "enabled" if new_status else "disabled"
            print(f"{category_name} has been {status_text}!")
        else:
            print(f" Failed to update {category_name} status.")

    def get_available_categories(self):
        response = self.api_client.get_categories()
        if response.ok:
            return response.json()
        else:
            print("Error fetching categories.")
            return []
