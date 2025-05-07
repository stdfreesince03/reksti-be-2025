FROM python:3.12.3-bullseye

WORKDIR /

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install git+https://github.com/ageitgey/face_recognition_models

EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
