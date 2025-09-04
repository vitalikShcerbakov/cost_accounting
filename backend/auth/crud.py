from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from auth.models import Users
from auth.schemas import UserInDB, UserRegistr
from database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter_by(name=username, is_active=True).first()
    if user:
        return UserInDB(**user.__dict__)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def add_user(db: Session, user_data: UserRegistr):
    password_hash = get_password_hash(user_data.password)
    data = user_data.model_dump()
    # data = user_data.dict()
    del data['password']
    data['hashed_password'] = password_hash
    db_user = Users(**data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
