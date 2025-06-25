from client.api.api_client import APIClient
from client.menu.main_menu import MainMenu

def main():
    api = APIClient()
    menu = MainMenu(api)
    menu.show()

if __name__ == "__main__":
    main()
