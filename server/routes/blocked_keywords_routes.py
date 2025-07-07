from fastapi import APIRouter, Depends, HTTPException
from server.controllers.blocked_keywords_controller import BlockedKeywordsController
from server.utils.jwt_handler import admin_required
from server.Exceptions.exceptions import CategoryAlreadyExistsException
from server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_BAD_REQUEST

router = APIRouter(prefix="/admin/keywords", tags=["admin-keywords"])
controller = BlockedKeywordsController()

@router.post("/keyword/block")
def block_keyword(keyword: str, user=Depends(admin_required)):
    try:
        return controller.add_keyword(keyword)
    except CategoryAlreadyExistsException as e:
        raise HTTPException(status_code=HTTP_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/keyword/unblock")
def unblock_keyword(keyword: str, user=Depends(admin_required)):
    try:
        return controller.remove_keyword(keyword)
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/blocked_keywords/view")
def list_blocked_keywords(user=Depends(admin_required)):
    try:
        return controller.get_all_keywords()
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")