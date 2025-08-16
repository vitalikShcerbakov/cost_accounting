from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.auth.auth import create_access_token, get_current_active_user
from backend.auth.schemas import Token, User
from backend.auth.crud import authenticate_user

router = APIRouter(tags=['auth'], prefix="/api")

cur_user_dep = Annotated[User, Depends(get_current_active_user)]


@router.post("/token")
async def login_for_access_token(
    db: Session,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=dict[str, User])
async def get_me(current_user: cur_user_dep):
    return {"user": current_user}
