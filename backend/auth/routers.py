from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.crud import (add_user, authenticate_user, create_access_token,
                       get_current_active_user, get_user)
from auth.schemas import Token, User, UserRegistr
from database import get_db

router = APIRouter(tags=['auth'], prefix="/auth")

cur_user_dep = Annotated[User, Depends(get_current_active_user)]


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
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


@router.post('/register')
async def register_user(user_data: UserRegistr, db: Session = Depends(get_db)):
    print('user_data.name: ', user_data.name)
    user = get_user(db=db, username=user_data.name)
    print('user:', user)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    print('user_datra: ', user_data)
    return add_user(db, user_data)
