# Build stage для фронтенда
FROM node:20 AS frontend-builder


WORKDIR /app/frontend
# COPY frontend/package.json frontend/package-lock.json ./
COPY frontend ./ 
RUN npm ci
RUN npm install

COPY frontend .
RUN npm run build  # Собираем статику (dist)

# Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем backend
COPY . .

# Копируем собранную статику фронтенда из builder-а
# COPY --from=frontend-builder /app/frontend/dist /app/static
COPY --from=frontend-builder /app/frontend/dist/spa /app/static/dist/spa


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
