from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import UserCreate, Token, UserShow
from ..services.auth_service import (
    create_user,
    authenticate_user,
)

router = APIRouter()


# PUBLIC_INTERFACE
@router.post("/signup", response_model=UserShow, summary="Register new user")
def signup(user: UserCreate):
    """
    Register a new user.
    """
    new_user = create_user(user)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists."
        )
    return new_user


# PUBLIC_INTERFACE
@router.post("/login", response_model=Token, summary="User login (get JWT token)")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and return JWT token.
    """
    token = authenticate_user(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
