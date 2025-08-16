from sqlalchemy.orm import Session

from backend.auth.auth import verify_password
from backend.auth.models import Users
from backend.auth.schemas import UserInDB


def get_user(db: Session, username: str):
    user = db.query(Users).filter_by(name=username, is_active=True)
    return UserInDB(**user.__dict__)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
