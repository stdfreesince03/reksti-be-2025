FROM --platform=linux/amd64 python:3.10-bullseye

WORKDIR /app

# Install system dependencies first (rarely change)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements file first (better caching)
COPY requirements.txt .

# Install requirements (which I assume includes face_recognition)
RUN pip install --no-cache-dir -r requirements.txt

# Install face_recognition_models (as in your original)
RUN pip install git+https://github.com/ageitgey/face_recognition_models

# Environment variables for better logging
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Copy application code (changes frequently, should be last)
COPY . .

# Fix for exec format error - use python -m
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]