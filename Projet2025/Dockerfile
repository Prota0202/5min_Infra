# Image Python légère
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PORT=8000

# Dépendances système minimales
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier l'application (dossier local 'app')
COPY app/app.py /app/app.py
COPY app/templates /app/templates

# Installer Flask et Gunicorn
RUN pip install --no-cache-dir flask gunicorn pymongo

EXPOSE 8000

# Lancer via Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "app:app"]
