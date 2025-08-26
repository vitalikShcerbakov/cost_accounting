#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных с начальными данными
"""

from app import models
from database import SessionLocal, engine


def init_db():
    db = SessionLocal()
    try:
        # Создание таблиц
        models.Base.metadata.create_all(bind=engine)
        # Создание ползьватей
        user_data = {
            "name": "admin",
            "email": "admin@gmail.com",
            "is_active": True,
            "hashed_password": "$2b$12$sWo1FFh4H1Fpse0PvOPy6O./CbMB6P2Wnz39eMWAo7y43yfZ4jwz6"
        }
        existing = db.query(models.Users).filter(models.Users.name == user_data['name']).first()
        if not existing:
            user = models.Users(**user_data)
            db.add(user)
        # Создание начальных категорий
        categories_expenses_data = [
            {"name": "Продукты", "description": "Продукты питания", "color": "#4CAF50", "user_id": 0},
            {"name": "Транспорт", "description": "Общественный транспорт, такси", "color": "#2196F3", "user_id": 0},
            {"name": "Автомобиль", "description": "Топливо, ремонт, страховка", "color": "#FF9800", "user_id": 0},
            {"name": "Жилье", "description": "Квартплата, коммунальные услуги", "color": "#9C27B0", "user_id": 0},
            {"name": "Развлечения", "description": "Кино, рестораны, хобби", "color": "#E91E63", "user_id": 0},
            {"name": "Здоровье", "description": "Медицина, лекарства", "color": "#F44336", "user_id": 0},
            {"name": "Одежда", "description": "Одежда и обувь", "color": "#795548", "user_id": 0},
            {"name": "Отпуск", "description": "Путешествия и отдых", "color": "#00BCD4", "user_id": 0},
            {"name": "Ремонт", "description": "Ремонт квартиры, техники", "color": "#607D8B", "user_id": 0},
            {"name": "Инвестиции", "description": "Фондовый рынок, вклады", "color": "#8BC34A", "user_id": 0}
        ]

        for cat_data in categories_expenses_data:
            existing = db.query(models.CategoryExpense).filter(models.CategoryExpense.name == cat_data["name"]).first()
            if not existing:
                category = models.CategoryExpense(**cat_data)
                db.add(category)

        categories_incomes_data = [
                {"name": "Зарплата", "description": "Основной доход", "color": "#4CAF50", "user_id": 0},
                {"name": "Подработка", "description": "Дополнительный доход", "color": "#4CAF50", "user_id": 0},
                {"name": "Проценты", "description": "Проценты по вкладам", "color": "#4CAF50", "user_id": 0},
            ]
        for cat_data in categories_incomes_data:
            existing = db.query(models.CategoryIncome).filter(models.CategoryIncome.name == cat_data["name"]).first()
            if not existing:
                category = models.CategoryIncome(**cat_data)
                db.add(category)
        # Создание видов трат
        expense_types_data = [
            {"name": "Ежемесячные траты", "description": "Регулярные ежемесячные расходы", "is_monthly": True, "user_id": 0},
            {"name": "Автомобиль", "description": "Ремонт, страховка, техобслуживание", "is_monthly": False, "user_id": 0},
            {"name": "Отпуск", "description": "Путешествия и отдых", "is_monthly": False, "user_id": 0},
            {"name": "Ремонт", "description": "Ремонт квартиры и техники", "is_monthly": False, "user_id": 0},
            {"name": "Инвестиции", "description": "Вложения в фондовый рынок", "is_monthly": False, "user_id": 0},
        ]
        for et_data in expense_types_data:
            existing = db.query(models.ExpenseType).filter(models.ExpenseType.name == et_data["name"]).first()
            if not existing:
                expense_type = models.ExpenseType(**et_data)
                db.add(expense_type)
        
        db.commit()
        print("База данных успешно инициализирована!")
        # Вывод созданных данных
        users = db.query(models.Users).all()
        categories = db.query(models.CategoryExpense).all()
        expense_types = db.query(models.ExpenseType).all()
        print(f"\nСоздано категорий: {len(categories)}")
        print(f"Создано видов трат: {len(expense_types)}")
        print(f"Создан пользователей: {len(users)}")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
