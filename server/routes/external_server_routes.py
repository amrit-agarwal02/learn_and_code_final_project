from fastapi import APIRouter, Depends, HTTPException
from server.controllers.external_server_controller import ExternalServerController
from server.utils.jwt_handler import admin_required
from server.schemas.external_server import UpdateServerKeyRequest
from server.Exceptions.exceptions import ExternalServerNotFoundException
from server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_NOT_FOUND

router = APIRouter(prefix="/external-servers", tags=["external_servers"])

@router.get("/all")
def get_all_external_servers(user=Depends(admin_required)):
    try:
        controller = ExternalServerController()
        return controller.get_all_external_servers()
    except ExternalServerNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/server-details")
def get_server_details(user=Depends(admin_required)):
    try:
        controller = ExternalServerController()
        return controller.get_external_server_details()
    except ExternalServerNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.patch("/update-server")
def update_server_key(update_server_key_request:UpdateServerKeyRequest, user=Depends(admin_required)):
    try:
        controller = ExternalServerController()
        server_id = update_server_key_request.server_id
        updated_api_key = update_server_key_request.updated_api_key
        return controller.update_server_key(server_id, updated_api_key)
    except ExternalServerNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")