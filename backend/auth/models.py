import sqlalchemy.sql.expression
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), comment='Электронная почта')
    name = Column(String(50), unique=True, index=True, comment='Имя')
    is_active = Column(Boolean, server_default=sqlalchemy.sql.expression.false(), comment='Признак актива ли запись')
    hashed_password = Column(String(), comment='ХЭШ пароля')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    expenses = relationship('Expense', back_populates='user')
    incomes = relationship('Income', back_populates='user')

    categories_expense = relationship('CategoryExpense', back_populates='user')
    categories_income = relationship('CategoryIncome', back_populates='user')
    expense_type = relationship('ExpenseType', back_populates='user')
