#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных с начальными данными
"""

from app.database import SessionLocal, engine
from app import models, crud, schemas
from datetime import datetime

def init_db():
    db = SessionLocal()
    
    try:
        # Создание таблиц
        models.Base.metadata.create_all(bind=engine)
        
        # Создание начальных категорий
        categories_expenses_data = [
            {"name": "Продукты", "description": "Продукты питания", "color": "#4CAF50"},
            {"name": "Транспорт", "description": "Общественный транспорт, такси", "color": "#2196F3"},
            {"name": "Автомобиль", "description": "Топливо, ремонт, страховка", "color": "#FF9800"},
            {"name": "Жилье", "description": "Квартплата, коммунальные услуги", "color": "#9C27B0"},
            {"name": "Развлечения", "description": "Кино, рестораны, хобби", "color": "#E91E63"},
            {"name": "Здоровье", "description": "Медицина, лекарства", "color": "#F44336"},
            {"name": "Одежда", "description": "Одежда и обувь", "color": "#795548"},
            {"name": "Отпуск", "description": "Путешествия и отдых", "color": "#00BCD4"},
            {"name": "Ремонт", "description": "Ремонт квартиры, техники", "color": "#607D8B"},
            {"name": "Инвестиции", "description": "Фондовый рынок, вклады", "color": "#8BC34A"}
        ]
        
        for cat_data in categories_expenses_data:
            existing = db.query(models.CategoryExpense).filter(models.CategoryExpense.name == cat_data["name"]).first()
            if not existing:
                category = models.CategoryExpense(**cat_data)
                db.add(category)
        
                categories_incomes_data = [
            {"name": "Зарплата", "description": "Основной доход", "color": "#4CAF50"},
            {"name": "Подработка", "description": "Дополнительный доход", "color": "#4CAF50"},
            {"name": "Проценты", "description": "Проценты по вкладам", "color": "#4CAF50"},
        ]
        
        for cat_data in categories_incomes_data:
            existing = db.query(models.CategoryIncome).filter(models.CategoryIncome.name == cat_data["name"]).first()
            if not existing:
                category = models.CategoryIncome(**cat_data)
                db.add(category)
        
        # Создание видов трат
        expense_types_data = [
            {"name": "Ежемесячные траты", "description": "Регулярные ежемесячные расходы", "is_monthly": True},
            {"name": "Автомобиль", "description": "Ремонт, страховка, техобслуживание", "is_monthly": False},
            {"name": "Отпуск", "description": "Путешествия и отдых", "is_monthly": False},
            {"name": "Ремонт", "description": "Ремонт квартиры и техники", "is_monthly": False},
            {"name": "Инвестиции", "description": "Вложения в фондовый рынок", "is_monthly": False},
        ]
        
        for et_data in expense_types_data:
            existing = db.query(models.ExpenseType).filter(models.ExpenseType.name == et_data["name"]).first()
            if not existing:
                expense_type = models.ExpenseType(**et_data)
                db.add(expense_type)
        
        db.commit()
        print("База данных успешно инициализирована!")
        
        # Вывод созданных данных
        categories = db.query(models.CategoryExpense).all()
        expense_types = db.query(models.ExpenseType).all()
        
        print(f"\nСоздано категорий: {len(categories)}")
        print(f"Создано видов трат: {len(expense_types)}")
        
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 