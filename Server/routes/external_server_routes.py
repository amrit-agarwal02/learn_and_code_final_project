from fastapi import APIRouter, Depends
from Server.Controllers.external_server_controller import ExternalServerController
from Server.Utils.jwt_handler import admin_required

router = APIRouter(prefix="/external-servers", tags=["external_servers"])

@router.get("/all")
def get_all_external_servers(user=Depends(admin_required)):
    controller = ExternalServerController()
    return controller.get_all_external_servers()
