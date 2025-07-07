# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./app /app/app
COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
