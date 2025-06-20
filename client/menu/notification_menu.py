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
                resp = self.api.get_notifications()
                if resp.ok:
                    for n in resp.json():
                        print(f"{n['notification_id']}: {n['message']}")
                else:
                    print("Failed to fetch notifications.")
                self.pause()
            elif choice == "2":
                print("Notification configuration not implemented.")
                self.pause()
            elif choice == "3":
                print("Keyword addition not implemented.")
                self.pause()
            elif choice == "4":
                break
            else:
                print("Invalid choice.")
                self.pause()
