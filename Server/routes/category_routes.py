from fastapi import APIRouter, Depends
from Server.Controllers.category_controller import CategoryController
from Server.schemas.category import CategoryCreate
from Server.Utils.jwt_handler import admin_required


router = APIRouter(prefix="/categories", tags=["category"])

@router.post("/category/create")
def create_category(category: CategoryCreate,user=Depends(admin_required)):
    controller = CategoryController()
    return controller.create_category(category)