# Usamos una imagen ligera de Python 3.11 (compatible y estable)
FROM python:3.11-slim

# Variables de entorno para evitar archivos .pyc y buffering en logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar ciertas libs
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# El CMD se define en el docker-compose.yml, así que aquí no es necesario,
# pero podemos dejar uno por defecto.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]