FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "web/manage.py", "runserver", "0.0.0.0:8000"]