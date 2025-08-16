import sqlalchemy.sql.expression
from sqlalchemy.sql import func
from sqlalchemy import Integer, Column, String, Boolean, DateTime

from backend.database import Base, engine


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), comment='Электронная почта')
    name = Column(String(50), unique=True, index=True, comment='Имя')
    is_active = Column(Boolean, server_default=sqlalchemy.sql.expression.false(), nulable=False, comment='Признак актива ли запись')
    hashed_password = Column(String(), comment='ХЭШ пароля')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # __table_args__ = {'autoload_with': engine, 'extend_existing': True}
