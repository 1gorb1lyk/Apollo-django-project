# Вибір базового образу
FROM python:3.11

# Встановлення робочої директорії
WORKDIR /app

# Копіювання файлів вимог проекту та їх встановлення
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання всіх файлів проекту в контейнер
COPY . /app/
