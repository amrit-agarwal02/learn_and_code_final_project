from client.api import APIClient

def main_menu():
    print("\nWelcome to the News Aggregator application. Please choose the options below.")
    print("1. Login")
    print("2. Sign up")
    print("3. Exit")
    return input("Enter your choice: ")

def show_menu_by_role(api: APIClient):
    if api.user_role == "admin":
        print("admin_menu")
    else:
        print("user_menu")