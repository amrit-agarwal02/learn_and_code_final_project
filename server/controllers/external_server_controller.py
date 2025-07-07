from server.services.external_server_service import ExternalServerService

class ExternalServerController:
    def __init__(self):
        self.server_service = ExternalServerService()

    def get_all_external_servers(self):
        return self.server_service.get_all_external_servers()

    def get_external_server_details(self):
        return self.server_service.get_external_server_details()

    def update_server_key(self, server_id: int, new_api_key: str):
        return self.server_service.update_server_key(server_id, new_api_key)
