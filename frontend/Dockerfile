# Build stage для фронтенда
FROM node:20 AS frontend-builder


WORKDIR /app/frontend
COPY frontend ./ 
RUN npm ci
RUN npm install
RUN npm run build  # Собираем статику (dist)

# Копируем собранную статику фронтенда из builder-а
COPY --from=frontend-builder /app/frontend/dist/spa /app/static/dist/spa


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
