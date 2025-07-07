from fastapi import APIRouter, HTTPException

from server.config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED
from server.schemas.auth import UserCredentials, TokenResponse
from server.schemas.user import UserOut, UserCreate
from server.controllers.auth_controller import AuthController
from server.Exceptions.exceptions import UserNotFoundException, UserAlreadyExistsException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login",response_model= TokenResponse)
def login(user_data: UserCredentials):
    try:
        auth_controller = AuthController()
        return auth_controller.login(user_data)
    except UserNotFoundException as e:
        raise HTTPException(status_code=HTTP_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_BAD_REQUEST, detail=str(e))


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate):
    try:
        auth_controller = AuthController()
        return auth_controller.register(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=HTTP_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail="Internal server error")