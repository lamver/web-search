# Используем легкий образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения (наш main.py из предыдущего шага)
COPY main.py .

# Открываем порт 8000
EXPOSE 8000

# Запускаем сервер
CMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8000"]