FROM python:3.12-slim

# Dependencias del sistema
RUN apt update && apt install -y \
    tesseract-ocr \
    libnss3 \
    libasound2 \
    fonts-liberation \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Instalar Playwright
RUN pip install playwright
RUN playwright install --with-deps chromium

# Copiar proyecto
WORKDIR /app
COPY . /app

# Instalar dependencias Python
RUN pip install -r requirements.txt

CMD ["pytest", "-s"]
