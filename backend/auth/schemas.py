from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int
    name: str
    email: EmailStr | None = None
    is_active: bool | None = None


class UserInDB(User):
    hashed_password: str


class UserRegistr(User):
    password: str
