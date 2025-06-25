from client.menu.base_menu import BaseMenu

class NotificationMenu(BaseMenu):
    def show(self):
        while True:
            print("\nNotifications Menu:")
            print("1. View Notifications")
            print("2. Configure Notifications (stub)")
            print("3. Add Keyword (stub)")
            print("4. Back")
            choice = input("Enter your choice: ")

            if choice == "1":
                self._view_notifications()
            elif choice == "2":
                print("Notification ")
            elif choice == "3":
                print("Keyword ")
            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    def _view_notifications(self):
        response = self.api.get_notifications()
        if response.ok:
            for n in response.json():
                print(f"{n['notification_id']}: {n['message']}")
        else:
            print("Failed to fetch notifications.")

