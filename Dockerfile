FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if you need PDF parsing libraries later
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set default command to run both steps sequentially
CMD ["sh", "-c", "python src/paper_fetcher.py && python src/pipeline.py"]
