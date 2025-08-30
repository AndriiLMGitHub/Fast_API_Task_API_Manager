# Використовуємо офіційний Python образ
FROM python:3.12-slim

# Копіюємо весь проєкт у контейнер
COPY . .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt


# Запускаємо FastAPI через Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]