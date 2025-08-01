# Cost Accounting - Система учета доходов и расходов

Веб-приложение для учета денежных средств с использованием FastAPI (бэкенд) и Vue3/Quasar (фронтенд).

## Функциональность

### Основные возможности:
- **Учет доходов** - добавление, редактирование, удаление доходов
- **Учет расходов** - добавление, редактирование, удаление расходов
- **Категории** - создание и управление категориями доходов и расходов
- **Виды трат** - разделение на ежемесячные и разовые траты
- **Аналитика** - месячные сводки и отчеты по категориям

### Виды трат:
- **Ежемесячные траты** - регулярные расходы с фиксированным бюджетом
- **Разовые траты** - автомобиль (ремонт, страховка), отпуск, ремонт, инвестиции

## Структура проекта

```
cost_accounting/
├── app/
│   ├── __init__.py
│   ├── main.py              # Основной файл FastAPI
│   ├── database.py          # Конфигурация базы данных
│   ├── models.py            # SQLAlchemy модели
│   ├── schemas.py           # Pydantic схемы
│   ├── crud.py             # CRUD операции
│   └── routers/            # API роутеры
│       ├── __init__.py
│       ├── categories.py
│       ├── expense_types.py
│       ├── expenses.py
│       ├── incomes.py
│       └── summary.py
├── requirements.txt
└── README.md
```

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск сервера

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Документация API

После запуска сервера документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Категории (`/categories`)
- `GET /categories/` - список всех категорий
- `POST /categories/` - создание категории
- `GET /categories/{id}` - получение категории по ID
- `PUT /categories/{id}` - обновление категории
- `DELETE /categories/{id}` - удаление категории

### Виды трат (`/expense-types`)
- `GET /expense-types/` - список всех видов трат
- `GET /expense-types/monthly` - список ежемесячных видов трат
- `POST /expense-types/` - создание вида трат
- `GET /expense-types/{id}` - получение вида трат по ID
- `PUT /expense-types/{id}` - обновление вида трат
- `DELETE /expense-types/{id}` - удаление вида трат

### Расходы (`/expenses`)
- `GET /expenses/` - список расходов с фильтрацией
- `POST /expenses/` - создание расхода
- `GET /expenses/{id}` - получение расхода по ID
- `PUT /expenses/{id}` - обновление расхода
- `DELETE /expenses/{id}` - удаление расхода

### Доходы (`/incomes`)
- `GET /incomes/` - список доходов с фильтрацией
- `POST /incomes/` - создание дохода
- `GET /incomes/{id}` - получение дохода по ID
- `PUT /incomes/{id}` - обновление дохода
- `DELETE /incomes/{id}` - удаление дохода

### Сводки (`/summary`)
- `GET /summary/monthly/{year}/{month}` - месячная сводка
- `GET /summary/category-summary` - сводка по категориям

## Модели данных

### Category (Категории)
- `id` - уникальный идентификатор
- `name` - название категории
- `description` - описание
- `color` - цвет для UI
- `created_at` - дата создания
- `updated_at` - дата обновления

### ExpenseType (Виды трат)
- `id` - уникальный идентификатор
- `name` - название вида трат
- `description` - описание
- `is_monthly` - флаг ежемесячных трат
- `monthly_budget` - месячный бюджет
- `created_at` - дата создания
- `updated_at` - дата обновления

### Expense (Расходы)
- `id` - уникальный идентификатор
- `amount` - сумма
- `description` - описание
- `date` - дата расхода
- `category_id` - ID категории
- `expense_type_id` - ID вида трат
- `created_at` - дата создания
- `updated_at` - дата обновления

### Income (Доходы)
- `id` - уникальный идентификатор
- `amount` - сумма
- `description` - описание
- `date` - дата дохода
- `category_id` - ID категории
- `created_at` - дата создания
- `updated_at` - дата обновления

## База данных

По умолчанию используется SQLite база данных (`cost_accounting.db`). 
Для продакшена рекомендуется использовать PostgreSQL.

Для изменения базы данных создайте файл `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/cost_accounting
``` 