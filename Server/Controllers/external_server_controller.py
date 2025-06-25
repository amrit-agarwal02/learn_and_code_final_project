from fastapi import HTTPException
from Server.Services.external_server_service import ExternalServerService
from Server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR

class ExternalServerController:
    def __init__(self):
        self.server_service = ExternalServerService()

    def get_all_external_servers(self):
        try:
            return self.server_service.get_all_external_servers()
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_external_server_details(self):
        try:
            return self.server_service.get_external_server_details()
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))
