from fastapi import APIRouter, Depends, HTTPException
from server.controllers.category_controller import CategoryController
from server.schemas.category import CategoryCreate
from server.utils.jwt_handler import admin_required, get_current_user
from server.Exceptions.exceptions import CategoryAlreadyExistsException, CategoryNotFoundException
from server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_BAD_REQUEST, HTTP_NOT_FOUND

router = APIRouter(prefix="/categories", tags=["category"])
controller = CategoryController()

@router.post("/create")
def create_category(category: CategoryCreate,user=Depends(admin_required)):
    try:
        return controller.create_category(category)
    except CategoryAlreadyExistsException as e:
        raise HTTPException(status_code=HTTP_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/view-all")
def get_all_categories(user=Depends(get_current_user)):
    try:
        return controller.get_all_categories()
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/admin/category/visibility")
def toggle_category_visibility(category_id: int, is_visible: bool,  user= Depends(admin_required)):
    try:
        return controller.toggle_category_visibility(category_id, is_visible)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")