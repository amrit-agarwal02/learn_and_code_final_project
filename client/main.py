from client.api import APIClient
from client.auth import signup, login
from client.menu import main_menu, show_menu_by_role

def main():
    api = APIClient()
    while True:
        choice = main_menu()
        if choice == "1":
            if login(api):
                show_menu_by_role(api)
                break
        elif choice == "2":
            signup(api)
            break
        elif choice == "3":
            print("Exiting application.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main() 