import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (categories_expense, categories_income, expense_types,
                         expenses, incomes, summary)
from auth.routers import router as user_router

# from auth import routers

# Создание таблиц в базе данных
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cost Accounting API",
    description="API для учета доходов и расходов",
    version="1.0.0"
)

# Определяем путь к статике фронтенда
# frontend_dist = Path(__file__).parent / "static" / "dist" / "spa"

# app.mount('/static', StaticFiles(directory=str(frontend_dist), html=True), name='static')


# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000", "http://localhost:9001"],  # Vue dev server
    allow_origins=["*"],
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
app.include_router(user_router, prefix='/api')


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
