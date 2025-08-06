from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import categories_expense, expense_types, expenses, incomes, summary

# Создание таблиц в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cost Accounting API",
    description="API для учета доходов и расходов",
    version="1.0.0"
)

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:9000"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(categories_expense.router)
app.include_router(expense_types.router)
app.include_router(expenses.router)
app.include_router(incomes.router)
app.include_router(summary.router)

@app.get("/")
def read_root():
    return {
        "message": "Cost Accounting API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"} 