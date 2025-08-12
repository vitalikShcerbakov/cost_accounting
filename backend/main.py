from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.database import engine
from backend import models
from backend.routers import categories_expense, categories_income, expense_types, expenses, incomes, summary

# Создание таблиц в базе данных
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cost Accounting API",
    description="API для учета доходов и расходов",
    version="1.0.0"
)

# Определяем путь к статике фронтенда
frontend_dist = Path(__file__).parent / "static" / "dist" / "spa"

app.mount('/static', StaticFiles(directory=str(frontend_dist), html=True), name='static')


# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:9000"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(categories_expense.router, prefix='/api')
app.include_router(categories_income.router, prefix='/api')
app.include_router(expense_types.router, prefix='/api')
app.include_router(expenses.router, prefix='/api')
app.include_router(incomes.router, prefix='/api')
app.include_router(summary.router, prefix='/api')

@app.get("/health")
def health_check():
    return {"status": "healthy"} 