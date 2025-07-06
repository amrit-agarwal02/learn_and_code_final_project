from client.menu.base_menu import BaseMenu

class AdminMenu(BaseMenu):
    def show(self):
        while True:
            print("\nAdmin Menu:")
            print("1. View external servers and status")
            print("2. View external server details")
            print("3. Update/Edit external server API key")
            print("4. Add new News Category")
            print("5. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self._view_servers()
            elif choice == "2":
                self._view_server_details()
            elif choice == "3":
                self._update_api_key()
            elif choice == "4":
                self._add_category()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    def _view_servers(self):
        response = self.api.get_external_servers()
        if response.ok:
            for server in response.json():
                status = "Active" if server["is_active"] else "Not Active"
                print(f"{server['server_id']}: {server['server_name']} - {status} - Last Accessed: {server.get('last_accessed')}")
        else:
            print("Failed to fetch servers.")

    def _view_server_details(self):
        response = self.api.get_external_server_details()
        if response.ok:
            server_details = response.json()
            for server in server_details:
                print(f"Server: {server['server_name']} - API Key: {server['api_key']}")
        else:
            print("Failed to fetch server details.")

    def _update_api_key(self):
        server_id = input("Enter server ID: ")
        api_key = input("Enter new API key: ")
        response = self.api.update_external_server_api_key(server_id, api_key)
        print("API key updated." if response.ok else "Failed to update API key.")


    def _add_category(self):
        category_name = input("Enter new category name: ")
        raw_keywords = input(f"Enter keywords for '{category_name}' (comma-separated): ")
        category_keywords = [kw.strip().lower() for kw in raw_keywords.split(",") if kw.strip()]

        if not category_keywords:
            print("No valid keywords entered. Aborting.")
            return

        response = self.api.add_category(category_name, category_keywords)
        print("Category added." if response.ok else "Failed to add category.")
