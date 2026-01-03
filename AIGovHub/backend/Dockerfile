FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies directly with pip
RUN pip install fastapi uvicorn sqlmodel psycopg2-binary alembic pydantic python-multipart \
    python-jose passlib reportlab

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
