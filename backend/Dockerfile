# Используем свежий образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements и ставим зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . /app

# Запуск Flask-приложения
CMD ["python", "src/app.py"]
