FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BEDFLOW_USE_WAITRESS=true \
    BEDFLOW_API_HOST=127.0.0.1 \
    BEDFLOW_API_PORT=5005

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["python", "app.py"]
