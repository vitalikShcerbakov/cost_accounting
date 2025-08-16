import sqlalchemy.sql.expression
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from backend.database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), comment='Электронная почта')
    name = Column(String(50), unique=True, index=True, comment='Имя')
    is_active = Column(Boolean, server_default=sqlalchemy.sql.expression.false(), nulable=False, comment='Признак актива ли запись')
    hashed_password = Column(String(), comment='ХЭШ пароля')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
