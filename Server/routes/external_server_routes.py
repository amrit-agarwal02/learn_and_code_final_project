from fastapi import APIRouter, Depends
from Server.Controllers.external_server_controller import ExternalServerController
from Server.Utils.jwt_handler import admin_required

router = APIRouter(prefix="/external-servers", tags=["external_servers"])

@router.get("/all")
def get_all_external_servers(user=Depends(admin_required)):
    controller = ExternalServerController()
    return controller.get_all_external_servers()

@router.get("/server-details")
def get_server_details(user=Depends(admin_required)):
    controller = ExternalServerController()
    return controller.get_external_server_details()

@router.patch("/update-server")
def update_server_key(server_id,updated_api_key, user=Depends(admin_required)):
    controller = ExternalServerController()
    return controller.update_server_key(server_id, updated_api_key)