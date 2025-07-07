from client.api.user_client import UserClient
from client.menu.main_menu import MainMenu

def main():
    api = UserClient()
    menu = MainMenu(api)
    menu.show()

if __name__ == "__main__":
    main()
