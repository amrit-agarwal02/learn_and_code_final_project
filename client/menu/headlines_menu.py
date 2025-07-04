from client.menu.base_menu import BaseMenu

class HeadlinesMenu(BaseMenu):
    def show(self):
        while True:
            print("\nHeadlines Menu:")
            print("1. Today")
            print("2. Date Range")
            print("3. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_today_headlines()
            elif choice == "2":
                print("Date Range")
            elif choice == "3":
                print("Keyword ")
            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    def view_today_headlines(self):
        response = self.api.get_same_day_articles()
        if response.ok:
            for article in response.json():
                print(article)
        else:
            print("Failed to fetch today articles.")

