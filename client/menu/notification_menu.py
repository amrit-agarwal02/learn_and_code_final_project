from client.api.api_client import APIClient
from client.menu.base_menu import BaseMenu


class NotificationMenu(BaseMenu):
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def show(self):
        print("\nNOTIFICATIONS")
        print("1. View Notifications")
        print("2. Configure Notification")
        print("3. Back")
        print("4. Logout")

    def handle_input(self):
        while True:
            self.show()
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.view_notifications()
            elif choice == "2":
                self.view_notification_settings()
            elif choice == "3":
                break
            elif choice == "4":
                print("Logging out...")
                exit(0)
            else:
                print("Invalid choice. Please try again.")

    def view_notifications(self):
        response = self.api_client.get_notifications()
        if not response.ok:
            print("Error fetching notifications.")
            return

        notifications = response.json()
        if not notifications:
            print("No notifications found.")
            return

        print("\nYour Notifications:")
        for note in notifications:
            print(f"- {note.get('message')} (Date: {note.get('date')})")

    def view_notification_settings(self):
        response = self.api_client.get_notification_setting()
        if not response.ok:
            print("Error fetching notification settings.")
            return

        settings = response.json()
        if not settings:
            print("No notification settings configured.")
            return

        self.display_notification_settings(settings)
        self.handle_notification_setting_action(settings)

    def display_notification_settings(self, settings):
        print("\nYour Notification Settings:")
        print(f"{'No.':<4} {'Keyword':<20} {'Category':<20} {'Enabled':<8}")
        for idx, s in enumerate(settings, 1):
            keyword = s['keyword'] or "-"
            status = "Yes" if s['is_enabled'] else "No"
            print(f"{idx:<4} {keyword:<20} {s['category_name']:<20} {status:<8}")

    def handle_notification_setting_action(self, settings):
        print("\nChoose an action:")
        print("1. Toggle a setting")
        print("2. Back")
        print("3. Logout")

        while True:
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.toggle_notification_setting(settings)
                return
            elif choice == "2":
                return
            elif choice == "3":
                print("Logging out...")
                exit(0)
            else:
                print("Invalid input. Try again.")

    def toggle_notification_setting(self, settings):
        try:
            idx = int(input("Enter setting number to toggle: ")) - 1
            if not 0 <= idx < len(settings):
                print("Invalid selection.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return

        selected = settings[idx]
        new_status = not selected['is_enabled']

        response = self.api_client.configure_notification(
            category_id=selected['category_id'],
            is_enabled=new_status,
            keyword=selected.get('keyword')
        )

        if not response.ok:
            print("Failed to update setting.")
        else:
            status_str = "enabled" if new_status else "disabled"
            keyword = selected.get('keyword') or 'N/A'
            print(f"Notification for category '{selected['category_name']}' with keyword '{keyword}' has been {status_str}.")
