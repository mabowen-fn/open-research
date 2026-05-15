# Updated Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for document compilation (Pandoc + PDF generation fonts)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pandoc \
    weasyprint \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
