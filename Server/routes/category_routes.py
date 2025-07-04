from fastapi import APIRouter, Depends
from Server.Controllers.category_controller import CategoryController
from Server.schemas.category import CategoryCreate
from Server.Utils.jwt_handler import admin_required


router = APIRouter(prefix="/categories", tags=["category"])
controller = CategoryController()

@router.post("/category/create")
def create_category(category: CategoryCreate,user=Depends(admin_required)):
    return controller.create_category(category)

@router.put("/admin/category/{category_id}/visibility")
def toggle_category_visibility(category_id: int, is_visible: bool,  user= Depends(admin_required)):
    return controller.toggle_category_visibility(category_id, is_visible)