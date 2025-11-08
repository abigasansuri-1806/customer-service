FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir fastapi uvicorn sqlmodel psycopg2-binary python-dotenv aiokafka

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
