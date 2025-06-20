from client.menu.base_menu import BaseMenu

class AdminMenu(BaseMenu):
    def show(self):
        while True:
            print("\nAdmin Menu:")
            print("1. View external servers")
            print("2. Server details")
            print("3. Update API key")
            print("4. Add category")
            print("5. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self._display_servers()
            elif choice == "2":
                server_id = input("Enter server ID: ")
                self._display_server_details(server_id)
            elif choice == "3":
                server_id = input("Enter server ID: ")
                api_key = input("Enter new API key: ")
                self._simple_action(self.api.update_external_server_api_key(server_id, api_key), "API key updated.")
            elif choice == "4":
                name = input("Enter category name: ")
                self._simple_action(self.api.add_category(name), "Category added.")
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice.")
            self.pause()

    def _display_servers(self):
        resp = self.api.get_external_servers()
        if resp.ok:
            for srv in resp.json():
                status = "Active" if srv["is_active"] else "Not Active"
                print(f"{srv['server_id']}: {srv['server_name']} - {status} - Last Accessed: {srv.get('last_accessed')}")
        else:
            print("Failed to fetch servers.")

    def _display_server_details(self, server_id):
        resp = self.api.get_external_server_details(server_id)
        if resp.ok:
            srv = resp.json()
            print(f"Server: {srv['server_name']} - API Key: {srv['api_key']}")
        else:
            print("Failed to fetch server details.")

    def _simple_action(self, resp, message):
        print(message if resp.ok else "Operation failed.")
