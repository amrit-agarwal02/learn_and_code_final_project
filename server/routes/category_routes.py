from fastapi import APIRouter, Depends
from server.controllers.category_controller import CategoryController
from server.schemas.category import CategoryCreate
from server.utils.jwt_handler import admin_required, get_current_user


router = APIRouter(prefix="/categories", tags=["category"])
controller = CategoryController()

@router.post("/create")
def create_category(category: CategoryCreate,user=Depends(admin_required)):
    return controller.create_category(category)

@router.get("/view-all")
def get_all_categories(user=Depends(get_current_user)):
    return controller.get_all_categories()

@router.put("/admin/category/visibility")
def toggle_category_visibility(category_id: int, is_visible: bool,  user= Depends(admin_required)):
    return controller.toggle_category_visibility(category_id, is_visible)