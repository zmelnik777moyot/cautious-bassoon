FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y gcc libffi-dev && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Запуск приложения
CMD ["python", "main.py"]
