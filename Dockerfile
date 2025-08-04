# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ Utilise $PORT fourni par Render
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "run:app"]
