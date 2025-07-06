from server.repositories.external_server_repo import ExternalServerRepository

class ExternalServerService:
    def __init__(self):
        self.server_repo = ExternalServerRepository()

    def get_all_external_servers(self):
        return self.server_repo.fetch_all_external_servers()

    def get_external_server_details(self):
        return self.server_repo.get_server_details()

    def update_server_key(self, server_id: int, new_api_key: str):
        return self.server_repo.update_server_api_key(server_id, new_api_key)