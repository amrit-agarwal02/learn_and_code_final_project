from fastapi import APIRouter, Depends, Query
from server.controllers.blocked_keywords_controller import BlockedKeywordsController
from server.utils.jwt_handler import admin_required

router = APIRouter(prefix="/admin/keywords", tags=["admin-keywords"])
controller = BlockedKeywordsController()

@router.post("/keyword/block")
def block_keyword(keyword: str, user=Depends(admin_required)):
    return controller.add_keyword(keyword)

@router.delete("/keyword/unblock")
def unblock_keyword(keyword: str, user=Depends(admin_required)):
    return controller.remove_keyword(keyword)

@router.get("/blocked_keywords/view")
def list_blocked_keywords(user=Depends(admin_required)):
    return controller.get_all_keywords()